# services/vector_service_enhanced.py
import pinecone
import openai
import faiss
import numpy as np
import os
import pickle
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer

class VectorService:
    def __init__(self):
        self.provider = os.getenv("VECTOR_PROVIDER", "pinecone")  # pinecone, faiss
        self.setup_provider()
    
    def setup_provider(self):
        """Initialize the selected vector database provider"""
        if self.provider == "pinecone":
            pinecone.init(
                api_key=os.getenv("PINECONE_API_KEY"),
                environment=os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
            )
            self.index_name = "ai-agents-knowledge"
            
            if self.index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=self.index_name,
                    dimension=1536,  # OpenAI embedding dimension
                    metric="cosine"
                )
            
            self.index = pinecone.Index(self.index_name)
            openai.api_key = os.getenv("OPENAI_API_KEY")
            
        elif self.provider == "faiss":
            # Local FAISS setup
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.dimension = 384  # all-MiniLM-L6-v2 dimension
            self.index = faiss.IndexFlatIP(self.dimension)  # Inner Product for cosine similarity
            self.documents = {}  # Store document metadata
            self.load_local_index()
    
    def load_local_index(self):
        """Load existing FAISS index from disk"""
        try:
            if os.path.exists("faiss_index.bin"):
                self.index = faiss.read_index("faiss_index.bin")
            if os.path.exists("documents.pkl"):
                with open("documents.pkl", "rb") as f:
                    self.documents = pickle.load(f)
        except Exception as e:
            print(f"Warning: Could not load existing index: {e}")
    
    def save_local_index(self):
        """Save FAISS index to disk"""
        try:
            faiss.write_index(self.index, "faiss_index.bin")
            with open("documents.pkl", "wb") as f:
                pickle.dump(self.documents, f)
        except Exception as e:
            print(f"Warning: Could not save index: {e}")
    
    async def add_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add a document to the vector database"""
        if self.provider == "pinecone":
            return await self._add_document_pinecone(content, metadata)
        elif self.provider == "faiss":
            return await self._add_document_faiss(content, metadata)
    
    async def _add_document_pinecone(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add document to Pinecone"""
        embedding_response = openai.Embedding.create(
            input=content,
            model="text-embedding-ada-002"
        )
        embedding = embedding_response['data'][0]['embedding']
        
        vector_id = f"doc_{metadata.get('agent_id', 'unknown')}_{hash(content)}"
        
        self.index.upsert([(vector_id, embedding, metadata)])
        
        return vector_id
    
    async def _add_document_faiss(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add document to FAISS"""
        embedding = self.embedding_model.encode([content])[0]
        
        # Normalize for cosine similarity
        embedding = embedding / np.linalg.norm(embedding)
        
        vector_id = f"doc_{metadata.get('agent_id', 'unknown')}_{hash(content)}"
        doc_index = self.index.ntotal
        
        self.index.add(np.array([embedding], dtype=np.float32))
        self.documents[doc_index] = {
            "id": vector_id,
            "content": content,
            "metadata": metadata
        }
        
        self.save_local_index()
        return vector_id
    
    async def search_similar(self, query: str, agent_id: int, top_k: int = 5) -> str:
        """Search for similar documents"""
        if self.provider == "pinecone":
            return await self._search_pinecone(query, agent_id, top_k)
        elif self.provider == "faiss":
            return await self._search_faiss(query, agent_id, top_k)
    
    async def _search_pinecone(self, query: str, agent_id: int, top_k: int) -> str:
        """Search using Pinecone"""
        embedding_response = openai.Embedding.create(
            input=query,
            model="text-embedding-ada-002"
        )
        query_embedding = embedding_response['data'][0]['embedding']
        
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            filter={"agent_id": agent_id},
            include_metadata=True
        )
        
        context_parts = []
        for match in results['matches']:
            if match['score'] > 0.7:
                context_parts.append(match['metadata'].get('content', ''))
        
        return "\n\n".join(context_parts)
    
    async def _search_faiss(self, query: str, agent_id: int, top_k: int) -> str:
        """Search using FAISS"""
        query_embedding = self.embedding_model.encode([query])[0]
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        scores, indices = self.index.search(
            np.array([query_embedding], dtype=np.float32), 
            min(top_k, self.index.ntotal)
        )
        
        context_parts = []
        for score, idx in zip(scores[0], indices[0]):
            if idx in self.documents and score > 0.7:
                doc = self.documents[idx]
                if doc["metadata"].get("agent_id") == agent_id:
                    context_parts.append(doc["content"])
        
        return "\n\n".join(context_parts)
