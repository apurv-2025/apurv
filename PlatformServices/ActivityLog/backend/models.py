# ========================
# models.py
# ========================
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to activity events
    activity_events = relationship("ActivityEvent", back_populates="user")


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    date_of_birth = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, ForeignKey("users.id"))
    
    # Relationship to activity events
    activity_events = relationship("ActivityEvent", back_populates="client")


class ActivityEvent(Base):
    __tablename__ = "activity_events"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    client_id = Column(String, ForeignKey("clients.id"), nullable=True)
    event_type = Column(String, nullable=False)  # sign_in, hipaa_audit, history
    event_category = Column(String, nullable=False)  # login, logout, view, create, update, delete
    event_description = Column(Text, nullable=False)
    ip_address = Column(String)
    location = Column(String)
    user_agent = Column(String)
    session_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    metadata = Column(JSON)  # Additional event-specific data
    
    # Relationships
    user = relationship("User", back_populates="activity_events")
    client = relationship("Client", back_populates="activity_events")


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    document_type = Column(String, nullable=False)  # superbill, statement, note, assessment
    document_number = Column(String)
    title = Column(String, nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, ForeignKey("users.id"))
    
    # Relationships
    client = relationship("Client")
    creator = relationship("User")


