# =============================================================================
# FILE: backend/app/api/routes/enhanced_claims.py
# =============================================================================
"""
Enhanced Claims API Routes with Claims Service Integration

This module provides API endpoints that combine ClaimsProcessing's business logic
with the foundational Claims service's FHIR-based CRUD operations.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging

from ...database.connection import get_db
from ...database.models import Claim as LocalClaim, ClaimStatus, WorkQueue, WorkQueueStatus, WorkQueuePriority
from ...schemas.claims import (
    Claim as ClaimSchema, 
    ClaimCreate, 
    ClaimUpdate,
    WorkQueueAssignment,
    WorkQueueUpdate,
    WorkQueueItem,
    WorkQueueSummary
)
from ...services.enhanced_claim_processor import EnhancedClaimProcessor

logger = logging.getLogger(__name__)
router = APIRouter()

# Dependency to get enhanced claim processor
def get_enhanced_processor(db: Session = Depends(get_db)) -> EnhancedClaimProcessor:
    """Get enhanced claim processor instance"""
    return EnhancedClaimProcessor(db)

@router.post("/", response_model=Dict[str, Any])
async def create_claim(
    claim: ClaimCreate, 
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Create a new claim using enhanced processor
    
    This endpoint creates claims using both local processing and Claims service
    """
    try:
        # Convert Pydantic model to dict
        claim_dict = claim.dict()
        
        # For now, return a message indicating this needs EDI content
        # In a real implementation, you'd generate EDI from structured data
        return {
            "message": "Claim creation from structured data requires EDI generation",
            "note": "Use /upload endpoint for EDI file processing",
            "claim_data": claim_dict
        }
        
    except Exception as e:
        logger.error(f"Error creating claim: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/upload", response_model=Dict[str, Any])
