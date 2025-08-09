from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Base
from app.config import settings
from app.routes import auth, users, patients, notes, templates

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mental Health Practice - Progress Notes API",
    description="API for managing progress notes in mental health EHR system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*"]
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(patients.router)
app.include_router(notes.router)
app.include_router(templates.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Mental Health Practice - Progress Notes API"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint."""
    return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
