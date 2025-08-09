"""
ActivityLog Service Integration for SaaSFoundation
Handles all activity logging through API calls to the ActivityLog service
"""

import httpx
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from fastapi import Request
import json

logger = logging.getLogger(__name__)

class ActivityLogService:
    """Service for logging activities to the ActivityLog service"""
    
    def __init__(self, activity_log_url: str = "http://localhost:8001"):
        self.activity_log_url = activity_log_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        if request.client:
            return request.client.host
        return "unknown"
    
    def _get_user_agent(self, request: Request) -> str:
        """Extract user agent from request"""
        return request.headers.get("user-agent", "unknown")
    
    async def log_activity(
        self,
        event_type: str,
        event_category: str,
        event_description: str,
        user_id: str,
        request: Optional[Request] = None,
        client_id: Optional[str] = None,
        event_metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        location: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Log an activity event to the ActivityLog service"""
        try:
            # Prepare event data
            event_data = {
                "event_type": event_type,
                "event_category": event_category,
                "event_description": event_description,
                "client_id": client_id,
                "ip_address": ip_address,
                "location": location,
                "user_agent": self._get_user_agent(request) if request else None,
                "session_id": session_id,
                "event_metadata": event_metadata or {}
            }
            
            # Add IP address from request if not provided
            if not event_data["ip_address"] and request:
                event_data["ip_address"] = self._get_client_ip(request)
            
            # Send to ActivityLog service
            response = await self.client.post(
                f"{self.activity_log_url}/api/activity-events",
                json=event_data,
                headers={
                    "Authorization": f"Bearer mock-token",  # In production, use real token
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Activity logged successfully: {event_type} - {event_description}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to log activity: {e}")
            return None
    
    # ============================================================================
    # Specific Activity Logging Methods
    # ============================================================================
    
    async def log_user_registration(
        self,
        user_id: str,
        email: str,
        request: Request,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """Log user registration activity"""
        metadata = {
            "email": email,
            "success": success,
            "error_message": error_message
        }
        
        event_type = "user_registration_success" if success else "user_registration_failed"
        description = f"User registration {'completed' if success else 'failed'} for {email}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="authentication",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_user_login(
        self,
        user_id: str,
        email: str,
        request: Request,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """Log user login activity"""
        metadata = {
            "email": email,
            "success": success,
            "error_message": error_message
        }
        
        event_type = "user_login_success" if success else "user_login_failed"
        description = f"User login {'completed' if success else 'failed'} for {email}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="authentication",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_user_logout(
        self,
        user_id: str,
        email: str,
        request: Request
    ):
        """Log user logout activity"""
        metadata = {
            "email": email
        }
        
        return await self.log_activity(
            event_type="user_logout",
            event_category="authentication",
            event_description=f"User logout for {email}",
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_user_profile_update(
        self,
        user_id: str,
        request: Request,
        updated_fields: List[str],
        success: bool = True
    ):
        """Log user profile update activity"""
        metadata = {
            "updated_fields": updated_fields,
            "success": success
        }
        
        event_type = "user_profile_update_success" if success else "user_profile_update_failed"
        description = f"User profile update {'completed' if success else 'failed'}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="user_management",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_organization_creation(
        self,
        user_id: str,
        organization_name: str,
        organization_id: str,
        request: Request,
        success: bool = True
    ):
        """Log organization creation activity"""
        metadata = {
            "organization_name": organization_name,
            "organization_id": organization_id,
            "success": success
        }
        
        event_type = "organization_creation_success" if success else "organization_creation_failed"
        description = f"Organization '{organization_name}' {'created' if success else 'creation failed'}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="organization_management",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_organization_update(
        self,
        user_id: str,
        organization_name: str,
        organization_id: str,
        request: Request,
        updated_fields: List[str],
        success: bool = True
    ):
        """Log organization update activity"""
        metadata = {
            "organization_name": organization_name,
            "organization_id": organization_id,
            "updated_fields": updated_fields,
            "success": success
        }
        
        event_type = "organization_update_success" if success else "organization_update_failed"
        description = f"Organization '{organization_name}' {'updated' if success else 'update failed'}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="organization_management",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_subscription_creation(
        self,
        user_id: str,
        subscription_id: str,
        plan_name: str,
        amount: float,
        request: Request,
        success: bool = True
    ):
        """Log subscription creation activity"""
        metadata = {
            "subscription_id": subscription_id,
            "plan_name": plan_name,
            "amount": amount,
            "success": success
        }
        
        event_type = "subscription_creation_success" if success else "subscription_creation_failed"
        description = f"Subscription '{plan_name}' {'created' if success else 'creation failed'}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="subscription_management",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_subscription_update(
        self,
        user_id: str,
        subscription_id: str,
        plan_name: str,
        request: Request,
        updated_fields: List[str],
        success: bool = True
    ):
        """Log subscription update activity"""
        metadata = {
            "subscription_id": subscription_id,
            "plan_name": plan_name,
            "updated_fields": updated_fields,
            "success": success
        }
        
        event_type = "subscription_update_success" if success else "subscription_update_failed"
        description = f"Subscription '{plan_name}' {'updated' if success else 'update failed'}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="subscription_management",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_subscription_cancellation(
        self,
        user_id: str,
        subscription_id: str,
        plan_name: str,
        request: Request,
        success: bool = True
    ):
        """Log subscription cancellation activity"""
        metadata = {
            "subscription_id": subscription_id,
            "plan_name": plan_name,
            "success": success
        }
        
        event_type = "subscription_cancellation_success" if success else "subscription_cancellation_failed"
        description = f"Subscription '{plan_name}' {'cancelled' if success else 'cancellation failed'}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="subscription_management",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_payment_processing(
        self,
        user_id: str,
        payment_id: str,
        amount: float,
        currency: str,
        payment_method: str,
        request: Request,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """Log payment processing activity"""
        metadata = {
            "payment_id": payment_id,
            "amount": amount,
            "currency": currency,
            "payment_method": payment_method,
            "success": success,
            "error_message": error_message
        }
        
        event_type = "payment_processing_success" if success else "payment_processing_failed"
        description = f"Payment processing {'completed' if success else 'failed'} for {amount} {currency}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="payment_processing",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_invoice_generation(
        self,
        user_id: str,
        invoice_id: str,
        amount: float,
        currency: str,
        request: Request,
        success: bool = True
    ):
        """Log invoice generation activity"""
        metadata = {
            "invoice_id": invoice_id,
            "amount": amount,
            "currency": currency,
            "success": success
        }
        
        event_type = "invoice_generation_success" if success else "invoice_generation_failed"
        description = f"Invoice generation {'completed' if success else 'failed'} for {amount} {currency}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="invoice_management",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_notification_sent(
        self,
        user_id: str,
        notification_type: str,
        recipient: str,
        request: Request,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """Log notification sending activity"""
        metadata = {
            "notification_type": notification_type,
            "recipient": recipient,
            "success": success,
            "error_message": error_message
        }
        
        event_type = "notification_sent_success" if success else "notification_sent_failed"
        description = f"{notification_type} notification {'sent' if success else 'failed'} to {recipient}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="notification_management",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_data_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        request: Request,
        success: bool = True
    ):
        """Log data access activity"""
        metadata = {
            "resource_type": resource_type,
            "resource_id": resource_id,
            "action": action,
            "success": success
        }
        
        event_type = "data_access_success" if success else "data_access_failed"
        description = f"Data access: {action} on {resource_type} {resource_id}"
        
        return await self.log_activity(
            event_type=event_type,
            event_category="data_access",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=metadata
        )
    
    async def log_security_event(
        self,
        user_id: str,
        event_type: str,
        description: str,
        request: Request,
        severity: str = "medium",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log security-related events"""
        event_metadata = {
            "severity": severity,
            **(metadata or {})
        }
        
        return await self.log_activity(
            event_type=event_type,
            event_category="security",
            event_description=description,
            user_id=user_id,
            request=request,
            event_metadata=event_metadata
        )
    
    async def log_system_event(
        self,
        event_type: str,
        description: str,
        system_user_id: str = "system",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log system-level events"""
        return await self.log_activity(
            event_type=event_type,
            event_category="system",
            event_description=description,
            user_id=system_user_id,
            request=None,
            event_metadata=metadata
        )
    
    # ============================================================================
    # Utility Methods
    # ============================================================================
    
    async def get_activity_events(
        self,
        user_id: str,
        event_type: Optional[str] = None,
        date_range: str = "all",
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Optional[List[Dict[str, Any]]]:
        """Get activity events from the ActivityLog service"""
        try:
            params = {
                "skip": skip,
                "limit": limit
            }
            
            if event_type:
                params["event_type"] = event_type
            if date_range:
                params["date_range"] = date_range
            if search:
                params["search"] = search
            
            response = await self.client.get(
                f"{self.activity_log_url}/api/activity-events",
                params=params,
                headers={
                    "Authorization": f"Bearer mock-token"  # In production, use real token
                }
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Failed to get activity events: {e}")
            return None
    
    async def health_check(self) -> bool:
        """Check if ActivityLog service is healthy"""
        try:
            response = await self.client.get(f"{self.activity_log_url}/health")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"ActivityLog service health check failed: {e}")
            return False

# Global instance for easy access
activity_logger = ActivityLogService() 