async def upload_claim_file(
    file: UploadFile = File(...),
    payer_id: int = Query(1, description="Payer ID for the claim"),
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Upload and process an EDI claim file using enhanced processor
    
    This endpoint processes EDI files using both local processing and Claims service
    """
    if not file.filename.endswith(('.edi', '.txt', '.x12')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload .edi, .txt, or .x12 files"
        )
    
    try:
        content = await file.read()
        edi_content = content.decode('utf-8')
        
        # Process using enhanced processor
        result = await processor.create_claim_from_edi(edi_content, payer_id)
        
        return {
            "message": "Claim processed successfully",
            "result": result,
            "file_info": {
                "filename": file.filename,
                "size": len(content),
                "payer_id": payer_id
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@router.get("/", response_model=Dict[str, Any])
async def get_claims(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None, description="Filter by claim status"),
    patient_id: Optional[str] = Query(None, description="Filter by patient ID"),
    use_fhir: bool = Query(True, description="Use Claims service (FHIR) if available"),
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Get list of claims with optional filtering
    
    This endpoint can retrieve claims from both local database and Claims service
    """
    try:
        result = await processor.get_claims(
            skip=skip,
            limit=limit,
            status=status,
            patient_id=patient_id,
            use_fhir=use_fhir
        )
        
        return {
            "claims": result['claims'],
            "total": result['total'],
            "source": result['source'],
            "filters": {
                "skip": skip,
                "limit": limit,
                "status": status,
                "patient_id": patient_id,
                "use_fhir": use_fhir
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting claims: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{claim_id}", response_model=Dict[str, Any])
async def get_claim(
    claim_id: str,
    use_fhir: bool = Query(True, description="Use Claims service (FHIR) if available"),
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Get a specific claim by ID
    
    This endpoint can retrieve claims from both local database and Claims service
    """
    try:
        result = await processor.get_claim(claim_id, use_fhir=use_fhir)
        
        return {
            "claim": result['claim'],
            "source": result['source'],
            "fhir_data": result.get('fhir_data'),
            "claim_id": claim_id
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting claim {claim_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{claim_id}", response_model=Dict[str, Any])
async def update_claim(
    claim_id: str,
    claim_update: ClaimUpdate,
    use_fhir: bool = Query(True, description="Update in Claims service (FHIR) if available"),
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Update a claim
    
    This endpoint can update claims in both local database and Claims service
    """
    try:
        update_data = claim_update.dict(exclude_unset=True)
        result = await processor.update_claim(claim_id, update_data, use_fhir=use_fhir)
        
        return {
            "message": "Claim updated successfully",
            "claim": result['claim'],
            "source": result['source'],
            "fhir_data": result.get('fhir_data'),
            "claim_id": claim_id
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating claim {claim_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{claim_id}", response_model=Dict[str, Any])
async def delete_claim(
    claim_id: str,
    use_fhir: bool = Query(True, description="Delete from Claims service (FHIR) if available"),
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Delete a claim
    
    This endpoint can delete claims from both local database and Claims service
    """
    try:
        result = await processor.delete_claim(claim_id, use_fhir=use_fhir)
        
        return {
            "message": "Claim deleted successfully",
            "result": result['result'],
            "source": result['source'],
            "claim_id": claim_id
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting claim {claim_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{claim_id}/validate", response_model=Dict[str, Any])
async def validate_claim(
    claim_id: str,
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Validate a claim using both local and FHIR validation
    
    This endpoint performs comprehensive validation using both systems
    """
    try:
        result = await processor.validate_claim(claim_id)
        
        return {
            "validation_result": result,
            "claim_id": claim_id
        }
        
    except Exception as e:
        logger.error(f"Error validating claim {claim_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{claim_id}/responses", response_model=Dict[str, Any])
async def get_claim_responses(
    claim_id: str,
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Get all responses for a specific claim
    
    This endpoint retrieves claim responses from the Claims service
    """
    try:
        result = await processor.get_claim_responses(claim_id)
        
        return {
            "responses": result['responses'],
            "claim_id": claim_id,
            "total": result['total'],
            "error": result.get('error')
        }
        
    except Exception as e:
        logger.error(f"Error getting claim responses for {claim_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patient/{patient_id}/claims", response_model=Dict[str, Any])
async def get_patient_claims(
    patient_id: str,
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Get all claims for a specific patient
    
    This endpoint retrieves patient claims from both local database and Claims service
    """
    try:
        result = await processor.get_patient_claims(patient_id)
        
        return {
            "claims": result['claims'],
            "patient_id": patient_id,
            "total": result['total'],
            "source": result.get('source'),
            "error": result.get('error')
        }
        
    except Exception as e:
        logger.error(f"Error getting patient claims for {patient_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/claims", response_model=Dict[str, Any])
async def get_claims_stats(
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Get claims statistics from both local and FHIR sources
    
    This endpoint provides comprehensive statistics from both systems
    """
    try:
        result = await processor.get_claims_stats()
        
        return {
            "statistics": result,
            "timestamp": "2024-01-01T00:00:00Z"  # In real implementation, use actual timestamp
        }
        
    except Exception as e:
        logger.error(f"Error getting claims stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health/integration", response_model=Dict[str, Any])
async def health_check_integration(
    processor: EnhancedClaimProcessor = Depends(get_enhanced_processor)
):
    """
    Check health of both local system and Claims service integration
    
    This endpoint provides comprehensive health status
    """
    try:
        result = await processor.health_check()
        
        return {
            "health_status": result,
            "integration": "enhanced_claims_processing"
        }
        
    except Exception as e:
        logger.error(f"Error checking health: {e}")
        return {
            "health_status": {
                "local": {"status": "error", "error": str(e)},
                "fhir": {"status": "unknown"},
                "overall_status": "error"
            },
            "integration": "enhanced_claims_processing"
        }

# Work Queue Operations (Maintained from original ClaimsProcessing)

@router.post("/{claim_id}/assign", response_model=WorkQueueItem)
async def assign_claim_to_work_queue(
    claim_id: str,
    assignment: WorkQueueAssignment,
    assigned_by: str = Query("system", description="User who assigned the claim"),
    db: Session = Depends(get_db)
):
    """
    Assign a claim to the work queue
    
    This maintains the original work queue functionality
    """
    try:
        # Check if claim exists
        claim = db.query(LocalClaim).filter(LocalClaim.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        # Create work queue entry
        work_queue_item = WorkQueue(
            claim_id=claim_id,
            assigned_by=assigned_by,
            assigned_to=assignment.assigned_to,
            status=WorkQueueStatus.ASSIGNED,
            priority=assignment.priority,
            estimated_completion=assignment.estimated_completion,
            work_notes=assignment.work_notes
        )
        
        db.add(work_queue_item)
        db.commit()
        db.refresh(work_queue_item)
        
        return WorkQueueItem(
            id=work_queue_item.id,
            claim_id=work_queue_item.claim_id,
            assigned_by=work_queue_item.assigned_by,
            assigned_to=work_queue_item.assigned_to,
            status=work_queue_item.status,
            priority=work_queue_item.priority,
            estimated_completion=work_queue_item.estimated_completion,
            work_notes=work_queue_item.work_notes,
            created_at=work_queue_item.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning claim to work queue: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/work-queue/", response_model=List[WorkQueueItem])
async def get_work_queue(
    status: Optional[WorkQueueStatus] = Query(None),
    assigned_to: Optional[str] = Query(None),
    priority: Optional[WorkQueuePriority] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get work queue items with optional filtering
    
    This maintains the original work queue functionality
    """
    try:
        query = db.query(WorkQueue)
        
        if status:
            query = query.filter(WorkQueue.status == status)
        if assigned_to:
            query = query.filter(WorkQueue.assigned_to == assigned_to)
        if priority:
            query = query.filter(WorkQueue.priority == priority)
        
        work_queue_items = query.offset(skip).limit(limit).all()
        
        return [
            WorkQueueItem(
                id=item.id,
                claim_id=item.claim_id,
                assigned_by=item.assigned_by,
                assigned_to=item.assigned_to,
                status=item.status,
                priority=item.priority,
                estimated_completion=item.estimated_completion,
                work_notes=item.work_notes,
                created_at=item.created_at
            )
            for item in work_queue_items
        ]
        
    except Exception as e:
        logger.error(f"Error getting work queue: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/work-queue/summary", response_model=WorkQueueSummary)
async def get_work_queue_summary(db: Session = Depends(get_db)):
    """
    Get work queue summary statistics
    
    This maintains the original work queue functionality
    """
    try:
        total_items = db.query(WorkQueue).count()
        pending_items = db.query(WorkQueue).filter(WorkQueue.status == WorkQueueStatus.PENDING).count()
        in_progress_items = db.query(WorkQueue).filter(WorkQueue.status == WorkQueueStatus.IN_PROGRESS).count()
        completed_items = db.query(WorkQueue).filter(WorkQueue.status == WorkQueueStatus.COMPLETED).count()
        
        return WorkQueueSummary(
            total_items=total_items,
            pending_items=pending_items,
            in_progress_items=in_progress_items,
            completed_items=completed_items
        )
        
    except Exception as e:
        logger.error(f"Error getting work queue summary: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 