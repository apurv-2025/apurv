#!/usr/bin/env python3
"""
Comprehensive Code Search API Router
Provides endpoints for searching the comprehensive medical code database
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from ..services.comprehensive_code_database import comprehensive_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/comprehensive", tags=["Comprehensive Code Search"])

@router.get("/search")
async def search_comprehensive_codes(
    query: Optional[str] = Query("", description="Search query for medical codes"),
    code_types: Optional[str] = Query(None, description="Comma-separated list of code types to search (cpt,icd10,hcpcs)"),
    specialty: Optional[str] = Query(None, description="Filter by medical specialty"),
    category: Optional[str] = Query(None, description="Filter by code category"),
    section: Optional[str] = Query(None, description="Filter by CPT section"),
    subsection: Optional[str] = Query(None, description="Filter by CPT subsection"),
    chapter: Optional[str] = Query(None, description="Filter by ICD-10 chapter"),
    level: Optional[str] = Query(None, description="Filter by HCPCS level")
):
    """
    Search comprehensive medical code database with advanced filtering
    
    This endpoint searches through a comprehensive database of medical codes
    including CPT, ICD-10, and HCPCS codes for all specialties with advanced filtering options.
    """
    try:
        # Parse code types
        types_list = None
        if code_types:
            types_list = [t.strip().lower() for t in code_types.split(',')]
        
        # Build filter criteria
        filters = {}
        if specialty:
            filters['specialty'] = specialty
        if category:
            filters['category'] = category
        if section:
            filters['section'] = section
        if subsection:
            filters['subsection'] = subsection
        if chapter:
            filters['chapter'] = chapter
        if level:
            filters['level'] = level
        
        # Search comprehensive database with filters
        results = comprehensive_db.search_comprehensive_codes_with_filters(query, types_list, filters)
        
        return {
            "success": True,
            "query": query,
            "code_types_searched": types_list or ["cpt", "icd10", "hcpcs"],
            "filters_applied": filters,
            "results": results,
            "total_results": results["total_results"]
        }
        
    except Exception as e:
        logger.error(f"Error in comprehensive search: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@router.get("/stats")
async def get_comprehensive_stats():
    """
    Get comprehensive database statistics
    
    Returns information about the comprehensive code database including
    total codes, last update time, and cache status.
    """
    try:
        stats = comprehensive_db.get_database_stats()
        
        return {
            "success": True,
            "database_stats": stats,
            "data_sources": comprehensive_db.data_sources
        }
        
    except Exception as e:
        logger.error(f"Error getting comprehensive stats: {e}")
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")

@router.post("/load")
async def load_comprehensive_database():
    """
    Load comprehensive medical code database
    
    This endpoint loads the comprehensive database into local cache.
    This should be called once to initialize the database.
    """
    try:
        logger.info("Loading comprehensive database...")
        results = comprehensive_db.load_comprehensive_database()
        
        return {
            "success": True,
            "message": "Comprehensive database loaded successfully",
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error loading comprehensive database: {e}")
        raise HTTPException(status_code=500, detail=f"Database loading error: {str(e)}")

@router.get("/specialties")
async def get_available_specialties():
    """
    Get available medical specialties
    
    Returns a list of medical specialties available in the comprehensive database.
    """
    try:
        specialties = {
            "cpt_specialties": list(comprehensive_db.cpt_specialties.keys()),
            "mental_health_chapters": list(comprehensive_db.icd10_mental_health.keys()),
            "sample_specialties": [
                "Psychiatry", "Primary Care", "Surgery", "Orthopedics", "Cardiology",
                "Gastroenterology", "Radiology", "Pathology", "Pulmonology", "Dermatology",
                "Rheumatology", "Urology", "Obstetrics", "Neonatology", "Emergency Medicine",
                "Infectious Disease", "Oncology", "Hematology", "Endocrinology", "Neurology",
                "Ophthalmology"
            ]
        }
        
        return {
            "success": True,
            "specialties": specialties
        }
        
    except Exception as e:
        logger.error(f"Error getting specialties: {e}")
        raise HTTPException(status_code=500, detail=f"Specialties error: {str(e)}")

@router.get("/search/mental-health")
async def search_mental_health_codes(
    query: str = Query(..., description="Search query for mental health codes")
):
    """
    Search mental health specific codes
    
    This endpoint searches specifically for mental health related codes
    including psychiatry CPT codes, mental health ICD-10 codes, and behavioral health HCPCS codes.
    """
    try:
        # Search with mental health focus
        results = comprehensive_db.search_comprehensive_codes(query, ["cpt", "icd10", "hcpcs"])
        
        # Filter for mental health related codes
        mental_health_results = {
            "cpt_codes": [code for code in results["cpt_codes"] if code.get("specialty") == "Psychiatry"],
            "icd10_codes": [code for code in results["icd10_codes"] if code.get("specialty") == "Psychiatry"],
            "hcpcs_codes": [code for code in results["hcpcs_codes"] if code.get("specialty") == "Psychiatry"],
            "total_results": 0
        }
        
        mental_health_results["total_results"] = (
            len(mental_health_results["cpt_codes"]) + 
            len(mental_health_results["icd10_codes"]) + 
            len(mental_health_results["hcpcs_codes"])
        )
        
        return {
            "success": True,
            "query": query,
            "search_type": "mental_health",
            "results": mental_health_results,
            "total_results": mental_health_results["total_results"]
        }
        
    except Exception as e:
        logger.error(f"Error in mental health search: {e}")
        raise HTTPException(status_code=500, detail=f"Mental health search error: {str(e)}")

@router.get("/health")
async def comprehensive_health_check():
    """
    Health check for comprehensive database
    
    Returns the health status of the comprehensive code database.
    """
    try:
        stats = comprehensive_db.get_database_stats()
        
        health_status = "healthy" if stats["cache_status"] == "loaded" else "not_loaded"
        
        return {
            "status": health_status,
            "database_stats": stats,
            "cache_status": stats["cache_status"],
            "total_codes": stats["total_codes"]
        }
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return {
            "status": "error",
            "error": str(e)
        } 