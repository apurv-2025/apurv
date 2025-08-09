"""
Middleware package for SaaSFoundation
"""

from .activity_logging import ActivityLoggingMiddleware, ActivityLoggingMiddlewareConfig

__all__ = ["ActivityLoggingMiddleware", "ActivityLoggingMiddlewareConfig"] 