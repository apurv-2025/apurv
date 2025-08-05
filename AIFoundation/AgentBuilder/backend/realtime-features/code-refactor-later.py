# Real-time Features & WebSocket Implementation

# websocket_manager.py
import asyncio
import json
import logging
from typing import Dict, List, Set
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import redis
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = {}  # user_id -> set of websockets
        self.agent_subscribers: Dict[int, Set[WebSocket]] = {}   # agent_id -> set of websockets
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a websocket for a specific user"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "message": "Connected to AI Agent Builder",
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
        
        logger.info(f"User {user_id} connected via WebSocket")
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """Disconnect a websocket"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        # Remove from agent subscriptions
        for agent_id in list(self.agent_subscribers.keys()):
            self.agent_subscribers[agent_id].discard(websocket)
            if not self.agent_subscribers[agent_id]:
                del self.agent_subscribers[agent_id]
        
        logger.info(f"User {user_id} disconnected from WebSocket")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific websocket"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending message to websocket: {e}")
    
    async def send_message_to_user(self, message: dict, user_id: int):
        """Send a message to all websockets for a specific user"""
        if user_id in self.active_connections:
            disconnected = []
            for websocket in self.active_connections[user_id].copy():
                try:
                    await websocket.send_text(json.dumps(message))
                except:
                    disconnected.append(websocket)
            
            # Clean up disconnected websockets
            for ws in disconnected:
                self.active_connections[user_id].discard(ws)
    
    async def subscribe_to_agent(self, websocket: WebSocket, agent_id: int):
        """Subscribe a websocket to agent updates"""
        if agent_id not in self.agent_subscribers:
            self.agent_subscribers[agent_id] = set()
        
        self.agent_subscribers[agent_id].add(websocket)
    
    async def broadcast_agent_update(self, agent_id: int, message: dict):
        """Broadcast an update to all subscribers of an agent"""
        if agent_id in self.agent_subscribers:
            disconnected = []
            for websocket in self.agent_subscribers[agent_id].copy():
                try:
                    await websocket.send_text(json.dumps(message))
                except:
                    disconnected.append(websocket)
            
            # Clean up disconnected websockets
            for ws in disconnected:
                self.agent_subscribers[agent_id].discard(ws)
    
    async def broadcast_to_practice(self, practice_id: int, message: dict):
        """Broadcast a message to all users in a practice"""
        # This would require storing practice_id mapping
        # For now, we'll store it in Redis
        practice_users = self.redis_client.smembers(f"practice:{practice_id}:users")
        
        for user_id in practice_users:
            await self.send_message_to_user(message, int(user_id))

# WebSocket connection manager instance
manager = ConnectionManager()

# websocket_routes.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from routers.auth import get_current_user_websocket
from models.user import User

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "subscribe_agent":
                agent_id = message.get("agent_id")
                if agent_id:
                    await manager.subscribe_to_agent(websocket, agent_id)
                    await manager.send_personal_message({
                        "type": "subscribed",
                        "agent_id": agent_id,
                        "message": f"Subscribed to agent {agent_id} updates"
                    }, websocket)
            
            elif message.get("type") == "ping":
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                }, websocket)
            
            elif message.get("type") == "typing":
                # Broadcast typing indicator to other users in the same conversation
                agent_id = message.get("agent_id")
                if agent_id:
                    await manager.broadcast_agent_update(agent_id, {
                        "type": "user_typing",
                        "user_id": user_id,
                        "agent_id": agent_id,
                        "timestamp": datetime.utcnow().isoformat()
                    })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

# real_time_chat.py
import asyncio
from typing import Dict, Any
from services.llm_service import LLMService
from websocket_manager import manager
from models.agent import AgentInteraction
from sqlalchemy.orm import Session

class RealTimeChatService:
    def __init__(self):
        self.llm_service = LLMService()
        self.active_conversations: Dict[str, Dict] = {}  # conversation_id -> conversation_data
    
    async def start_conversation(self, user_id: int, agent_id: int, db: Session) -> str:
        """Start a new real-time conversation"""
        conversation_id = f"{user_id}_{agent_id}_{datetime.utcnow().timestamp()}"
        
        self.active_conversations[conversation_id] = {
            "user_id": user_id,
            "agent_id": agent_id,
            "messages": [],
            "started_at": datetime.utcnow(),
            "status": "active"
        }
        
        # Notify user that conversation started
        await manager.send_message_to_user({
            "type": "conversation_started",
            "conversation_id": conversation_id,
            "agent_id": agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }, user_id)
        
        return conversation_id
    
    async def send_message(self, conversation_id: str, user_message: str, db: Session) -> Dict[str, Any]:
        """Process a message in real-time conversation"""
        if conversation_id not in self.active_conversations:
            raise ValueError("Conversation not found")
        
        conversation = self.active_conversations[conversation_id]
        user_id = conversation["user_id"]
        agent_id = conversation["agent_id"]
        
        # Add user message to conversation
        user_msg = {
            "role": "user",
            "content": user_message,
            "timestamp": datetime.utcnow().isoformat()
        }
        conversation["messages"].append(user_msg)
        
        # Notify typing indicator
        await manager.send_message_to_user({
            "type": "agent_typing",
            "conversation_id": conversation_id,
            "agent_id": agent_id
        }, user_id)
        
        try:
            # Get agent from database
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                raise ValueError("Agent not found")
            
            # Generate response
            response_data = await self.llm_service.generate_response(
                agent=agent,
                user_message=user_message,
                db=db
            )
            
            # Add agent response to conversation
            agent_msg = {
                "role": "assistant",
                "content": response_data["response"],
                "confidence": response_data.get("confidence", 0.0),
                "timestamp": datetime.utcnow().isoformat()
            }
            conversation["messages"].append(agent_msg)
            
            # Log interaction in database
            interaction = AgentInteraction(
                agent_id=agent_id,
                user_query=user_message,
                agent_response=response_data["response"],
                metadata={
                    "conversation_id": conversation_id,
                    "confidence": response_data.get("confidence", 0.0),
                    "real_time": True
                }
            )
            db.add(interaction)
            db.commit()
            
            # Send response to user
            await manager.send_message_to_user({
                "type": "agent_response",
                "conversation_id": conversation_id,
                "message": agent_msg,
                "timestamp": datetime.utcnow().isoformat()
            }, user_id)
            
            return agent_msg
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            
            error_msg = {
                "role": "assistant",
                "content": "I'm sorry, I encountered an error processing your message. Please try again.",
                "error": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await manager.send_message_to_user({
                "type": "agent_response",
                "conversation_id": conversation_id,
                "message": error_msg,
                "error": True
            }, user_id)
            
            return error_msg
    
    async def end_conversation(self, conversation_id: str, user_id: int):
        """End a real-time conversation"""
        if conversation_id in self.active_conversations:
            self.active_conversations[conversation_id]["status"] = "ended"
            self.active_conversations[conversation_id]["ended_at"] = datetime.utcnow()
            
            await manager.send_message_to_user({
                "type": "conversation_ended",
                "conversation_id": conversation_id,
                "timestamp": datetime.utcnow().isoformat()
            }, user_id)
            
            # Clean up after some time
            await asyncio.sleep(300)  # Keep for 5 minutes
            if conversation_id in self.active_conversations:
                del self.active_conversations[conversation_id]

# Enhanced chat routes
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

chat_router = APIRouter()
chat_service = RealTimeChatService()

class StartConversationRequest(BaseModel):
    agent_id: int

class SendMessageRequest(BaseModel):
    conversation_id: str
    message: str

@chat_router.post("/conversations/start")
async def start_conversation(
    request: StartConversationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new real-time conversation with an agent"""
    conversation_id = await chat_service.start_conversation(
        user_id=current_user.id,
        agent_id=request.agent_id,
        db=db
    )
    
    return {"conversation_id": conversation_id}

