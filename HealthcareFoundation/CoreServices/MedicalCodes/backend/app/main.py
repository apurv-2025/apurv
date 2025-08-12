# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base
from .routers import search, codes, utils, data_sync, comprehensive_search, export, fhir_api

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="Medical Codes API", 
    version="1.0.0",
    description="A comprehensive API for medical billing code lookup supporting CPT, ICD-10, HCPCS, and Modifier codes with official data synchronization."
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3003"],  # React dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search.router)
app.include_router(codes.router)
app.include_router(utils.router)
app.include_router(data_sync.router)
app.include_router(comprehensive_search.router)
app.include_router(export.router)
app.include_router(fhir_api.router)

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
            "modifier_codes": "/api/modifier/{modifier}",
            "data_sync": "/api/sync",
            "comprehensive_search": "/api/comprehensive",
            "export": "/api/export",
            "fhir": {
                "metadata": "/fhir/metadata",
                "codesystems": "/fhir/CodeSystem",
                "valuesets": "/fhir/ValueSet",
                "conceptmaps": "/fhir/ConceptMap",
                "lookup": "/fhir/CodeSystem/{id}/$lookup",
                "expand": "/fhir/ValueSet/{id}/$expand"
            },
            "official_sources": {
                "ama_cpt": "https://www.ama-assn.org/practice-management/cpt",
                "cms_icd10": "https://www.cms.gov/medicare/coding-billing/icd-10-codes",
                "cms_hcpcs": "https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system"
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
