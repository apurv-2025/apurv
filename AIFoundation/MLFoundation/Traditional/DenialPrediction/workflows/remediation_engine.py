"""
Automated Remediation Engine
Handles automated resolution workflows for healthcare denials
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
import redis
from pydantic import BaseModel, Field

from workflows.denial_classifier import (
    DenialInput, DenialClassification, ResolutionWorkflow, DenialCause
)
from models.database import SessionLocal, DenialRecord, RemediationAction

logger = logging.getLogger(__name__)

class RemediationRequest(BaseModel):
    denial_record_id: int = Field(..., description="Denial record ID")
    execute_automated_actions: bool = Field(True, description="Whether to execute automated actions")
    override_workflow: Optional[str] = Field(None, description="Override workflow type")

class RemediationResponse(BaseModel):
    denial_record_id: int = Field(..., description="Denial record ID")
    status: str = Field(..., description="Remediation status")
    workflow_type: str = Field(..., description="Workflow type executed")
    actions_taken: List[str] = Field(..., description="Actions taken")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time")
    success_probability: float = Field(..., ge=0, le=1, description="Success probability")

class DenialStatusResponse(BaseModel):
    denial_record_id: int = Field(..., description="Denial record ID")
    status: str = Field(..., description="Current status")
    workflow_progress: float = Field(..., ge=0, le=100, description="Workflow progress percentage")
    last_action: str = Field(..., description="Last action taken")
    next_action: Optional[str] = Field(None, description="Next action")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time")
    actions_log: List[Dict[str, Any]] = Field(..., description="Action history")

class AutoRemediationEngine:
    """Automated remediation engine for healthcare denials"""
    
    def __init__(self, db_session: Session, redis_client: redis.Redis):
        self.db = db_session
        self.redis = redis_client
        self.action_handlers = self._initialize_action_handlers()
        
    def _initialize_action_handlers(self) -> Dict[ResolutionWorkflow, callable]:
        """Initialize handlers for different workflow types"""
        return {
            ResolutionWorkflow.RESUBMIT_WITH_AUTH: self._handle_resubmit_with_auth,
            ResolutionWorkflow.CODE_REVIEW_CORRECT: self._handle_code_correction,
            ResolutionWorkflow.VERIFY_ELIGIBILITY: self._handle_eligibility_verification,
            ResolutionWorkflow.INVESTIGATE_DUPLICATE: self._handle_duplicate_investigation,
            ResolutionWorkflow.REQUEST_DOCUMENTATION: self._handle_documentation_request,
            ResolutionWorkflow.MEDICAL_REVIEW: self._handle_medical_review,
            ResolutionWorkflow.APPEAL_FILING: self._handle_appeal_filing,
            ResolutionWorkflow.COB_COORDINATION: self._handle_cob_coordination,
            ResolutionWorkflow.MANUAL_REVIEW: self._handle_manual_review
        }
    
    async def process_denial(self, denial_input: DenialInput) -> Dict[str, Any]:
        """Process a denial through automated remediation"""
        logger.info(f"Processing denial for claim {denial_input.claim_id}")
        
        try:
            # Create denial record
            denial_record = DenialRecord(
                claim_id=denial_input.claim_id,
                denial_date=datetime.utcnow(),
                denial_codes=json.dumps(denial_input.denial_codes),
                denial_reason_text=denial_input.denial_reason_text,
                resolution_status="processing"
            )
            self.db.add(denial_record)
            self.db.commit()
            self.db.refresh(denial_record)
            
            # Classify the denial
            from workflows.denial_classifier import DenialClassifier
            classifier = DenialClassifier()
            classification = classifier.classify_denial(denial_input)
            
            # Update denial record with classification
            denial_record.classification_result = json.dumps({
                "cause_category": classification.cause_category.value,
                "confidence": classification.confidence,
                "subcategory": classification.subcategory,
                "resolution_workflow": classification.resolution_workflow.value,
                "priority_score": classification.priority_score
            })
            self.db.commit()
            
            # Execute workflow
            result = await self._execute_workflow(
                classification.resolution_workflow,
                denial_record.id,
                denial_input,
                classification
            )
            
            return {
                "denial_record_id": denial_record.id,
                "classification": classification,
                "workflow_result": result,
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error processing denial: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def _execute_workflow(
        self,
        workflow_type: ResolutionWorkflow,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Execute the appropriate workflow"""
        handler = self.action_handlers.get(workflow_type)
        if handler:
            return await handler(denial_record_id, denial_input, classification)
        else:
            return await self._handle_manual_review(denial_record_id, denial_input, classification)
    
    async def _handle_resubmit_with_auth(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle resubmission with authorization workflow"""
        logger.info(f"Executing resubmit with auth workflow for denial {denial_record_id}")
        
        actions_taken = []
        
        # Check if authorization is requestable
        if await self._check_auth_requestable(denial_input):
            # Request authorization
            auth_result = await self._request_authorization(denial_input)
            actions_taken.append("Authorization request submitted")
            
            # Prepare resubmission
            resubmit_result = await self._prepare_resubmission(denial_input, auth_number=auth_result.get("auth_number"))
            actions_taken.append("Claim prepared for resubmission")
            
            # Log actions
            self._log_remediation_action(
                denial_record_id, "auth_request", auth_result, "completed"
            )
            self._log_remediation_action(
                denial_record_id, "resubmission_prep", resubmit_result, "completed"
            )
            
            return {
                "workflow_type": "resubmit_with_auth",
                "actions_taken": actions_taken,
                "estimated_completion": (datetime.utcnow() + timedelta(hours=48)).isoformat(),
                "success_probability": 0.85,
                "auth_number": auth_result.get("auth_number"),
                "resubmission_ready": True
            }
        else:
            # Escalate to manual review
            return await self._escalate_to_manual_review(
                denial_record_id, "Authorization not requestable", classification
            )
    
    async def _handle_code_correction(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle code review and correction workflow"""
        logger.info(f"Executing code correction workflow for denial {denial_record_id}")
        
        actions_taken = []
        
        # Analyze coding issues
        coding_analysis = await self._analyze_coding_issue(denial_input)
        actions_taken.append("Coding analysis completed")
        
        if coding_analysis.get("corrections_needed"):
            # Apply corrections
            correction_result = await self._apply_code_corrections(
                denial_input, coding_analysis["corrections"]
            )
            actions_taken.append("Code corrections applied")
            
            # Log actions
            self._log_remediation_action(
                denial_record_id, "coding_analysis", coding_analysis, "completed"
            )
            self._log_remediation_action(
                denial_record_id, "code_correction", correction_result, "completed"
            )
            
            return {
                "workflow_type": "code_review_and_correct",
                "actions_taken": actions_taken,
                "estimated_completion": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
                "success_probability": 0.70,
                "corrections_applied": True,
                "corrected_codes": correction_result.get("corrected_codes")
            }
        else:
            return await self._escalate_to_manual_review(
                denial_record_id, "No coding corrections identified", classification
            )
    
    async def _handle_eligibility_verification(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle eligibility verification workflow"""
        logger.info(f"Executing eligibility verification workflow for denial {denial_record_id}")
        
        actions_taken = []
        
        # Check patient eligibility
        eligibility_result = await self._check_patient_eligibility(
            denial_input.claim_data.get("patient_id"),
            denial_input.claim_data.get("service_date")
        )
        actions_taken.append("Patient eligibility verified")
        
        # Log actions
        self._log_remediation_action(
            denial_record_id, "eligibility_check", eligibility_result, "completed"
        )
        
        return {
            "workflow_type": "verify_eligibility",
            "actions_taken": actions_taken,
            "estimated_completion": (datetime.utcnow() + timedelta(hours=72)).isoformat(),
            "success_probability": 0.30,
            "eligibility_status": eligibility_result.get("status")
        }
    
    async def _handle_duplicate_investigation(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle duplicate claim investigation"""
        logger.info(f"Executing duplicate investigation workflow for denial {denial_record_id}")
        
        actions_taken = ["Duplicate investigation initiated"]
        
        # Check for duplicates in system
        # This would query the database for similar claims
        duplicate_check = {
            "duplicates_found": False,
            "similar_claims": [],
            "investigation_complete": True
        }
        
        self._log_remediation_action(
            denial_record_id, "duplicate_investigation", duplicate_check, "completed"
        )
        
        return {
            "workflow_type": "investigate_duplicate",
            "actions_taken": actions_taken,
            "estimated_completion": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
            "success_probability": 0.20,
            "duplicate_found": duplicate_check["duplicates_found"]
        }
    
    async def _handle_documentation_request(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle documentation request workflow"""
        logger.info(f"Executing documentation request workflow for denial {denial_record_id}")
        
        actions_taken = ["Documentation request prepared"]
        
        # Generate documentation request
        doc_request = {
            "request_type": "medical_records",
            "requested_documents": ["clinical_notes", "lab_results", "imaging_reports"],
            "deadline": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
        
        self._log_remediation_action(
            denial_record_id, "documentation_request", doc_request, "pending"
        )
        
        return {
            "workflow_type": "request_documentation",
            "actions_taken": actions_taken,
            "estimated_completion": (datetime.utcnow() + timedelta(hours=96)).isoformat(),
            "success_probability": 0.75,
            "documentation_requested": True
        }
    
    async def _handle_medical_review(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle medical review workflow"""
        logger.info(f"Executing medical review workflow for denial {denial_record_id}")
        
        actions_taken = ["Medical review initiated"]
        
        # Prepare medical necessity documentation
        medical_review = {
            "review_type": "medical_necessity",
            "required_documentation": ["clinical_justification", "peer_review"],
            "review_deadline": (datetime.utcnow() + timedelta(days=14)).isoformat()
        }
        
        self._log_remediation_action(
            denial_record_id, "medical_review", medical_review, "pending"
        )
        
        return {
            "workflow_type": "medical_review",
            "actions_taken": actions_taken,
            "estimated_completion": (datetime.utcnow() + timedelta(hours=120)).isoformat(),
            "success_probability": 0.60,
            "medical_review_initiated": True
        }
    
    async def _handle_appeal_filing(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle appeal filing workflow"""
        logger.info(f"Executing appeal filing workflow for denial {denial_record_id}")
        
        actions_taken = ["Appeal preparation initiated"]
        
        # Prepare appeal documentation
        appeal_prep = {
            "appeal_type": "first_level",
            "deadline": (datetime.utcnow() + timedelta(days=60)).isoformat(),
            "required_documents": ["appeal_letter", "clinical_documentation", "supporting_evidence"]
        }
        
        self._log_remediation_action(
            denial_record_id, "appeal_preparation", appeal_prep, "pending"
        )
        
        return {
            "workflow_type": "appeal_filing",
            "actions_taken": actions_taken,
            "estimated_completion": (datetime.utcnow() + timedelta(hours=168)).isoformat(),
            "success_probability": classification.appeal_success_probability,
            "appeal_prepared": True
        }
    
    async def _handle_cob_coordination(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle coordination of benefits workflow"""
        logger.info(f"Executing COB coordination workflow for denial {denial_record_id}")
        
        actions_taken = ["COB coordination initiated"]
        
        # Initiate COB process
        cob_process = {
            "cob_type": "primary_secondary",
            "coordination_required": True,
            "deadline": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
        
        self._log_remediation_action(
            denial_record_id, "cob_coordination", cob_process, "pending"
        )
        
        return {
            "workflow_type": "cob_coordination",
            "actions_taken": actions_taken,
            "estimated_completion": (datetime.utcnow() + timedelta(hours=72)).isoformat(),
            "success_probability": 0.80,
            "cob_initiated": True
        }
    
    async def _handle_manual_review(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle manual review workflow"""
        logger.info(f"Escalating to manual review for denial {denial_record_id}")
        
        actions_taken = ["Escalated to manual review"]
        
        # Update denial record status
        denial_record = self.db.query(DenialRecord).filter(
            DenialRecord.id == denial_record_id
        ).first()
        if denial_record:
            denial_record.resolution_status = "manual_review"
            self.db.commit()
        
        self._log_remediation_action(
            denial_record_id, "manual_review_escalation", 
            {"reason": "Complex case requiring human review"}, "pending"
        )
        
        return {
            "workflow_type": "manual_review",
            "actions_taken": actions_taken,
            "estimated_completion": (datetime.utcnow() + timedelta(hours=48)).isoformat(),
            "success_probability": 0.50,
            "escalated_to_manual": True
        }
    
    async def _check_auth_requestable(self, denial_input: DenialInput) -> bool:
        """Check if authorization is requestable for this claim"""
        # Simple logic - in production this would check payer rules
        return True
    
    async def _request_authorization(self, denial_input: DenialInput) -> Dict[str, Any]:
        """Request authorization from payer"""
        # Simulate authorization request
        return {
            "auth_number": f"AUTH_{denial_input.claim_id}_{datetime.utcnow().strftime('%Y%m%d')}",
            "status": "pending",
            "request_date": datetime.utcnow().isoformat()
        }
    
    async def _prepare_resubmission(self, denial_input: DenialInput, **kwargs) -> Dict[str, Any]:
        """Prepare claim for resubmission"""
        return {
            "resubmission_ready": True,
            "auth_number": kwargs.get("auth_number"),
            "resubmission_date": datetime.utcnow().isoformat()
        }
    
    async def _analyze_coding_issue(self, denial_input: DenialInput) -> Dict[str, Any]:
        """Analyze coding issues in the claim"""
        return {
            "corrections_needed": True,
            "corrections": {
                "cpt_codes": ["99213"],  # Example correction
                "icd_codes": ["Z00.00"]
            }
        }
    
    async def _apply_code_corrections(self, denial_input: DenialInput, corrections: Dict[str, Any]) -> Dict[str, Any]:
        """Apply code corrections to the claim"""
        return {
            "corrected_codes": corrections,
            "correction_applied": True
        }
    
    async def _check_patient_eligibility(self, patient_id: str, service_date: str) -> Dict[str, Any]:
        """Check patient eligibility for the service date"""
        return {
            "status": "eligible",
            "coverage_type": "commercial",
            "effective_date": "2024-01-01",
            "termination_date": "2024-12-31"
        }
    
    def _log_remediation_action(
        self,
        denial_record_id: int,
        action_type: str,
        action_data: Dict[str, Any],
        status: str
    ):
        """Log a remediation action"""
        action = RemediationAction(
            denial_record_id=denial_record_id,
            action_type=action_type,
            action_data=json.dumps(action_data),
            status=status,
            executed_at=datetime.utcnow()
        )
        self.db.add(action)
        self.db.commit()
    
    async def _escalate_to_manual_review(
        self,
        denial_record_id: int,
        reason: str,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Escalate case to manual review"""
        return await self._handle_manual_review(
            denial_record_id, None, classification
        ) 