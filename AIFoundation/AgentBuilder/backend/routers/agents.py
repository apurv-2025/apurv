from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from models.database import get_db
from models.agent import Agent, AgentInteraction
from models.user import User
from routers.auth import get_current_user
from services.llm_service import LLMService

router = APIRouter()

class AgentCreate(BaseModel):
    name: str
    description: str
    role: str
    persona: str
    instructions: str
    configuration: Optional[dict] = {}

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    persona: Optional[str] = None
    instructions: Optional[str] = None
    configuration: Optional[dict] = None
    is_active: Optional[bool] = None

class AgentResponse(BaseModel):
    id: int
    name: str
    description: str
    role: str
    persona: str
    instructions: str
    configuration: dict
    is_active: bool

class ChatRequest(BaseModel):
    message: str
    agent_id: int

class ChatResponse(BaseModel):
    response: str
    confidence: float

@router.post("/", response_model=AgentResponse)
async def create_agent(
    agent: AgentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_agent = Agent(
        name=agent.name,
        description=agent.description,
        role=agent.role,
        persona=agent.persona,
        instructions=agent.instructions,
        configuration=agent.configuration,
        owner_id=current_user.id
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.get("/", response_model=List[AgentResponse])
async def get_agents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agents = db.query(Agent).filter(Agent.owner_id == current_user.id).all()
    return agents

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_update: AgentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    for field, value in agent_update.dict(exclude_unset=True).items():
        setattr(agent, field, value)
    
    db.commit()
    db.refresh(agent)
    return agent

@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agent = db.query(Agent).filter(
        Agent.id == agent_id,
        Agent.owner_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(agent)
    db.commit()
    return {"message": "Agent deleted successfully"}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agent = db.query(Agent).filter(
        Agent.id == chat_request.agent_id,
        Agent.owner_id == current_user.id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Initialize LLM service
    llm_service = LLMService()
    
    # Generate response
    response = await llm_service.generate_response(
        agent=agent,
        user_message=chat_request.message,
        db=db
    )
    
    # Log interaction
    interaction = AgentInteraction(
        agent_id=agent.id,
        user_query=chat_request.message,
        agent_response=response.get("response", ""),
        metadata={
            "confidence": response.get("confidence", 0.0),
            "user_id": current_user.id
        }
    )
    db.add(interaction)
    db.commit()
    
    return ChatResponse(
        response=response.get("response", ""),
        confidence=response.get("confidence", 0.0)
    )
