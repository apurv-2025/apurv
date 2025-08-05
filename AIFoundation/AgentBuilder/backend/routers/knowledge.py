from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import PyPDF2
import io

from models.database import get_db
from models.agent import KnowledgeBase, Agent
from models.user import User
from routers.auth import get_current_user
from services.vector_service import VectorService

router = APIRouter()

class KnowledgeCreate(BaseModel):
    agent_id: int
    title: str
    content: str
    source_type: str = "manual"

class KnowledgeResponse(BaseModel):
    id: int
    agent_id: int
    title: str
    content: str
    source_type: str

@router.post("/", response_model=KnowledgeResponse)
async def create_knowledge(
    knowledge: KnowledgeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify agent ownership
    agent = db.query(Agent).filter(
        Agent.id == knowledge.agent_id,
        Agent.owner_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Store in vector database
    vector_service = VectorService()
    vector_id = await vector_service.add_document(
        content=knowledge.content,
        metadata={"agent_id": knowledge.agent_id, "title": knowledge.title}
    )
    
    # Create knowledge base entry
    db_knowledge = KnowledgeBase(
        agent_id=knowledge.agent_id,
        title=knowledge.title,
        content=knowledge.content,
        source_type=knowledge.source_type,
        vector_id=vector_id
    )
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    
    return db_knowledge

@router.post("/upload/{agent_id}")
async def upload_document(
    agent_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify agent ownership
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Extract text from PDF
    content = ""
    if file.content_type == "application/pdf":
        pdf_bytes = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in pdf_reader.pages:
            content += page.extract_text()
    else:
        content = await file.read()
        content = content.decode("utf-8")
    
    # Store in vector database
    vector_service = VectorService()
    vector_id = await vector_service.add_document(
        content=content,
        metadata={"agent_id": agent_id, "title": file.filename}
    )
    
    # Create knowledge base entry
    db_knowledge = KnowledgeBase(
        agent_id=agent_id,
        title=file.filename,
        content=content,
        source_type="pdf" if file.content_type == "application/pdf" else "text",
        vector_id=vector_id
    )
    db.add(db_knowledge)
    db.commit()
    
    return {"message": "Document uploaded successfully", "id": db_knowledge.id}

@router.get("/{agent_id}", response_model=List[KnowledgeResponse])
async def get_knowledge_base(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify agent ownership
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    knowledge_items = db.query(KnowledgeBase).filter(
        KnowledgeBase.agent_id == agent_id
    ).all()
    
    return knowledge_items
