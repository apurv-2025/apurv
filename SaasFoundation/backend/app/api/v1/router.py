from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, notifications,organizations, subscriptions, pricing,invoices,payments,health

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/user", tags=["users"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(organizations.router, prefix="/invitations", tags=["invitations"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["pricing"])
api_router.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
