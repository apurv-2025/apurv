# app/api/v1/endpoints/websockets.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.websockets.connection_manager import ConnectionManager
from app.websockets.notifications import NotificationManager
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Global connection manager
manager = ConnectionManager()
notification_manager = NotificationManager(manager)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    await manager.send_personal_message(
                        json.dumps({"type": "pong", "timestamp": message.get("timestamp")}),
                        websocket
                    )
                elif message.get("type") == "subscribe":
                    # Handle subscription to specific events
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "subscription_confirmed",
                            "channels": message.get("channels", [])
                        }),
                        websocket
                    )
                else:
                    # Echo unknown messages
                    await manager.send_personal_message(data, websocket)
                    
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    json.dumps({"type": "error", "message": "Invalid JSON"}),
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        logger.info(f"Client {client_id} disconnected")


@router.websocket("/ws/notifications/{user_id}")
async def notification_websocket(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        # Send welcome message
        await manager.send_personal_message(
            json.dumps({
                "type": "connected",
                "message": "Connected to notifications",
                "user_id": user_id
            }),
            websocket
        )
        
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            logger.info(f"Received from user {user_id}: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        logger.info(f"User {user_id} disconnected from notifications")
