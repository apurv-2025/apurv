from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AI Agent Builder API")
    yield
    # Shutdown
    logger.info("Shutting down AI Agent Builder API")

app = FastAPI(
    title="AI Agent Builder API",
    description="""
    AI Agent Builder API for Small Medical Practices
    
    This API enables medical practices to create, configure, and deploy AI agents
    that assist with administrative workflows while maintaining HIPAA compliance.
    
    ## Features
    
    * **User Management**: Secure authentication and authorization
    * **Agent Management**: Create and configure AI agents for different roles
    * **Knowledge Base**: Upload and manage training documents
    * **Chat Interface**: Test and interact with agents
    * **Audit Logging**: Complete audit trail for compliance
    * **HIPAA Compliance**: Built-in privacy and security features
    
    ## Authentication
    
    All endpoints except registration and login require a Bearer token.
    Get a token by calling the `/auth/token` endpoint with valid credentials.
    
    ## Rate Limiting
    
    API calls are rate-limited to prevent abuse. Contact support if you need higher limits.
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@aiagentbuilder.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "yourdomain.com", "testserver"]
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    return response

# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    """
    Detailed health check including database connectivity.
    """
    try:
        # Test database connection
        from models.database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": time.time(),
                "database": "disconnected",
                "error": str(e)
            }
        )

# Performance monitoring
@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    """
    Basic application metrics for monitoring.
    """
    # In production, you might use Prometheus or similar
    return {
        "uptime": time.time(),
        "requests_total": "metrics_not_implemented",
        "active_agents": "metrics_not_implemented",
        "memory_usage": "metrics_not_implemented"
    }

# Include routers
from routers import auth, agents, knowledge

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "path": str(request.url)}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