@chat_router.post("/conversations/message")
async def send_message(
    request: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in a real-time conversation"""
    try:
        response = await chat_service.send_message(
            conversation_id=request.conversation_id,
            user_message=request.message,
            db=db
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@chat_router.post("/conversations/{conversation_id}/end")
async def end_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """End a real-time conversation"""
    await chat_service.end_conversation(conversation_id, current_user.id)
    return {"message": "Conversation ended"}

# notification_service.py
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from models.database import Base

class NotificationType(str, Enum):
    AGENT_UPDATE = "agent_update"
    SYSTEM_ALERT = "system_alert"
    COMPLIANCE_WARNING = "compliance_warning"
    PERFORMANCE_ALERT = "performance_alert"
    SECURITY_ALERT = "security_alert"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # None for system-wide notifications
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    priority = Column(String, default="normal")  # low, normal, high, critical
    read = Column(Boolean, default=False)
    action_url = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_notification(
        self,
        title: str,
        message: str,
        notification_type: NotificationType,
        user_id: Optional[int] = None,
        priority: str = "normal",
        action_url: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> Notification:
        """Create a new notification"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            priority=priority,
            action_url=action_url,
            metadata=metadata or {}
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        # Send real-time notification if user is connected
        if user_id:
            await manager.send_message_to_user({
                "type": "notification",
                "notification": {
                    "id": notification.id,
                    "title": notification.title,
                    "message": notification.message,
                    "type": notification.type,
                    "priority": notification.priority,
                    "action_url": notification.action_url,
                    "created_at": notification.created_at.isoformat()
                }
            }, user_id)
        
        return notification
    
    async def notify_agent_update(self, agent_id: int, agent_name: str, user_id: int):
        """Notify about agent updates"""
        await self.create_notification(
            title="Agent Updated",
            message=f"Your agent '{agent_name}' has been successfully updated.",
            notification_type=NotificationType.AGENT_UPDATE,
            user_id=user_id,
            action_url=f"/agents/{agent_id}"
        )
    
    async def notify_compliance_warning(self, message: str, user_id: Optional[int] = None):
        """Notify about compliance issues"""
        await self.create_notification(
            title="Compliance Warning",
            message=message,
            notification_type=NotificationType.COMPLIANCE_WARNING,
            user_id=user_id,
            priority="high",
            action_url="/compliance"
        )
    
    async def notify_security_alert(self, message: str, user_id: Optional[int] = None):
        """Notify about security alerts"""
        await self.create_notification(
            title="Security Alert",
            message=message,
            notification_type=NotificationType.SECURITY_ALERT,
            user_id=user_id,
            priority="critical",
            action_url="/security"
        )
    
    def mark_as_read(self, notification_id: int, user_id: int) -> bool:
        """Mark a notification as read"""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if notification:
            notification.read = True
            self.db.commit()
            return True
        
        return False
    
    def get_user_notifications(
        self, 
        user_id: int, 
        unread_only: bool = False, 
        limit: int = 50
    ) -> List[Notification]:
        """Get notifications for a user"""
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.read == False)
        
        return query.order_by(Notification.created_at.desc()).limit(limit).all()

# Add WebSocket routes to main app
from main import app
app.include_router(router, prefix="/ws", tags=["websocket"])
app.include_router(chat_router, prefix="/chat", tags=["real-time-chat"])

# Background tasks for real-time features
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background tasks
    task = asyncio.create_task(background_monitor())
    yield
    # Clean up
    task.cancel()

async def background_monitor():
    """Background task to monitor system health and send alerts"""
    while True:
        try:
            # Check system health every 30 seconds
            await check_system_health()
            await asyncio.sleep(30)
        except Exception as e:
            logger.error(f"Background monitor error: {e}")
            await asyncio.sleep(60)

async def check_system_health():
    """Check various system health metrics"""
    # Check database connectivity
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
    except Exception as e:
        await manager.broadcast_to_practice(
            practice_id=None,  # System-wide alert
            message={
                "type": "system_alert",
                "severity": "critical",
                "message": "Database connectivity issues detected",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    # Check LLM service health
    # Add more health checks as needed
