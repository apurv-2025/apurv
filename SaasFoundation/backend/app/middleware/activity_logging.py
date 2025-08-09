"""
Activity Logging Middleware for SaaSFoundation
Automatically logs all activities to the ActivityLog service
"""

import time
import logging
from typing import Callable, Dict, Any
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.services.activity_log import activity_logger

logger = logging.getLogger(__name__)

class ActivityLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically log all activities"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.excluded_paths = {
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico",
            "/static",
            "/api/v1/health"
        }
        
        # Define activity mappings for different endpoints
        self.activity_mappings = {
            # Authentication endpoints
            "POST /api/v1/auth/register": {
                "event_type": "user_registration",
                "event_category": "authentication",
                "description_template": "User registration attempt"
            },
            "POST /api/v1/auth/login": {
                "event_type": "user_login",
                "event_category": "authentication",
                "description_template": "User login attempt"
            },
            "POST /api/v1/auth/logout": {
                "event_type": "user_logout",
                "event_category": "authentication",
                "description_template": "User logout"
            },
            "POST /api/v1/auth/refresh": {
                "event_type": "token_refresh",
                "event_category": "authentication",
                "description_template": "Token refresh attempt"
            },
            
            # User management endpoints
            "GET /api/v1/user/profile": {
                "event_type": "profile_view",
                "event_category": "user_management",
                "description_template": "User profile viewed"
            },
            "PUT /api/v1/user/profile": {
                "event_type": "profile_update",
                "event_category": "user_management",
                "description_template": "User profile updated"
            },
            "DELETE /api/v1/user/profile": {
                "event_type": "profile_deletion",
                "event_category": "user_management",
                "description_template": "User profile deletion"
            },
            
            # Organization endpoints
            "POST /api/v1/organizations": {
                "event_type": "organization_creation",
                "event_category": "organization_management",
                "description_template": "Organization creation"
            },
            "GET /api/v1/organizations": {
                "event_type": "organization_list",
                "event_category": "organization_management",
                "description_template": "Organizations list viewed"
            },
            "GET /api/v1/organizations/{id}": {
                "event_type": "organization_view",
                "event_category": "organization_management",
                "description_template": "Organization details viewed"
            },
            "PUT /api/v1/organizations/{id}": {
                "event_type": "organization_update",
                "event_category": "organization_management",
                "description_template": "Organization updated"
            },
            "DELETE /api/v1/organizations/{id}": {
                "event_type": "organization_deletion",
                "event_category": "organization_management",
                "description_template": "Organization deleted"
            },
            
            # Subscription endpoints
            "POST /api/v1/subscriptions": {
                "event_type": "subscription_creation",
                "event_category": "subscription_management",
                "description_template": "Subscription creation"
            },
            "GET /api/v1/subscriptions": {
                "event_type": "subscription_list",
                "event_category": "subscription_management",
                "description_template": "Subscriptions list viewed"
            },
            "GET /api/v1/subscriptions/{id}": {
                "event_type": "subscription_view",
                "event_category": "subscription_management",
                "description_template": "Subscription details viewed"
            },
            "PUT /api/v1/subscriptions/{id}": {
                "event_type": "subscription_update",
                "event_category": "subscription_management",
                "description_template": "Subscription updated"
            },
            "DELETE /api/v1/subscriptions/{id}": {
                "event_type": "subscription_cancellation",
                "event_category": "subscription_management",
                "description_template": "Subscription cancelled"
            },
            
            # Payment endpoints
            "POST /api/v1/payments": {
                "event_type": "payment_processing",
                "event_category": "payment_processing",
                "description_template": "Payment processing"
            },
            "GET /api/v1/payments": {
                "event_type": "payment_list",
                "event_category": "payment_processing",
                "description_template": "Payments list viewed"
            },
            "GET /api/v1/payments/{id}": {
                "event_type": "payment_view",
                "event_category": "payment_processing",
                "description_template": "Payment details viewed"
            },
            
            # Invoice endpoints
            "POST /api/v1/invoices": {
                "event_type": "invoice_generation",
                "event_category": "invoice_management",
                "description_template": "Invoice generation"
            },
            "GET /api/v1/invoices": {
                "event_type": "invoice_list",
                "event_category": "invoice_management",
                "description_template": "Invoices list viewed"
            },
            "GET /api/v1/invoices/{id}": {
                "event_type": "invoice_view",
                "event_category": "invoice_management",
                "description_template": "Invoice details viewed"
            },
            
            # Notification endpoints
            "POST /api/v1/notifications": {
                "event_type": "notification_sent",
                "event_category": "notification_management",
                "description_template": "Notification sent"
            },
            "GET /api/v1/notifications": {
                "event_type": "notification_list",
                "event_category": "notification_management",
                "description_template": "Notifications list viewed"
            },
            
            # Pricing endpoints
            "GET /api/v1/pricing": {
                "event_type": "pricing_view",
                "event_category": "pricing_management",
                "description_template": "Pricing information viewed"
            },
            "GET /api/v1/pricing/plans": {
                "event_type": "pricing_plans_view",
                "event_category": "pricing_management",
                "description_template": "Pricing plans viewed"
            }
        }
    
    def _should_exclude_path(self, path: str) -> bool:
        """Check if path should be excluded from logging"""
        return any(path.startswith(excluded) for excluded in self.excluded_paths)
    
    def _get_activity_mapping(self, method: str, path: str) -> Dict[str, Any]:
        """Get activity mapping for the given endpoint"""
        # Try exact match first
        key = f"{method} {path}"
        if key in self.activity_mappings:
            return self.activity_mappings[key]
        
        # Try pattern matching for path parameters
        for mapping_key, mapping in self.activity_mappings.items():
            mapping_method, mapping_path = mapping_key.split(" ", 1)
            if mapping_method == method and self._path_matches(mapping_path, path):
                return mapping
        
        # Default mapping for unknown endpoints
        return {
            "event_type": f"{method.lower()}_{path.replace('/', '_').replace('-', '_')}",
            "event_category": "api_access",
            "description_template": f"{method} request to {path}"
        }
    
    def _path_matches(self, pattern: str, path: str) -> bool:
        """Check if path matches pattern with parameters"""
        pattern_parts = pattern.split("/")
        path_parts = path.split("/")
        
        if len(pattern_parts) != len(path_parts):
            return False
        
        for pattern_part, path_part in zip(pattern_parts, path_parts):
            if pattern_part.startswith("{") and pattern_part.endswith("}"):
                continue  # Parameter placeholder
            if pattern_part != path_part:
                return False
        
        return True
    
    def _extract_user_id(self, request: Request) -> str:
        """Extract user ID from request"""
        # Try to get from headers
        user_id = request.headers.get("X-User-ID")
        if user_id:
            return user_id
        
        # Try to get from query parameters
        user_id = request.query_params.get("user_id")
        if user_id:
            return user_id
        
        # Try to get from path parameters
        user_id = request.path_params.get("user_id")
        if user_id:
            return user_id
        
        # Default to anonymous
        return "anonymous"
    
    def _extract_request_data(self, request: Request) -> Dict[str, Any]:
        """Extract relevant data from request"""
        data = {
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": dict(request.headers),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent")
        }
        
        # Try to extract body data for POST/PUT requests
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                # Note: This might consume the request body
                # In production, you might want to handle this differently
                body = request.body()
                if body:
                    import json
                    try:
                        data["body"] = json.loads(body)
                    except:
                        data["body"] = body.decode()[:1000]  # Limit body size
            except:
                pass
        
        return data
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log activity"""
        start_time = time.time()
        
        # Skip logging for excluded paths
        if self._should_exclude_path(request.url.path):
            return await call_next(request)
        
        # Extract request data
        request_data = self._extract_request_data(request)
        
        # Get activity mapping
        activity_mapping = self._get_activity_mapping(request.method, request.url.path)
        
        # Extract user ID
        user_id = self._extract_user_id(request)
        
        # Prepare event metadata
        event_metadata = {
            "request_data": request_data,
            "timestamp": start_time
        }
        
        # Log the activity
        try:
            await activity_logger.log_activity(
                event_type=activity_mapping["event_type"],
                event_category=activity_mapping["event_category"],
                event_description=activity_mapping["description_template"],
                user_id=user_id,
                request=request,
                event_metadata=event_metadata
            )
        except Exception as e:
            logger.error(f"Failed to log activity: {e}")
        
        # Process the request
        try:
            response = await call_next(request)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Log response information
            response_metadata = {
                "response_time": response_time,
                "status_code": response.status_code,
                "response_headers": dict(response.headers)
            }
            
            # Update event metadata with response info
            event_metadata.update(response_metadata)
            
            # Log completion
            try:
                await activity_logger.log_activity(
                    event_type=f"{activity_mapping['event_type']}_completed",
                    event_category=activity_mapping["event_category"],
                    event_description=f"{activity_mapping['description_template']} completed",
                    user_id=user_id,
                    request=request,
                    event_metadata=event_metadata
                )
            except Exception as e:
                logger.error(f"Failed to log activity completion: {e}")
            
            return response
            
        except Exception as e:
            # Log error
            error_metadata = {
                "error": str(e),
                "error_type": type(e).__name__,
                "response_time": time.time() - start_time
            }
            event_metadata.update(error_metadata)
            
            try:
                await activity_logger.log_activity(
                    event_type=f"{activity_mapping['event_type']}_error",
                    event_category=activity_mapping["event_category"],
                    event_description=f"{activity_mapping['description_template']} failed",
                    user_id=user_id,
                    request=request,
                    event_metadata=event_metadata
                )
            except Exception as log_error:
                logger.error(f"Failed to log activity error: {log_error}")
            
            # Re-raise the exception
            raise

class ActivityLoggingMiddlewareConfig:
    """Configuration for ActivityLoggingMiddleware"""
    
    def __init__(self):
        self.enabled = True
        self.excluded_paths = set()
        self.include_request_body = False
        self.include_response_body = False
        self.max_body_size = 1000
        self.log_level = "INFO"
    
    def add_excluded_path(self, path: str):
        """Add path to excluded paths"""
        self.excluded_paths.add(path)
    
    def remove_excluded_path(self, path: str):
        """Remove path from excluded paths"""
        self.excluded_paths.discard(path) 