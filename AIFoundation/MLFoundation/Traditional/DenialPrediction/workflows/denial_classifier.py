"""
Denial Classification System
NLP-based classification of healthcare claim denials
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# For demo purposes, we'll use simpler NLP approaches
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

logger = logging.getLogger(__name__)

class DenialCause(Enum):
    MISSING_AUTHORIZATION = "missing_auth"
    INVALID_CODE = "invalid_code"
    ELIGIBILITY_ISSUE = "eligibility"
    DUPLICATE_CLAIM = "duplicate"
    INSUFFICIENT_DOCUMENTATION = "insufficient_docs"
    MEDICAL_NECESSITY = "medical_necessity"
    TIMELY_FILING = "timely_filing"
    COORDINATION_OF_BENEFITS = "cob"
    OTHER = "other"

class ResolutionWorkflow(Enum):
    RESUBMIT_WITH_AUTH = "resubmit_with_auth"
    CODE_REVIEW_CORRECT = "code_review_and_correct"
    VERIFY_ELIGIBILITY = "verify_eligibility"
    INVESTIGATE_DUPLICATE = "investigate_duplicate"
    REQUEST_DOCUMENTATION = "request_documentation"
    MEDICAL_REVIEW = "medical_review"
    APPEAL_FILING = "appeal_filing"
    COB_COORDINATION = "cob_coordination"
    MANUAL_REVIEW = "manual_review"

@dataclass
class DenialClassification:
    cause_category: DenialCause
    confidence: float
    subcategory: str
    resolution_workflow: ResolutionWorkflow
    appeal_success_probability: float
    recommended_actions: List[str]
    priority_score: int  # 1-10, 10 being highest priority
    estimated_resolution_time: int  # hours

class DenialInput(BaseModel):
    claim_id: str = Field(..., description="Claim identifier")
    denial_codes: List[str] = Field(..., description="Denial codes")
    denial_reason_text: str = Field(..., description="Denial reason text")
    raw_edi_segment: Optional[str] = Field(None, description="Raw EDI segment")
    claim_data: Dict[str, Any] = Field(..., description="Original claim data")

class ClassificationResponse(BaseModel):
    claim_id: str = Field(..., description="Claim identifier")
    cause_category: str = Field(..., description="Denial cause category")
    confidence: float = Field(..., ge=0, le=1, description="Classification confidence")
    subcategory: str = Field(..., description="Denial subcategory")
    resolution_workflow: str = Field(..., description="Recommended resolution workflow")
    appeal_success_probability: float = Field(..., ge=0, le=1, description="Appeal success probability")
    recommended_actions: List[str] = Field(..., description="Recommended actions")
    priority_score: int = Field(..., ge=1, le=10, description="Priority score (1-10)")
    estimated_resolution_time: int = Field(..., description="Estimated resolution time in hours")
    automated_actions_available: bool = Field(..., description="Whether automated actions are available")

class DenialClassifier:
    """Enhanced denial classification using multiple approaches"""
    
    def __init__(self):
        self.denial_code_mapping = self._load_denial_code_mapping()
        self.pattern_templates = self._load_pattern_templates()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.training_data = self._load_training_data()
        
    def _load_denial_code_mapping(self) -> Dict[str, DenialCause]:
        """Load mapping of denial codes to causes"""
        return {
            # CO (Contractual Obligation) codes
            "CO_16": DenialCause.MISSING_AUTHORIZATION,
            "CO_18": DenialCause.DUPLICATE_CLAIM,
            "CO_22": DenialCause.INVALID_CODE,
            "CO_23": DenialCause.ELIGIBILITY_ISSUE,
            "CO_24": DenialCause.INSUFFICIENT_DOCUMENTATION,
            "CO_50": DenialCause.MEDICAL_NECESSITY,
            "CO_96": DenialCause.TIMELY_FILING,
            "CO_97": DenialCause.COORDINATION_OF_BENEFITS,
            
            # PR (Patient Responsibility) codes
            "PR_1": DenialCause.ELIGIBILITY_ISSUE,
            "PR_2": DenialCause.COORDINATION_OF_BENEFITS,
            
            # OA (Other Adjustment) codes
            "OA_23": DenialCause.INVALID_CODE,
            "OA_50": DenialCause.MEDICAL_NECESSITY,
        }
    
    def _load_pattern_templates(self) -> Dict[DenialCause, List[str]]:
        """Load text patterns for each denial cause"""
        return {
            DenialCause.MISSING_AUTHORIZATION: [
                "authorization", "pre-certification", "pre-authorization", "prior approval",
                "auth required", "certification required", "approval needed"
            ],
            DenialCause.INVALID_CODE: [
                "invalid code", "invalid cpt", "invalid icd", "code not covered",
                "procedure not covered", "diagnosis not covered", "code error"
            ],
            DenialCause.ELIGIBILITY_ISSUE: [
                "not eligible", "eligibility", "coverage", "benefit", "member",
                "patient not covered", "coverage terminated", "no coverage"
            ],
            DenialCause.DUPLICATE_CLAIM: [
                "duplicate", "already paid", "previously submitted", "duplicate claim",
                "already processed", "repetitive claim"
            ],
            DenialCause.INSUFFICIENT_DOCUMENTATION: [
                "documentation", "medical records", "clinical notes", "insufficient",
                "missing documentation", "records needed", "chart notes"
            ],
            DenialCause.MEDICAL_NECESSITY: [
                "medical necessity", "not medically necessary", "experimental",
                "investigational", "not covered", "excluded service"
            ],
            DenialCause.TIMELY_FILING: [
                "timely filing", "filing deadline", "time limit", "late submission",
                "filing period", "deadline exceeded"
            ],
            DenialCause.COORDINATION_OF_BENEFITS: [
                "coordination of benefits", "cob", "other insurance", "primary",
                "secondary", "tertiary", "multiple coverage"
            ]
        }
    
    def _load_training_data(self) -> pd.DataFrame:
        """Load training data for text classification"""
        # Sample training data - in production this would come from a database
        data = {
            'text': [
                "Missing authorization for procedure",
                "Invalid CPT code submitted",
                "Patient not eligible for service",
                "Duplicate claim already processed",
                "Insufficient medical documentation",
                "Service not medically necessary",
                "Claim submitted after filing deadline",
                "Coordination of benefits required"
            ],
            'cause': [
                DenialCause.MISSING_AUTHORIZATION,
                DenialCause.INVALID_CODE,
                DenialCause.ELIGIBILITY_ISSUE,
                DenialCause.DUPLICATE_CLAIM,
                DenialCause.INSUFFICIENT_DOCUMENTATION,
                DenialCause.MEDICAL_NECESSITY,
                DenialCause.TIMELY_FILING,
                DenialCause.COORDINATION_OF_BENEFITS
            ]
        }
        return pd.DataFrame(data)
    
    def classify_denial(self, denial_input: DenialInput) -> DenialClassification:
        """Classify denial using multiple approaches"""
        logger.info(f"Classifying denial for claim {denial_input.claim_id}")
        
        # Classify by denial codes
        code_result = self._classify_by_codes(denial_input.denial_codes)
        
        # Classify by text analysis
        text_result = self._classify_by_text(denial_input.denial_reason_text)
        
        # Classify by pattern matching
        pattern_result = self._classify_by_patterns(denial_input.denial_reason_text)
        
        # Combine classifications
        classification = self._combine_classifications(
            code_result, text_result, pattern_result, denial_input
        )
        
        return classification
    
    def _classify_by_codes(self, denial_codes: List[str]) -> Tuple[DenialCause, float]:
        """Classify based on denial codes"""
        if not denial_codes:
            return DenialCause.OTHER, 0.0
        
        # Find matching codes
        matches = []
        for code in denial_codes:
            if code in self.denial_code_mapping:
                matches.append(self.denial_code_mapping[code])
        
        if matches:
            # Return most common cause
            cause_counts = {}
            for cause in matches:
                cause_counts[cause] = cause_counts.get(cause, 0) + 1
            
            most_common = max(cause_counts.items(), key=lambda x: x[1])
            confidence = most_common[1] / len(matches)
            return most_common[0], confidence
        
        return DenialCause.OTHER, 0.1
    
    def _classify_by_text(self, denial_text: str) -> Tuple[DenialCause, float]:
        """Classify based on text similarity"""
        if not denial_text:
            return DenialCause.OTHER, 0.0
        
        # Simple keyword matching for demo
        text_lower = denial_text.lower()
        
        for cause, patterns in self.pattern_templates.items():
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    return cause, 0.8
        
        return DenialCause.OTHER, 0.3
    
    def _classify_by_patterns(self, denial_text: str) -> Tuple[DenialCause, float]:
        """Classify using regex patterns"""
        if not denial_text:
            return DenialCause.OTHER, 0.0
        
        # Define regex patterns
        patterns = {
            DenialCause.MISSING_AUTHORIZATION: r'\b(auth|authorization|pre-cert|pre-auth)\b',
            DenialCause.INVALID_CODE: r'\b(invalid|incorrect|wrong)\s+(code|cpt|icd)\b',
            DenialCause.ELIGIBILITY_ISSUE: r'\b(not\s+eligible|coverage|benefit)\b',
            DenialCause.DUPLICATE_CLAIM: r'\b(duplicate|already\s+paid|previously)\b',
            DenialCause.INSUFFICIENT_DOCUMENTATION: r'\b(documentation|records|notes)\b',
            DenialCause.MEDICAL_NECESSITY: r'\b(medically\s+necessary|experimental)\b',
            DenialCause.TIMELY_FILING: r'\b(timely|deadline|late)\b',
            DenialCause.COORDINATION_OF_BENEFITS: r'\b(cob|coordination|other\s+insurance)\b'
        }
        
        for cause, pattern in patterns.items():
            if re.search(pattern, denial_text, re.IGNORECASE):
                return cause, 0.9
        
        return DenialCause.OTHER, 0.2
    
    def _combine_classifications(
        self,
        code_result: Tuple[DenialCause, float],
        text_result: Tuple[DenialCause, float],
        pattern_result: Tuple[DenialCause, float],
        denial_input: DenialInput
    ) -> DenialClassification:
        """Combine multiple classification results"""
        
        # Weight the results (codes are most reliable)
        code_cause, code_conf = code_result
        text_cause, text_conf = text_result
        pattern_cause, pattern_conf = pattern_result
        
        # Simple weighted voting
        causes = [code_cause, text_cause, pattern_cause]
        confidences = [code_conf * 0.5, text_conf * 0.3, pattern_conf * 0.2]
        
        # Find most common cause
        cause_counts = {}
        for cause in causes:
            cause_counts[cause] = cause_counts.get(cause, 0) + 1
        
        final_cause = max(cause_counts.items(), key=lambda x: x[1])[0]
        
        # Calculate weighted confidence
        total_confidence = sum(confidences)
        
        # Determine subcategory
        subcategory = self._determine_subcategory(final_cause, denial_input)
        
        # Determine workflow
        workflow = self._determine_workflow(final_cause)
        
        # Recommend actions
        actions = self._recommend_actions(final_cause, denial_input)
        
        # Calculate priority
        priority = self._calculate_priority(final_cause, denial_input)
        
        # Estimate appeal success
        appeal_success = self._estimate_appeal_success(final_cause, denial_input)
        
        # Estimate resolution time
        resolution_time = self._estimate_resolution_time(final_cause, workflow)
        
        return DenialClassification(
            cause_category=final_cause,
            confidence=total_confidence,
            subcategory=subcategory,
            resolution_workflow=workflow,
            appeal_success_probability=appeal_success,
            recommended_actions=actions,
            priority_score=priority,
            estimated_resolution_time=resolution_time
        )
    
    def _determine_subcategory(self, cause: DenialCause, denial_input: DenialInput) -> str:
        """Determine specific subcategory of the denial"""
        subcategories = {
            DenialCause.MISSING_AUTHORIZATION: "Prior Authorization Required",
            DenialCause.INVALID_CODE: "CPT/ICD Code Error",
            DenialCause.ELIGIBILITY_ISSUE: "Patient Coverage Issue",
            DenialCause.DUPLICATE_CLAIM: "Duplicate Submission",
            DenialCause.INSUFFICIENT_DOCUMENTATION: "Missing Medical Records",
            DenialCause.MEDICAL_NECESSITY: "Service Not Medically Necessary",
            DenialCause.TIMELY_FILING: "Filing Deadline Exceeded",
            DenialCause.COORDINATION_OF_BENEFITS: "Multiple Insurance Coordination",
            DenialCause.OTHER: "General Denial"
        }
        return subcategories.get(cause, "Unknown")
    
    def _determine_workflow(self, cause: DenialCause) -> ResolutionWorkflow:
        """Determine appropriate resolution workflow"""
        workflow_mapping = {
            DenialCause.MISSING_AUTHORIZATION: ResolutionWorkflow.RESUBMIT_WITH_AUTH,
            DenialCause.INVALID_CODE: ResolutionWorkflow.CODE_REVIEW_CORRECT,
            DenialCause.ELIGIBILITY_ISSUE: ResolutionWorkflow.VERIFY_ELIGIBILITY,
            DenialCause.DUPLICATE_CLAIM: ResolutionWorkflow.INVESTIGATE_DUPLICATE,
            DenialCause.INSUFFICIENT_DOCUMENTATION: ResolutionWorkflow.REQUEST_DOCUMENTATION,
            DenialCause.MEDICAL_NECESSITY: ResolutionWorkflow.MEDICAL_REVIEW,
            DenialCause.TIMELY_FILING: ResolutionWorkflow.APPEAL_FILING,
            DenialCause.COORDINATION_OF_BENEFITS: ResolutionWorkflow.COB_COORDINATION,
            DenialCause.OTHER: ResolutionWorkflow.MANUAL_REVIEW
        }
        return workflow_mapping.get(cause, ResolutionWorkflow.MANUAL_REVIEW)
    
    def _recommend_actions(self, cause: DenialCause, denial_input: DenialInput) -> List[str]:
        """Recommend specific actions based on denial cause"""
        action_templates = {
            DenialCause.MISSING_AUTHORIZATION: [
                "Request prior authorization from payer",
                "Verify authorization requirements for procedure",
                "Submit authorization request with clinical justification"
            ],
            DenialCause.INVALID_CODE: [
                "Review and correct CPT/ICD codes",
                "Verify code validity and coverage",
                "Update claim with correct codes"
            ],
            DenialCause.ELIGIBILITY_ISSUE: [
                "Verify patient eligibility and coverage",
                "Check benefit plan details",
                "Confirm service date coverage"
            ],
            DenialCause.DUPLICATE_CLAIM: [
                "Investigate potential duplicate submissions",
                "Check for similar claims in system",
                "Verify if claim was already processed"
            ],
            DenialCause.INSUFFICIENT_DOCUMENTATION: [
                "Request additional medical records",
                "Obtain clinical documentation",
                "Submit supporting documentation"
            ],
            DenialCause.MEDICAL_NECESSITY: [
                "Prepare medical necessity documentation",
                "Submit clinical justification",
                "Consider peer-to-peer review"
            ],
            DenialCause.TIMELY_FILING: [
                "File appeal for late submission",
                "Document extenuating circumstances",
                "Request filing deadline extension"
            ],
            DenialCause.COORDINATION_OF_BENEFITS: [
                "Coordinate with other insurance carriers",
                "Determine primary vs secondary coverage",
                "Submit COB information"
            ],
            DenialCause.OTHER: [
                "Review denial details thoroughly",
                "Contact payer for clarification",
                "Prepare appeal documentation"
            ]
        }
        return action_templates.get(cause, ["Manual review required"])
    
    def _calculate_priority(self, cause: DenialCause, denial_input: DenialInput) -> int:
        """Calculate priority score (1-10)"""
        base_priorities = {
            DenialCause.MISSING_AUTHORIZATION: 7,
            DenialCause.INVALID_CODE: 6,
            DenialCause.ELIGIBILITY_ISSUE: 8,
            DenialCause.DUPLICATE_CLAIM: 5,
            DenialCause.INSUFFICIENT_DOCUMENTATION: 6,
            DenialCause.MEDICAL_NECESSITY: 9,
            DenialCause.TIMELY_FILING: 8,
            DenialCause.COORDINATION_OF_BENEFITS: 7,
            DenialCause.OTHER: 4
        }
        
        base_priority = base_priorities.get(cause, 5)
        
        # Adjust based on claim amount
        claim_amount = denial_input.claim_data.get('claim_amount', 0)
        if claim_amount > 10000:
            base_priority += 1
        elif claim_amount > 5000:
            base_priority += 0.5
        
        return min(10, int(base_priority))
    
    def _estimate_appeal_success(self, cause: DenialCause, denial_input: DenialInput) -> float:
        """Estimate probability of successful appeal"""
        success_rates = {
            DenialCause.MISSING_AUTHORIZATION: 0.85,
            DenialCause.INVALID_CODE: 0.70,
            DenialCause.ELIGIBILITY_ISSUE: 0.30,
            DenialCause.DUPLICATE_CLAIM: 0.20,
            DenialCause.INSUFFICIENT_DOCUMENTATION: 0.75,
            DenialCause.MEDICAL_NECESSITY: 0.60,
            DenialCause.TIMELY_FILING: 0.40,
            DenialCause.COORDINATION_OF_BENEFITS: 0.80,
            DenialCause.OTHER: 0.50
        }
        return success_rates.get(cause, 0.50)
    
    def _estimate_resolution_time(self, cause: DenialCause, workflow: ResolutionWorkflow) -> int:
        """Estimate resolution time in hours"""
        time_estimates = {
            DenialCause.MISSING_AUTHORIZATION: 48,
            DenialCause.INVALID_CODE: 24,
            DenialCause.ELIGIBILITY_ISSUE: 72,
            DenialCause.DUPLICATE_CLAIM: 12,
            DenialCause.INSUFFICIENT_DOCUMENTATION: 96,
            DenialCause.MEDICAL_NECESSITY: 120,
            DenialCause.TIMELY_FILING: 168,
            DenialCause.COORDINATION_OF_BENEFITS: 72,
            DenialCause.OTHER: 48
        }
        return time_estimates.get(cause, 48) 