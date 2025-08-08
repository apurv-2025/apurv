# ========================
# services.py
# ========================
from sqlalchemy.orm import Session
from typing import List
import schemas
import crud


class ActivityLogService:
    def __init__(self):
        self.activity_crud = crud.activity_crud

    def log_sign_in_event(self, db: Session, user_id: str, success: bool, ip_address: str, location: str, user_agent: str):
        event_desc = f"You signed in successfully to SimplePractice web app" if success else "You failed to sign in to SimplePractice account app due to invalid password"
        event = schemas.ActivityEventCreate(
            event_type="sign_in",
            event_category="login" if success else "failed_login",
            event_description=event_desc,
            ip_address=ip_address,
            location=location,
            user_agent=user_agent,
            metadata={"success": success}
        )
        return self.activity_crud.create_event(db, event, user_id)

    def log_hipaa_audit_event(self, db: Session, user_id: str, action: str, resource: str, client_id: str = None, ip_address: str = None, location: str = None):
        if client_id:
            event_desc = f"You {action} {resource} for client"
        else:
            event_desc = f"You {action} the {resource}"
        
        event = schemas.ActivityEventCreate(
            event_type="hipaa_audit",
            event_category="view",
            event_description=event_desc,
            client_id=client_id,
            ip_address=ip_address,
            location=location,
            metadata={"action": action, "resource": resource}
        )
        return self.activity_crud.create_event(db, event, user_id)

    def log_history_event(self, db: Session, user_id: str, action: str, resource: str, resource_id: str = None, client_id: str = None, ip_address: str = None, location: str = None):
        if client_id:
            event_desc = f"You {action} {resource} for client"
        else:
            event_desc = f"You {action} {resource}"
        
        event = schemas.ActivityEventCreate(
            event_type="history",
            event_category=action,
            event_description=event_desc,
            client_id=client_id,
            ip_address=ip_address,
            location=location,
            metadata={"action": action, "resource": resource, "resource_id": resource_id}
        )
        return self.activity_crud.create_event(db, event, user_id)

    def format_events_for_frontend(self, events: List[models.ActivityEvent]) -> List[schemas.ActivityEventResponse]:
        formatted_events = []
        for event in events:
            client_name = None
            if event.client:
                client_name = f"{event.client.first_name} {event.client.last_name}"
            
            formatted_event = schemas.ActivityEventResponse(
                id=event.id,
                date=event.timestamp.strftime("%m/%d/%Y"),
                time=event.timestamp.strftime("%I:%M %p (ET)"),
                event=event.event_description,
                eventType=event.event_type,
                ipAddress=event.ip_address,
                location=event.location,
                clientName=client_name,
                userId=event.user_id,
                details=event.metadata
            )
            formatted_events.append(formatted_event)
        
        return formatted_events


activity_service = ActivityLogService()
