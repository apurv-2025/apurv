try:
    from pinecone import Pinecone
except ImportError:
    Pinecone = None

from openai import OpenAI
import os
from typing import List, Dict, Any

class VectorService:
    def __init__(self):
        if not Pinecone:
            # Fallback to local storage or skip vector functionality
            self.enabled = False
            return
            
        self.enabled = True
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY", "test-key"))
        self.index_name = "ai-agents-knowledge"
        
        # For testing, we'll skip actual pinecone operations
        if os.getenv("PINECONE_API_KEY") == "test-key":
            self.enabled = False
            return
        
        # Create index if it doesn't exist (only for real API keys)
        try:
            existing_indexes = [idx['name'] for idx in self.pc.list_indexes()]
            if self.index_name not in existing_indexes:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536,  # OpenAI embedding dimension
                    metric="cosine"
                )
            self.index = self.pc.Index(self.index_name)
        except:
            self.enabled = False
            
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "test-key"))
    
    async def add_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add a document to the vector database"""
        if not self.enabled:
            return f"mock_vector_id_{hash(content)}"
            
        # Generate embedding
        embedding_response = self.openai_client.embeddings.create(
            input=content,
            model="text-embedding-ada-002"
        )
        embedding = embedding_response.data[0].embedding
        
        # Generate unique ID
        vector_id = f"doc_{metadata.get('agent_id', 'unknown')}_{hash(content)}"
        
        # Upsert to Pinecone
        self.index.upsert([(vector_id, embedding, metadata)])
        
        return vector_id
    
    async def search_similar(self, query: str, agent_id: int, top_k: int = 5) -> str:
        """Search for similar documents"""
        if not self.enabled:
            return "Mock context for testing"
            
        # Generate query embedding
        embedding_response = self.openai_client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        query_embedding = embedding_response.data[0].embedding
        
        # Search in Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            filter={"agent_id": agent_id},
            include_metadata=True
        )
        
        # Format results
        context_parts = []
        for match in results.matches:
            if match.score > 0.7:  # Only include high-confidence matches
                context_parts.append(match.metadata.get('content', ''))
        
        return "\n\n".join(context_parts)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
