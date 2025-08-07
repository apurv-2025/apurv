# =============================================================================
# FILE: backend/app/api/routes/claims.py
# =============================================================================
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from ...database.connection import get_db
from ...database.models import Claim, ClaimStatus, WorkQueue, WorkQueueStatus, WorkQueuePriority
from ...schemas.claims import (
    Claim as ClaimSchema, 
    ClaimCreate, 
    ClaimUpdate,
    WorkQueueAssignment,
    WorkQueueUpdate,
    WorkQueueItem,
    WorkQueueSummary
)
from ...services.claim_processor import ClaimProcessor

router = APIRouter()

@router.post("/", response_model=ClaimSchema)
def create_claim(claim: ClaimCreate, db: Session = Depends(get_db)):
    """Create a new claim"""
    processor = ClaimProcessor(db)
    
    # Convert Pydantic model to dict for processing
    claim_dict = claim.dict()
    
    # This is a simplified version - in real implementation,
    # you'd need to generate EDI from the structured data
    return {"message": "Claim creation from structured data not yet implemented"}

@router.post("/upload", response_model=ClaimSchema)
async def upload_claim_file(
    file: UploadFile = File(...),
    payer_id: int = 1,
    db: Session = Depends(get_db)
):
    """Upload and process an EDI claim file"""
    
    if not file.filename.endswith(('.edi', '.txt', '.x12')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload .edi, .txt, or .x12 files")
    
    try:
        content = await file.read()
        edi_content = content.decode('utf-8')
        
        processor = ClaimProcessor(db)
        claim = processor.create_claim_from_edi(edi_content, payer_id)
        
        return claim
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@router.get("/", response_model=List[ClaimSchema])
def get_claims(
    skip: int = 0,
    limit: int = 100,
    status: ClaimStatus = None,
    db: Session = Depends(get_db)
):
    """Get list of claims with optional filtering"""
    
    query = db.query(Claim)
    
    if status:
        query = query.filter(Claim.status == status)
    
    claims = query.offset(skip).limit(limit).all()
    return claims

@router.get("/{claim_id}", response_model=ClaimSchema)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    """Get a specific claim by ID"""
    
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    return claim

@router.patch("/{claim_id}", response_model=ClaimSchema)
def update_claim(claim_id: int, claim_update: ClaimUpdate, db: Session = Depends(get_db)):
    """Update a claim"""
    
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    for field, value in claim_update.dict(exclude_unset=True).items():
        setattr(claim, field, value)
    
    db.commit()
    db.refresh(claim)
    
    return claim

@router.post("/{claim_id}/validate")
def validate_claim(claim_id: int, db: Session = Depends(get_db)):
    """Validate a claim"""
    
    processor = ClaimProcessor(db)
    
    try:
        result = processor.validate_claim(claim_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{claim_id}/submit")
def submit_claim(claim_id: int, db: Session = Depends(get_db)):
    """Submit a validated claim to payer"""
    
    processor = ClaimProcessor(db)
    
    try:
        # This would implement actual submission logic
        # For now, just update status
        claim = db.query(Claim).filter(Claim.id == claim_id).first()
        if not claim:
            raise HTTPException(status_code=404, detail="Claim not found")
        
        if claim.status != ClaimStatus.VALIDATED:
            raise HTTPException(status_code=400, detail="Claim must be validated before submission")
        
        claim.status = ClaimStatus.SENT
        db.commit()
        
        return {"success": True, "message": "Claim submitted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Work Queue Endpoints
@router.post("/{claim_id}/assign", response_model=WorkQueueItem)
def assign_claim_to_work_queue(
    claim_id: int, 
    assignment: WorkQueueAssignment, 
    assigned_by: str = "system",  # In real app, get from auth
    db: Session = Depends(get_db)
):
    """Assign a claim to the work queue for processing"""
    
    # Check if claim exists
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    # Check if already in work queue
    existing_assignment = db.query(WorkQueue).filter(
        WorkQueue.claim_id == claim_id,
        WorkQueue.status.in_([WorkQueueStatus.PENDING, WorkQueueStatus.ASSIGNED, WorkQueueStatus.IN_PROGRESS])
    ).first()
    
    if existing_assignment:
        raise HTTPException(status_code=400, detail="Claim is already in work queue")
    
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
    
    # If assigned to an AI agent, create an agent task
    if assignment.assigned_to.startswith('agent-') or assignment.assigned_to.startswith('ai-'):
        try:
            from ...agent.manager import get_agent_manager
            from ...schemas.agent import AgentRequest, TaskType
            
            agent_manager = get_agent_manager()
            
            # Create agent task for claim processing
            agent_request = AgentRequest(
                task_type=TaskType.PROCESS_CLAIM,
                user_id=assigned_by,
                task_description=f"Process claim {claim_id} from work queue",
                context={
                    "claim_id": claim_id,
                    "work_queue_id": work_queue_item.id,
                    "priority": assignment.priority.value,
                    "work_notes": assignment.work_notes
                },
                claim_id=claim_id,
                priority=5  # Default priority
            )
            
            # Process the agent task asynchronously
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            agent_response = loop.run_until_complete(agent_manager.process_task(agent_request.dict()))
            loop.close()
            
            # Update work queue with agent task info
            work_queue_item.action_taken = f"Agent task created: {agent_response.get('task_id', 'unknown')}"
            work_queue_item.result_summary = agent_response.get('message', 'Agent task initiated')
            
        except Exception as e:
            # Log error but don't fail the assignment
            work_queue_item.work_notes = f"{assignment.work_notes or ''}\n[Agent task creation failed: {str(e)}]"
            print(f"Error creating agent task: {e}")
    
    # Update claim work queue status
    claim.work_queue_status = WorkQueueStatus.ASSIGNED
    claim.assigned_to = assignment.assigned_to
    claim.assigned_at = work_queue_item.assigned_at
    claim.work_queue_priority = assignment.priority
    claim.work_notes = assignment.work_notes
    
    db.add(work_queue_item)
    db.commit()
    db.refresh(work_queue_item)
    
    # Return enriched work queue item
    return WorkQueueItem(
        id=work_queue_item.id,
        claim_id=claim_id,
        claim_number=claim.claim_number,
        patient_name=f"{claim.patient_first_name} {claim.patient_last_name}",
        claim_type=claim.claim_type,
        claim_status=claim.status,
        assigned_by=assigned_by,
        assigned_to=assignment.assigned_to,
        assigned_at=work_queue_item.assigned_at,
        status=work_queue_item.status,
        priority=work_queue_item.priority,
        estimated_completion=work_queue_item.estimated_completion,
        actual_completion=work_queue_item.actual_completion,
        work_notes=work_queue_item.work_notes,
        action_taken=work_queue_item.action_taken,
        result_summary=work_queue_item.result_summary,
                 created_at=work_queue_item.created_at,
         updated_at=work_queue_item.updated_at
     )

@router.get("/work-queue/available-agents")
def get_available_agents():
    """Get list of available AI agents for assignment"""
    
    # In a real implementation, this would query the agent registry
    # For now, return a static list of available agents
    available_agents = [
        {
            "id": "Claims-Agent",
            "name": "Claims Processing Agent",
            "description": "Specialized in processing and validating claims",
            "capabilities": ["process_claim", "validate_claim", "analyze_rejection"],
            "status": "available"
        },
        {
            "id": "agent-002", 
            "name": "Payment Reconciliation Agent",
            "description": "Handles payment reconciliation and adjustments",
            "capabilities": ["reconcile_payment", "process_claim"],
            "status": "available"
        },
        {
            "id": "agent-003",
            "name": "Document Analysis Agent", 
            "description": "Analyzes claim documents and extracts information",
            "capabilities": ["process_claim", "generate_report"],
            "status": "available"
        }
    ]
    
    return {"agents": available_agents}

@router.get("/work-queue/", response_model=List[WorkQueueItem])
def get_work_queue(
    status: WorkQueueStatus = None,
    assigned_to: str = None,
    priority: WorkQueuePriority = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get work queue items with optional filtering"""
    
    query = db.query(WorkQueue).join(Claim)
    
    if status:
        query = query.filter(WorkQueue.status == status)
    if assigned_to:
        query = query.filter(WorkQueue.assigned_to == assigned_to)
    if priority:
        query = query.filter(WorkQueue.priority == priority)
    
    work_queue_items = query.offset(skip).limit(limit).all()
    
    # Convert to response format
    result = []
    for item in work_queue_items:
        claim = item.claim
        result.append(WorkQueueItem(
            id=item.id,
            claim_id=claim.id,
            claim_number=claim.claim_number,
            patient_name=f"{claim.patient_first_name} {claim.patient_last_name}",
            claim_type=claim.claim_type,
            claim_status=claim.status,
            assigned_by=item.assigned_by,
            assigned_to=item.assigned_to,
            assigned_at=item.assigned_at,
            status=item.status,
            priority=item.priority,
            estimated_completion=item.estimated_completion,
            actual_completion=item.actual_completion,
            work_notes=item.work_notes,
            action_taken=item.action_taken,
            result_summary=item.result_summary,
            created_at=item.created_at,
            updated_at=item.updated_at
        ))
    
    return result

@router.post("/work-queue/{work_queue_id}/assign-to-agent")
def assign_work_queue_to_agent(
    work_queue_id: int,
    agent_id: str = "Claims-Agent",
    task_type: str = "process_claim",
    assigned_by: str = "system",
    db: Session = Depends(get_db)
):
    """Assign a work queue item to an AI agent for processing"""
    
    # Get work queue item
    work_queue_item = db.query(WorkQueue).filter(WorkQueue.id == work_queue_id).first()
    if not work_queue_item:
        raise HTTPException(status_code=404, detail="Work queue item not found")
    
    # Check if already assigned to an agent
    if work_queue_item.assigned_to.startswith('agent-') or work_queue_item.assigned_to.startswith('ai-'):
        raise HTTPException(status_code=400, detail="Work queue item is already assigned to an agent")
    
    try:
        from ...agent.manager import get_agent_manager
        from ...schemas.agent import AgentRequest, TaskType
        
        agent_manager = get_agent_manager()
        
        # Create agent task
        agent_request = AgentRequest(
            task_type=TaskType(task_type),
            user_id=assigned_by,
            task_description=f"Process work queue item {work_queue_id} for claim {work_queue_item.claim_id}",
            context={
                "claim_id": work_queue_item.claim_id,
                "work_queue_id": work_queue_id,
                "priority": work_queue_item.priority.value,
                "work_notes": work_queue_item.work_notes
            },
            claim_id=work_queue_item.claim_id,
            priority=5
        )
        
        # Process the agent task
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        agent_response = loop.run_until_complete(agent_manager.process_task(agent_request.dict()))
        loop.close()
        
        # Update work queue item
        work_queue_item.assigned_to = agent_id
        work_queue_item.status = WorkQueueStatus.IN_PROGRESS
        work_queue_item.action_taken = f"Assigned to agent {agent_id}. Task ID: {agent_response.get('task_id', 'unknown')}"
        work_queue_item.result_summary = agent_response.get('message', 'Agent task initiated')
        
        # Update claim status
        claim = db.query(Claim).filter(Claim.id == work_queue_item.claim_id).first()
        if claim:
            claim.work_queue_status = WorkQueueStatus.IN_PROGRESS
            claim.assigned_to = agent_id
        
        db.commit()
        
        return {
            "success": True,
            "work_queue_id": work_queue_id,
            "agent_task_id": agent_response.get('task_id'),
            "message": "Successfully assigned to agent",
            "agent_response": agent_response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning to agent: {str(e)}")

@router.get("/work-queue/summary", response_model=WorkQueueSummary)
def get_work_queue_summary(db: Session = Depends(get_db)):
    """Get work queue summary statistics"""
    
    # Get counts by status
    total_items = db.query(WorkQueue).count()
    pending = db.query(WorkQueue).filter(WorkQueue.status == WorkQueueStatus.PENDING).count()
    assigned = db.query(WorkQueue).filter(WorkQueue.status == WorkQueueStatus.ASSIGNED).count()
    in_progress = db.query(WorkQueue).filter(WorkQueue.status == WorkQueueStatus.IN_PROGRESS).count()
    completed = db.query(WorkQueue).filter(WorkQueue.status == WorkQueueStatus.COMPLETED).count()
    failed = db.query(WorkQueue).filter(WorkQueue.status == WorkQueueStatus.FAILED).count()
    cancelled = db.query(WorkQueue).filter(WorkQueue.status == WorkQueueStatus.CANCELLED).count()
    
    # Get counts by priority
    by_priority = {}
    for priority in WorkQueuePriority:
        count = db.query(WorkQueue).filter(WorkQueue.priority == priority).count()
        by_priority[priority.value] = count
    
    # Get counts by assignee
    by_assignee = {}
    assignees = db.query(WorkQueue.assigned_to).distinct().all()
    for assignee in assignees:
        count = db.query(WorkQueue).filter(WorkQueue.assigned_to == assignee[0]).count()
        by_assignee[assignee[0]] = count
    
    return WorkQueueSummary(
        total_items=total_items,
        pending=pending,
        assigned=assigned,
        in_progress=in_progress,
        completed=completed,
        failed=failed,
        cancelled=cancelled,
        by_priority=by_priority,
        by_assignee=by_assignee
    )

@router.patch("/work-queue/{work_queue_id}", response_model=WorkQueueItem)
def update_work_queue_item(
    work_queue_id: int,
    update: WorkQueueUpdate,
    db: Session = Depends(get_db)
):
    """Update a work queue item"""
    
    work_queue_item = db.query(WorkQueue).filter(WorkQueue.id == work_queue_id).first()
    if not work_queue_item:
        raise HTTPException(status_code=404, detail="Work queue item not found")
    
    # Update work queue item
    for field, value in update.dict(exclude_unset=True).items():
        setattr(work_queue_item, field, value)
    
    # Update claim work queue status if status changed
    if update.status:
        claim = db.query(Claim).filter(Claim.id == work_queue_item.claim_id).first()
        if claim:
            claim.work_queue_status = update.status
            if update.status == WorkQueueStatus.COMPLETED:
                work_queue_item.actual_completion = work_queue_item.updated_at
    
    db.commit()
    db.refresh(work_queue_item)
    
    # Return enriched response
    claim = work_queue_item.claim
    return WorkQueueItem(
        id=work_queue_item.id,
        claim_id=claim.id,
        claim_number=claim.claim_number,
        patient_name=f"{claim.patient_first_name} {claim.patient_last_name}",
        claim_type=claim.claim_type,
        claim_status=claim.status,
        assigned_by=work_queue_item.assigned_by,
        assigned_to=work_queue_item.assigned_to,
        assigned_at=work_queue_item.assigned_at,
        status=work_queue_item.status,
        priority=work_queue_item.priority,
        estimated_completion=work_queue_item.estimated_completion,
        actual_completion=work_queue_item.actual_completion,
        work_notes=work_queue_item.work_notes,
        action_taken=work_queue_item.action_taken,
        result_summary=work_queue_item.result_summary,
        created_at=work_queue_item.created_at,
        updated_at=work_queue_item.updated_at
    )
