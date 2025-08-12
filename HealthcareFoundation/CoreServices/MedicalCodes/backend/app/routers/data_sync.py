#!/usr/bin/env python3
"""
Data Synchronization API Endpoints
Provides endpoints for fetching and integrating data from official medical coding sources
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
import asyncio
import json
from datetime import datetime

from ..database import get_db
from ..services.data_sync_service import data_sync_service
from ..services.specialized_scrapers import official_data_scraper
from ..services.enhanced_scrapers import enhanced_scraper
from ..schemas import SyncStatusResponse, SyncResultResponse, ScrapedDataResponse

router = APIRouter(prefix="/api/sync", tags=["data-sync"])

# Background task to run data synchronization
async def run_data_sync_task():
    """Background task for data synchronization"""
    try:
        results = await data_sync_service.sync_all_data()
        return results
    except Exception as e:
        return {"error": str(e)}

@router.get("/status", response_model=SyncStatusResponse)
async def get_sync_status():
    """Get the current status of data synchronization"""
    try:
        status = data_sync_service.get_sync_status()
        return SyncStatusResponse(
            status="ready",
            last_sync=status['last_sync'],
            sources=status['sources'],
            message="Data synchronization service is ready"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sync status: {str(e)}")

@router.post("/start", response_model=SyncResultResponse)
async def start_data_sync(background_tasks: BackgroundTasks):
    """Start data synchronization from official sources"""
    try:
        # Add the sync task to background tasks
        background_tasks.add_task(run_data_sync_task)
        
        return SyncResultResponse(
            success=True,
            message="Data synchronization started in background",
            task_id=f"sync_{datetime.now().isoformat()}",
            status="running"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting data sync: {str(e)}")

@router.post("/scrape", response_model=ScrapedDataResponse)
async def scrape_official_data():
    """Scrape data from official sources without updating database"""
    try:
        # Scrape data from all official sources
        scraped_data = official_data_scraper.scrape_all_official_data()
        
        # Save scraped data to file
        filename = official_data_scraper.save_scraped_data(scraped_data)
        
        # Count total codes
        total_codes = (
            len(scraped_data.get('cpt_codes', [])) +
            len(scraped_data.get('icd10_codes', [])) +
            len(scraped_data.get('hcpcs_codes', []))
        )
        
        return ScrapedDataResponse(
            success=True,
            message=f"Successfully scraped {total_codes} codes from official sources",
            filename=filename,
            cpt_codes_count=len(scraped_data.get('cpt_codes', [])),
            icd10_codes_count=len(scraped_data.get('icd10_codes', [])),
            hcpcs_codes_count=len(scraped_data.get('hcpcs_codes', [])),
            total_codes=total_codes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping official data: {str(e)}")

# NEW: Enhanced endpoints with database integration
@router.post("/scrape-to-database")
async def scrape_and_save_to_database(
    save_to_db: bool = Query(True, description="Save scraped data to database"),
    save_to_file: bool = Query(False, description="Also save scraped data to JSON file")
):
    """Scrape data from all official sources and save to database"""
    try:
        results = await enhanced_scraper.scrape_and_save_to_database(
            save_to_db=save_to_db,
            save_to_file=save_to_file
        )
        
        return {
            "success": True,
            "message": f"Scraping completed - DB: {results['database_saved']}, File: {results['file_saved']}",
            "database_saved": results['database_saved'],
            "file_saved": results['file_saved'],
            "filename": results['filename'],
            "database_counts": results['db_counts'],
            "scraped_counts": {
                "cpt": len(results['scraped_data'].get('cpt_codes', [])),
                "icd10": len(results['scraped_data'].get('icd10_codes', [])),
                "hcpcs": len(results['scraped_data'].get('hcpcs_codes', []))
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping and saving to database: {str(e)}")

@router.post("/scrape-cpt-to-database")
async def scrape_cpt_to_database():
    """Scrape CPT codes from AMA and save directly to database"""
    try:
        results = await enhanced_scraper.scrape_cpt_to_database()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping CPT to database: {str(e)}")

@router.post("/scrape-icd10-to-database")
async def scrape_icd10_to_database():
    """Scrape ICD-10 codes from CMS and save directly to database"""
    try:
        results = await enhanced_scraper.scrape_icd10_to_database()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping ICD-10 to database: {str(e)}")

@router.post("/scrape-hcpcs-to-database")
async def scrape_hcpcs_to_database():
    """Scrape HCPCS codes from CMS and save directly to database"""
    try:
        results = await enhanced_scraper.scrape_hcpcs_to_database()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping HCPCS to database: {str(e)}")

@router.post("/scrape-cpt")
async def scrape_cpt_data():
    """Scrape CPT codes from AMA website"""
    try:
        cpt_codes = official_data_scraper.cpt_scraper.scrape_cpt_codes()
        
        return {
            "success": True,
            "message": f"Successfully scraped {len(cpt_codes)} CPT codes from AMA",
            "cpt_codes_count": len(cpt_codes),
            "source": "AMA CPT",
            "url": "https://www.ama-assn.org/practice-management/cpt"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping CPT data: {str(e)}")

@router.post("/scrape-icd10")
async def scrape_icd10_data():
    """Scrape ICD-10 codes from CMS website"""
    try:
        icd10_codes = official_data_scraper.icd10_scraper.scrape_icd10_codes()
        
        return {
            "success": True,
            "message": f"Successfully scraped {len(icd10_codes)} ICD-10 codes from CMS",
            "icd10_codes_count": len(icd10_codes),
            "source": "CMS ICD-10",
            "url": "https://www.cms.gov/medicare/coding-billing/icd-10-codes"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping ICD-10 data: {str(e)}")

@router.post("/scrape-hcpcs")
async def scrape_hcpcs_data():
    """Scrape HCPCS codes from CMS website"""
    try:
        hcpcs_codes = official_data_scraper.hcpcs_scraper.scrape_hcpcs_codes()
        
        return {
            "success": True,
            "message": f"Successfully scraped {len(hcpcs_codes)} HCPCS codes from CMS",
            "hcpcs_codes_count": len(hcpcs_codes),
            "source": "CMS HCPCS",
            "url": "https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping HCPCS data: {str(e)}")

@router.get("/sources")
async def get_official_sources():
    """Get information about official data sources"""
    sources = {
        "cpt": {
            "name": "AMA CPT",
            "url": "https://www.ama-assn.org/practice-management/cpt",
            "description": "Current Procedural Terminology codes maintained by American Medical Association",
            "type": "CPT Codes",
            "maintainer": "American Medical Association (AMA)"
        },
        "icd10": {
            "name": "CMS ICD-10",
            "url": "https://www.cms.gov/medicare/coding-billing/icd-10-codes",
            "description": "International Classification of Diseases, 10th Revision codes",
            "type": "ICD-10 Codes",
            "maintainer": "Centers for Medicare & Medicaid Services (CMS)"
        },
        "hcpcs": {
            "name": "CMS HCPCS",
            "url": "https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system",
            "description": "Healthcare Common Procedure Coding System Level II codes",
            "type": "HCPCS Codes",
            "maintainer": "Centers for Medicare & Medicaid Services (CMS)"
        }
    }
    
    return {
        "sources": sources,
        "total_sources": len(sources),
        "last_updated": datetime.now().isoformat()
    }

@router.get("/health")
async def sync_health_check():
    """Health check for data synchronization service"""
    try:
        # Test basic connectivity to official sources
        sources_status = {}
        
        # Test AMA CPT
        try:
            response = official_data_scraper.cpt_scraper.session.get(
                "https://www.ama-assn.org/practice-management/cpt", 
                timeout=10
            )
            sources_status["ama_cpt"] = "accessible" if response.status_code == 200 else "unavailable"
        except:
            sources_status["ama_cpt"] = "unreachable"
        
        # Test CMS ICD-10
        try:
            response = official_data_scraper.icd10_scraper.session.get(
                "https://www.cms.gov/medicare/coding-billing/icd-10-codes", 
                timeout=10
            )
            sources_status["cms_icd10"] = "accessible" if response.status_code == 200 else "unavailable"
        except:
            sources_status["cms_icd10"] = "unreachable"
        
        # Test CMS HCPCS
        try:
            response = official_data_scraper.hcpcs_scraper.session.get(
                "https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system", 
                timeout=10
            )
            sources_status["cms_hcpcs"] = "accessible" if response.status_code == 200 else "unavailable"
        except:
            sources_status["cms_hcpcs"] = "unreachable"
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "sources_status": sources_status,
            "service": "data-sync"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}") 