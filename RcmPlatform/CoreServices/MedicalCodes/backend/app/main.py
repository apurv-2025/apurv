# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base
from .routers import search, codes, utils

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="Medical Codes API", 
    version="1.0.0",
    description="A comprehensive API for medical billing code lookup supporting CPT, ICD-10, HCPCS, and Modifier codes."
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search.router)
app.include_router(codes.router)
app.include_router(utils.router)

@app.get("/")
async def root():
    return {
        "message": "Medical Codes API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "search": "/api/search",
            "categories": "/api/categories",
            "stats": "/api/stats",
            "cpt_codes": "/api/cpt/{code}",
            "icd10_codes": "/api/icd10/{code}",
            "hcpcs_codes": "/api/hcpcs/{code}",
            "modifier_codes": "/api/modifier/{modifier}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
