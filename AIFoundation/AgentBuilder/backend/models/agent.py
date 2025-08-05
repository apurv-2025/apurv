from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    role = Column(String)  # billing, front_desk, general
    persona = Column(Text)
    instructions = Column(Text)
    configuration = Column(JSON)  # stores agent config, templates, etc.
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    owner = relationship("User", back_populates="agents")

User.agents = relationship("Agent", back_populates="owner")

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    title = Column(String)
    content = Column(Text)
    source_type = Column(String)  # pdf, manual, api
    source_url = Column(String)
    vector_id = Column(String)  # reference to vector DB
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    agent = relationship("Agent")

class AgentInteraction(Base):
    __tablename__ = "agent_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    user_query = Column(Text)
    agent_response = Column(Text)
    metadata = Column(JSON)  # contains session info, confidence scores, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    agent = relationship("Agent")
