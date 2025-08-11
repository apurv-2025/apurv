# Phase 2: Post-Denial Automation Implementation
# Healthcare Denial Prediction & Automation System

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import numpy as np

# External dependencies
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import torch
import mlflow
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, BackgroundTasks
import redis
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Temporal workflow imports (placeholder - would be actual temporal imports)
class workflow:
    @staticmethod
    def defn(cls): return cls
    @staticmethod
    def run(func): return func
    @staticmethod
    def execute_activity(activity, *args, **kwargs): return activity(*args, **kwargs)

class activity:
    @staticmethod
    def defn(func): return func

# Database Models
Base = declarative_base()

class DenialRecord(Base):
    __tablename__ = "denial_records"
    
    id = Column(Integer, primary_key=True)
    claim_id = Column(String, unique=True, nullable=False)
    denial_date = Column(DateTime, nullable=False)
    denial_codes = Column(Text)  # JSON string of denial codes
    denial_reason_text = Column(Text)
    classification_result = Column(Text)  # JSON string
    resolution_status = Column(String, default="pending")
    workflow_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RemediationAction(Base):
    __tablename__ = "remediation_actions"
    
    id = Column(Integer, primary_key=True)
    denial_record_id = Column(Integer, nullable=False)
    action_type = Column(String, nullable=False)
    action_data = Column(Text)  # JSON string
    status = Column(String, default="pending")
    success_probability = Column(Float)
    executed_at = Column(DateTime)
    result = Column(Text)  # JSON string of result

# Enums and Data Classes
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

@dataclass
class ClaimData:
    claim_id: str
    provider_id: str
    payer_id: str
    patient_id: str
    cpt_codes: List[str]
    icd_codes: List[str]
    claim_amount: float
    service_date: datetime
    submission_date: datetime
    modifiers: List[str] = None
    auth_number: str = None

# Pydantic Models for API
class DenialInput(BaseModel):
    claim_id: str
    denial_codes: List[str]
    denial_reason_text: str
    raw_edi_segment: Optional[str] = None
    claim_data: Dict[str, Any]

class ClassificationResponse(BaseModel):
    claim_id: str
    cause_category: str
    confidence: float
    subcategory: str
    resolution_workflow: str
    appeal_success_probability: float
    recommended_actions: List[str]
    priority_score: int
    estimated_resolution_time: int  # hours
    automated_actions_available: bool

class RemediationRequest(BaseModel):
    denial_record_id: int
    execute_automated_actions: bool = True
    override_workflow: Optional[str] = None

# 1. Enhanced Denial Classification Service
class EnhancedDenialClassifier:
    def __init__(self, model_path: str = "distilbert-base-uncased"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load pre-trained model for text classification
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path, 
            num_labels=len(DenialCause)
        )
        self.model.to(self.device)
        
        # Initialize TF-IDF vectorizer for similarity matching
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 3)
        )
        
        # Load denial code mappings and patterns
        self.denial_code_mapping = self._load_denial_code_mapping()
        self.pattern_templates = self._load_pattern_templates()
        
        # Initialize knowledge base from historical data
        self._initialize_knowledge_base()
        
        logging.info("Enhanced Denial Classifier initialized")
    
    def _load_denial_code_mapping(self) -> Dict[str, DenialCause]:
        """Load standard denial code to cause mappings"""
        return {
            # Common ANSI denial codes
            "1": DenialCause.MEDICAL_NECESSITY,
            "2": DenialCause.ELIGIBILITY_ISSUE,
            "3": DenialCause.COORDINATION_OF_BENEFITS,
            "4": DenialCause.MISSING_AUTHORIZATION,
            "11": DenialCause.INVALID_CODE,
            "18": DenialCause.DUPLICATE_CLAIM,
            "29": DenialCause.TIMELY_FILING,
            "50": DenialCause.INSUFFICIENT_DOCUMENTATION,
            # Add more mappings based on payer-specific codes
            "CO-16": DenialCause.MISSING_AUTHORIZATION,
            "CO-97": DenialCause.INSUFFICIENT_DOCUMENTATION,
            "CO-197": DenialCause.INVALID_CODE,
        }
    
    def _load_pattern_templates(self) -> Dict[DenialCause, List[str]]:
        """Load text patterns for each denial cause"""
        return {
            DenialCause.MISSING_AUTHORIZATION: [
                "prior authorization", "auth required", "pre-authorization",
                "PA required", "authorization not on file"
            ],
            DenialCause.INVALID_CODE: [
                "invalid procedure code", "invalid diagnosis code",
                "unbundling", "code not covered", "inappropriate code"
            ],
            DenialCause.ELIGIBILITY_ISSUE: [
                "patient not eligible", "coverage terminated",
                "not covered under plan", "eligibility not verified"
            ],
            DenialCause.DUPLICATE_CLAIM: [
                "duplicate", "already processed", "previously paid",
                "claim already on file"
            ],
            DenialCause.INSUFFICIENT_DOCUMENTATION: [
                "documentation not provided", "medical records required",
                "incomplete information", "additional documentation"
            ]
        }
    
    def _initialize_knowledge_base(self):
        """Initialize knowledge base from historical denial patterns"""
        # In production, this would load from your historical data
        # For now, we'll simulate with example patterns
        historical_patterns = [
            ("Prior authorization required for this procedure", DenialCause.MISSING_AUTHORIZATION),
            ("Invalid CPT code for diagnosis", DenialCause.INVALID_CODE),
            ("Patient eligibility could not be verified", DenialCause.ELIGIBILITY_ISSUE),
            ("Duplicate claim already processed", DenialCause.DUPLICATE_CLAIM),
            ("Medical necessity not established", DenialCause.MEDICAL_NECESSITY),
        ]
        
        texts = [pattern[0] for pattern in historical_patterns]
        self.historical_embeddings = self.tfidf_vectorizer.fit_transform(texts)
        self.historical_labels = [pattern[1] for pattern in historical_patterns]
    
    def classify_denial(self, denial_input: DenialInput) -> DenialClassification:
        """Main classification method combining multiple approaches"""
        
        # 1. Rule-based classification using denial codes
        code_classification = self._classify_by_codes(denial_input.denial_codes)
        
        # 2. Text-based classification using NLP
        text_classification = self._classify_by_text(denial_input.denial_reason_text)
        
        # 3. Pattern matching with historical data
        pattern_classification = self._classify_by_patterns(denial_input.denial_reason_text)
        
        # 4. Combine classifications with weighted voting
        final_classification = self._combine_classifications(
            code_classification,
            text_classification,
            pattern_classification,
            denial_input
        )
        
        # 5. Determine resolution workflow and actions
        workflow = self._determine_workflow(final_classification.cause_category)
        actions = self._recommend_actions(final_classification.cause_category, denial_input)
        priority = self._calculate_priority(final_classification, denial_input)
        appeal_probability = self._estimate_appeal_success(final_classification, denial_input)
        
        return DenialClassification(
            cause_category=final_classification.cause_category,
            confidence=final_classification.confidence,
            subcategory=final_classification.subcategory,
            resolution_workflow=workflow,
            appeal_success_probability=appeal_probability,
            recommended_actions=actions,
            priority_score=priority
        )
    
    def _classify_by_codes(self, denial_codes: List[str]) -> Tuple[DenialCause, float]:
        """Classify denial based on denial codes"""
        if not denial_codes:
            return DenialCause.OTHER, 0.0
        
        # Check for direct code mappings
        for code in denial_codes:
            if code in self.denial_code_mapping:
                return self.denial_code_mapping[code], 0.95
        
        # Check for pattern matches in codes
        code_text = " ".join(denial_codes).lower()
        if "auth" in code_text or "pa" in code_text:
            return DenialCause.MISSING_AUTHORIZATION, 0.8
        elif "dup" in code_text:
            return DenialCause.DUPLICATE_CLAIM, 0.8
        elif "elig" in code_text:
            return DenialCause.ELIGIBILITY_ISSUE, 0.8
        
        return DenialCause.OTHER, 0.1
    
    def _classify_by_text(self, denial_text: str) -> Tuple[DenialCause, float]:
        """Classify denial using transformer model"""
        if not denial_text:
            return DenialCause.OTHER, 0.0
        
        # Tokenize and prepare input
        inputs = self.tokenizer(
            denial_text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        ).to(self.device)
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(probabilities, dim=-1).item()
            confidence = probabilities[0][predicted_class].item()
        
        # Map prediction to denial cause
        causes = list(DenialCause)
        predicted_cause = causes[predicted_class] if predicted_class < len(causes) else DenialCause.OTHER
        
        return predicted_cause, confidence
    
    def _classify_by_patterns(self, denial_text: str) -> Tuple[DenialCause, float]:
        """Classify using pattern matching with historical data"""
        if not denial_text:
            return DenialCause.OTHER, 0.0
        
        # Transform text using TF-IDF
        text_vector = self.tfidf_vectorizer.transform([denial_text.lower()])
        
        # Calculate similarity with historical patterns
        similarities = cosine_similarity(text_vector, self.historical_embeddings)[0]
        
        # Find best match
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        if best_similarity > 0.3:  # Threshold for pattern matching
            return self.historical_labels[best_match_idx], best_similarity
        
        # Check for keyword patterns
        text_lower = denial_text.lower()
        for cause, patterns in self.pattern_templates.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return cause, 0.7
        
        return DenialCause.OTHER, 0.1
    
    def _combine_classifications(
        self,
        code_result: Tuple[DenialCause, float],
        text_result: Tuple[DenialCause, float],
        pattern_result: Tuple[DenialCause, float],
        denial_input: DenialInput
    ) -> DenialClassification:
        """Combine multiple classification results with weighted voting"""
        
        # Weights for different classification methods
        weights = {
            'codes': 0.4,    # Denial codes are usually reliable
            'text': 0.35,    # NLP classification
            'pattern': 0.25  # Pattern matching
        }
        
        # Count votes for each cause
        cause_votes = {}
        cause_votes[code_result[0]] = cause_votes.get(code_result[0], 0) + (weights['codes'] * code_result[1])
        cause_votes[text_result[0]] = cause_votes.get(text_result[0], 0) + (weights['text'] * text_result[1])
        cause_votes[pattern_result[0]] = cause_votes.get(pattern_result[0], 0) + (weights['pattern'] * pattern_result[1])
        
        # Find winning cause
        winning_cause = max(cause_votes.items(), key=lambda x: x[1])
        
        # Calculate overall confidence
        total_possible_score = sum(weights.values())
        confidence = min(winning_cause[1] / total_possible_score, 1.0)
        
        # Determine subcategory based on specific patterns
        subcategory = self._determine_subcategory(winning_cause[0], denial_input)
        
        return DenialClassification(
            cause_category=winning_cause[0],
            confidence=confidence,
            subcategory=subcategory,
            resolution_workflow=ResolutionWorkflow.MANUAL_REVIEW,  # Will be updated later
            appeal_success_probability=0.0,  # Will be calculated later
            recommended_actions=[],  # Will be populated later
            priority_score=5  # Default priority
        )
    
    def _determine_subcategory(self, cause: DenialCause, denial_input: DenialInput) -> str:
        """Determine more specific subcategory"""
        subcategory_map = {
            DenialCause.MISSING_AUTHORIZATION: {
                "default": "Standard Prior Auth",
                "retro": "Retroactive Auth Required",
                "specialist": "Specialist Referral Required"
            },
            DenialCause.INVALID_CODE: {
                "default": "General Coding Error",
                "bundling": "Unbundling Issue",
                "modifier": "Missing/Incorrect Modifier"
            }
        }
        
        if cause in subcategory_map:
            # Simple logic to determine subcategory
            # In production, this would be more sophisticated
            denial_text = denial_input.denial_reason_text.lower()
            for key, subcategory in subcategory_map[cause].items():
                if key in denial_text:
                    return subcategory
            return subcategory_map[cause]["default"]
        
        return "General"
    
    def _determine_workflow(self, cause: DenialCause) -> ResolutionWorkflow:
        """Map denial cause to resolution workflow"""
        workflow_map = {
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
        return workflow_map.get(cause, ResolutionWorkflow.MANUAL_REVIEW)
    
    def _recommend_actions(self, cause: DenialCause, denial_input: DenialInput) -> List[str]:
        """Recommend specific actions based on denial cause"""
        action_map = {
            DenialCause.MISSING_AUTHORIZATION: [
                "Request prior authorization from payer",
                "Check if retroactive auth is possible",
                "Verify authorization requirements for procedure"
            ],
            DenialCause.INVALID_CODE: [
                "Review CPT/ICD code accuracy",
                "Check for required modifiers",
                "Verify code is appropriate for diagnosis"
            ],
            DenialCause.ELIGIBILITY_ISSUE: [
                "Verify patient eligibility on date of service",
                "Check for coordination of benefits",
                "Confirm patient demographics"
            ]
        }
        return action_map.get(cause, ["Manual review required"])
    
    def _calculate_priority(self, classification: DenialClassification, denial_input: DenialInput) -> int:
        """Calculate priority score (1-10) based on multiple factors"""
        priority = 5  # Base priority
        
        # Adjust based on claim amount
        claim_amount = denial_input.claim_data.get('claim_amount', 0)
        if claim_amount > 10000:
            priority += 2
        elif claim_amount > 5000:
            priority += 1
        
        # Adjust based on confidence
        if classification.confidence > 0.9:
            priority += 1
        
        # Adjust based on cause type
        high_priority_causes = [DenialCause.TIMELY_FILING, DenialCause.ELIGIBILITY_ISSUE]
        if classification.cause_category in high_priority_causes:
            priority += 2
        
        # Adjust based on automated resolution potential
        automatable_causes = [DenialCause.MISSING_AUTHORIZATION, DenialCause.INVALID_CODE]
        if classification.cause_category in automatable_causes:
            priority += 1
        
        return min(max(priority, 1), 10)  # Clamp to 1-10 range
    
    def _estimate_appeal_success(self, classification: DenialClassification, denial_input: DenialInput) -> float:
        """Estimate probability of successful appeal"""
        base_rates = {
            DenialCause.MISSING_AUTHORIZATION: 0.85,
            DenialCause.INVALID_CODE: 0.75,
            DenialCause.ELIGIBILITY_ISSUE: 0.65,
            DenialCause.DUPLICATE_CLAIM: 0.90,
            DenialCause.INSUFFICIENT_DOCUMENTATION: 0.70,
            DenialCause.MEDICAL_NECESSITY: 0.45,
            DenialCause.TIMELY_FILING: 0.30,
            DenialCause.COORDINATION_OF_BENEFITS: 0.80,
            DenialCause.OTHER: 0.50
        }
        
        base_rate = base_rates.get(classification.cause_category, 0.50)
        
        # Adjust based on confidence
        confidence_adjustment = (classification.confidence - 0.5) * 0.2
        
        # Adjust based on claim characteristics
        claim_adjustment = 0.0
        if denial_input.claim_data.get('has_auth_number', False):
            claim_adjustment += 0.1
        
        final_probability = base_rate + confidence_adjustment + claim_adjustment
        return min(max(final_probability, 0.0), 1.0)

# 2. Auto-Remediation Engine
class AutoRemediationEngine:
    def __init__(self, db_session: Session, redis_client: redis.Redis):
        self.db_session = db_session
        self.redis_client = redis_client
        self.classifier = EnhancedDenialClassifier()
        self.action_handlers = self._initialize_action_handlers()
        
        logging.info("Auto-Remediation Engine initialized")
    
    def _initialize_action_handlers(self) -> Dict[ResolutionWorkflow, callable]:
        """Initialize handlers for each workflow type"""
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
        """Main method to process a denial and trigger remediation"""
        try:
            # 1. Classify the denial
            classification = self.classifier.classify_denial(denial_input)
            
            # 2. Store denial record in database
            denial_record = DenialRecord(
                claim_id=denial_input.claim_id,
                denial_date=datetime.utcnow(),
                denial_codes=json.dumps(denial_input.denial_codes),
                denial_reason_text=denial_input.denial_reason_text,
                classification_result=json.dumps({
                    "cause_category": classification.cause_category.value,
                    "confidence": classification.confidence,
                    "subcategory": classification.subcategory,
                    "resolution_workflow": classification.resolution_workflow.value,
                    "appeal_success_probability": classification.appeal_success_probability,
                    "priority_score": classification.priority_score
                })
            )
            
            self.db_session.add(denial_record)
            self.db_session.commit()
            
            # 3. Trigger appropriate workflow
            workflow_result = await self._execute_workflow(
                classification.resolution_workflow,
                denial_record.id,
                denial_input,
                classification
            )
            
            # 4. Update record with workflow ID
            denial_record.workflow_id = workflow_result.get('workflow_id')
            self.db_session.commit()
            
            return {
                "denial_record_id": denial_record.id,
                "classification": {
                    "cause_category": classification.cause_category.value,
                    "confidence": classification.confidence,
                    "subcategory": classification.subcategory,
                    "resolution_workflow": classification.resolution_workflow.value,
                    "appeal_success_probability": classification.appeal_success_probability,
                    "priority_score": classification.priority_score,
                    "recommended_actions": classification.recommended_actions
                },
                "workflow_result": workflow_result,
                "status": "processed"
            }
            
        except Exception as e:
            logging.error(f"Error processing denial {denial_input.claim_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    async def _execute_workflow(
        self,
        workflow_type: ResolutionWorkflow,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Execute the appropriate workflow"""
        
        handler = self.action_handlers.get(workflow_type)
        if not handler:
            logging.warning(f"No handler found for workflow type: {workflow_type}")
            return {"status": "no_handler", "workflow_id": None}
        
        try:
            result = await handler(denial_record_id, denial_input, classification)
            return result
        except Exception as e:
            logging.error(f"Error executing workflow {workflow_type}: {str(e)}")
            return {"status": "error", "error": str(e), "workflow_id": None}
    
    # Workflow Handlers
    async def _handle_resubmit_with_auth(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle missing authorization workflow"""
        
        # 1. Check if authorization can be requested automatically
        auth_requestable = await self._check_auth_requestable(denial_input)
        
        if auth_requestable:
            # 2. Request authorization
            auth_result = await self._request_authorization(denial_input)
            
            if auth_result.get('approved'):
                # 3. Prepare resubmission with auth number
                resubmit_result = await self._prepare_resubmission(
                    denial_input,
                    auth_number=auth_result['auth_number']
                )
                
                # 4. Log remediation action
                self._log_remediation_action(
                denial_record_id,
                "eligibility_verified_resubmit",
                {
                    "eligibility_proof": eligibility_result,
                    "resubmit_data": resubmit_result
                },
                "completed"
            )
            
            return {
                "status": "automated_resolution",
                "workflow_id": f"eligibility_resubmit_{denial_record_id}",
                "actions_taken": ["Verified patient eligibility", "Prepared resubmission"],
                "estimated_resolution_days": 2
            }
        else:
            # Patient not eligible - investigate further
            investigation_result = await self._investigate_eligibility_issue(
                denial_input,
                eligibility_result
            )
            
            return {
                "status": "eligibility_issue_confirmed",
                "workflow_id": f"eligibility_investigate_{denial_record_id}",
                "investigation_result": investigation_result,
                "manual_actions": [
                    "Contact patient to verify insurance information",
                    "Check for coordination of benefits",
                    "Verify service date coverage"
                ],
                "estimated_resolution_days": 7
            }
    
    async def _handle_duplicate_investigation(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle duplicate claim workflow"""
        
        # 1. Search for duplicate claims
        duplicate_search = await self._search_duplicate_claims(denial_input)
        
        if duplicate_search.get('found_duplicate'):
            duplicate_info = duplicate_search['duplicate_claim']
            
            # 2. Analyze the duplicate situation
            if duplicate_info['status'] == 'paid':
                # Original was already paid - no action needed
                self._log_remediation_action(
                    denial_record_id,
                    "duplicate_confirmed_paid",
                    {"original_claim": duplicate_info},
                    "completed"
                )
                
                return {
                    "status": "duplicate_confirmed",
                    "workflow_id": f"duplicate_resolved_{denial_record_id}",
                    "resolution": "Original claim already paid",
                    "no_action_required": True
                }
            else:
                # Need to investigate why both claims exist
                return {
                    "status": "duplicate_investigation_required",
                    "workflow_id": f"duplicate_investigate_{denial_record_id}",
                    "duplicate_info": duplicate_info,
                    "manual_actions": [
                        "Review both claims for differences",
                        "Determine if resubmission was appropriate",
                        "Contact payer if necessary"
                    ],
                    "estimated_resolution_days": 5
                }
        else:
            # No duplicate found - may be false positive
            return {
                "status": "no_duplicate_found",
                "workflow_id": f"false_duplicate_{denial_record_id}",
                "recommended_actions": [
                    "Appeal denial as false duplicate",
                    "Provide documentation proving uniqueness"
                ],
                "estimated_resolution_days": 14
            }
    
    async def _handle_documentation_request(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle insufficient documentation workflow"""
        
        # 1. Determine what documentation is needed
        doc_requirements = await self._analyze_documentation_requirements(denial_input)
        
        # 2. Check if documentation is available in system
        available_docs = await self._check_available_documentation(
            denial_input.claim_data['patient_id'],
            denial_input.claim_data['service_date'],
            doc_requirements
        )
        
        if available_docs.get('complete'):
            # 3. Auto-attach documentation and resubmit
            resubmit_result = await self._prepare_resubmission(
                denial_input,
                additional_docs=available_docs['documents']
            )
            
            self._log_remediation_action(
                denial_record_id,
                "auto_documentation_resubmit",
                {
                    "attached_docs": available_docs['documents'],
                    "resubmit_data": resubmit_result
                },
                "completed"
            )
            
            return {
                "status": "automated_resolution",
                "workflow_id": f"docs_resubmit_{denial_record_id}",
                "actions_taken": [f"Attached {len(available_docs['documents'])} documents"],
                "estimated_resolution_days": 4
            }
        else:
            # 4. Request missing documentation from provider
            missing_docs = doc_requirements['required'] - set(available_docs.get('found', []))
            
            notification_result = await self._notify_provider_documentation_needed(
                denial_input.claim_data['provider_id'],
                list(missing_docs),
                denial_input.claim_id
            )
            
            return {
                "status": "documentation_requested",
                "workflow_id": f"docs_request_{denial_record_id}",
                "missing_documents": list(missing_docs),
                "notification_sent": notification_result,
                "estimated_resolution_days": 10
            }
    
    async def _handle_medical_review(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle medical necessity review workflow"""
        
        # 1. Gather clinical information
        clinical_data = await self._gather_clinical_information(denial_input)
        
        # 2. Check against medical policy database
        policy_check = await self._check_medical_policies(
            denial_input.claim_data['cpt_codes'],
            denial_input.claim_data['icd_codes'],
            clinical_data
        )
        
        if policy_check.get('supported'):
            # 3. Prepare appeal with medical justification
            appeal_data = await self._prepare_medical_necessity_appeal(
                denial_input,
                clinical_data,
                policy_check
            )
            
            self._log_remediation_action(
                denial_record_id,
                "medical_necessity_appeal",
                {"appeal_data": appeal_data},
                "submitted"
            )
            
            return {
                "status": "appeal_submitted",
                "workflow_id": f"medical_appeal_{denial_record_id}",
                "appeal_strength": policy_check['strength'],
                "estimated_resolution_days": 21
            }
        else:
            # 4. Medical necessity not clearly supported
            return {
                "status": "medical_review_required",
                "workflow_id": f"medical_review_{denial_record_id}",
                "policy_gaps": policy_check.get('gaps', []),
                "manual_actions": [
                    "Clinical review by medical director",
                    "Gather additional supporting documentation",
                    "Consider alternative treatment codes"
                ],
                "estimated_resolution_days": 14
            }
    
    async def _handle_appeal_filing(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle timely filing and other appeal workflows"""
        
        # 1. Check appeal deadlines
        appeal_deadlines = await self._check_appeal_deadlines(denial_input)
        
        if appeal_deadlines.get('within_deadline'):
            # 2. Prepare and submit appeal
            appeal_result = await self._prepare_and_submit_appeal(
                denial_input,
                classification,
                appeal_deadlines
            )
            
            self._log_remediation_action(
                denial_record_id,
                "appeal_submitted",
                {"appeal_data": appeal_result},
                "submitted"
            )
            
            return {
                "status": "appeal_submitted",
                "workflow_id": f"appeal_{denial_record_id}",
                "appeal_level": appeal_result['level'],
                "deadline": appeal_deadlines['deadline'],
                "estimated_resolution_days": 30
            }
        else:
            # 3. Past deadline - limited options
            return {
                "status": "appeal_deadline_passed",
                "workflow_id": f"late_appeal_{denial_record_id}",
                "options": [
                    "Request deadline extension with good cause",
                    "Write off claim if extension denied",
                    "Review for billing errors that could justify late appeal"
                ],
                "estimated_resolution_days": 45
            }
    
    async def _handle_cob_coordination(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle coordination of benefits workflow"""
        
        # 1. Identify other insurance coverage
        cob_analysis = await self._analyze_coordination_of_benefits(denial_input)
        
        if cob_analysis.get('other_coverage_found'):
            # 2. Determine primary/secondary order
            coverage_order = await self._determine_coverage_order(
                cob_analysis['coverages'],
                denial_input.claim_data['patient_id']
            )
            
            # 3. Resubmit to correct payer or update COB info
            if coverage_order['current_payer_is_primary']:
                # Update claim with secondary insurance info
                resubmit_result = await self._prepare_resubmission(
                    denial_input,
                    cob_info=coverage_order
                )
                
                return {
                    "status": "cob_corrected_resubmit",
                    "workflow_id": f"cob_resubmit_{denial_record_id}",
                    "actions_taken": ["Updated coordination of benefits information"],
                    "estimated_resolution_days": 3
                }
            else:
                # Submit to primary payer first
                return {
                    "status": "submit_to_primary_first",
                    "workflow_id": f"cob_primary_{denial_record_id}",
                    "primary_payer": coverage_order['primary_payer'],
                    "manual_actions": [
                        f"Submit claim to primary payer: {coverage_order['primary_payer']}",
                        "Obtain EOB from primary payer",
                        "Resubmit to secondary with primary EOB"
                    ],
                    "estimated_resolution_days": 21
                }
        else:
            # No other coverage found
            return {
                "status": "no_other_coverage",
                "workflow_id": f"cob_false_{denial_record_id}",
                "recommended_actions": [
                    "Appeal COB denial with documentation",
                    "Verify patient insurance information is current"
                ],
                "estimated_resolution_days": 14
            }
    
    async def _handle_manual_review(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle cases requiring manual review"""
        
        # 1. Create detailed review package
        review_package = await self._create_manual_review_package(
            denial_input,
            classification
        )
        
        # 2. Assign to appropriate team/specialist
        assignment_result = await self._assign_to_specialist(
            denial_record_id,
            classification.cause_category,
            review_package
        )
        
        # 3. Set up monitoring and follow-up
        follow_up_result = await self._schedule_follow_up(
            denial_record_id,
            assignment_result['assigned_to'],
            classification.priority_score
        )
        
        return {
            "status": "assigned_for_manual_review",
            "workflow_id": f"manual_{denial_record_id}",
            "assigned_to": assignment_result['assigned_to'],
            "review_package": review_package['summary'],
            "follow_up_date": follow_up_result['follow_up_date'],
            "estimated_resolution_days": 14
        }
    
    # Helper Methods for Workflow Handlers
    async def _check_auth_requestable(self, denial_input: DenialInput) -> bool:
        """Check if authorization can be requested automatically"""
        # Implementation would check payer capabilities, procedure requirements, etc.
        return True  # Simplified for example
    
    async def _request_authorization(self, denial_input: DenialInput) -> Dict[str, Any]:
        """Request prior authorization from payer"""
        # Simulate authorization request
        return {
            "approved": True,
            "auth_number": f"AUTH{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "valid_through": (datetime.now() + timedelta(days=90)).isoformat()
        }
    
    async def _prepare_resubmission(self, denial_input: DenialInput, **kwargs) -> Dict[str, Any]:
        """Prepare claim for resubmission with corrections"""
        resubmission_data = {
            "original_claim_id": denial_input.claim_id,
            "new_claim_id": f"{denial_input.claim_id}_RESUBMIT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "corrections_applied": list(kwargs.keys()),
            "resubmit_date": datetime.now().isoformat(),
            "status": "prepared"
        }
        
        # Add specific corrections based on kwargs
        if 'auth_number' in kwargs:
            resubmission_data['auth_number'] = kwargs['auth_number']
        if 'corrected_data' in kwargs:
            resubmission_data['code_corrections'] = kwargs['corrected_data']
        if 'eligibility_proof' in kwargs:
            resubmission_data['eligibility_verification'] = kwargs['eligibility_proof']
        
        return resubmission_data
    
    async def _analyze_coding_issue(self, denial_input: DenialInput) -> Dict[str, Any]:
        """Analyze coding issues and suggest corrections"""
        # Simplified coding analysis
        analysis = {
            "auto_correctable": False,
            "issues_found": [],
            "suggested_corrections": {}
        }
        
        # Example: Check for common modifier issues
        cpt_codes = denial_input.claim_data.get('cpt_codes', [])
        if '99213' in cpt_codes and 'modifier_25' not in denial_input.claim_data.get('modifiers', []):
            analysis["auto_correctable"] = True
            analysis["issues_found"].append("Missing modifier 25 for E&M with procedure")
            analysis["suggested_corrections"]["add_modifier"] = "25"
        
        return analysis
    
    async def _apply_code_corrections(self, denial_input: DenialInput, corrections: Dict[str, Any]) -> Dict[str, Any]:
        """Apply coding corrections to claim data"""
        corrected_claim = denial_input.claim_data.copy()
        
        if "add_modifier" in corrections:
            modifiers = corrected_claim.get('modifiers', [])
            modifiers.append(corrections["add_modifier"])
            corrected_claim['modifiers'] = modifiers
        
        return corrected_claim
    
    async def _check_patient_eligibility(self, patient_id: str, service_date: str) -> Dict[str, Any]:
        """Check patient eligibility for service date"""
        # Simulate eligibility check
        return {
            "eligible": True,
            "coverage_effective": "2024-01-01",
            "coverage_termination": None,
            "copay": 25.00,
            "deductible_remaining": 500.00
        }
    
    def _log_remediation_action(
        self,
        denial_record_id: int,
        action_type: str,
        action_data: Dict[str, Any],
        status: str
    ):
        """Log remediation action to database"""
        action = RemediationAction(
            denial_record_id=denial_record_id,
            action_type=action_type,
            action_data=json.dumps(action_data, default=str),
            status=status,
            executed_at=datetime.utcnow() if status != "pending" else None
        )
        
        self.db_session.add(action)
        self.db_session.commit()
    
    async def _escalate_to_manual_review(
        self,
        denial_record_id: int,
        reason: str,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Escalate case to manual review"""
        return {
            "status": "escalated_to_manual",
            "workflow_id": f"escalated_{denial_record_id}",
            "escalation_reason": reason,
            "priority": classification.priority_score,
            "estimated_resolution_days": 10
        }

# 3. FastAPI Service for Phase 2
def create_phase2_api() -> FastAPI:
    """Create FastAPI application for Phase 2 denial automation"""
    
    app = FastAPI(
        title="Healthcare Denial Automation API - Phase 2",
        description="Post-denial classification and auto-remediation service",
        version="2.0.0"
    )
    
    # Initialize components (in production, these would be dependency-injected)
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    engine = create_engine("postgresql://user:pass@localhost/denials_db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    @app.post("/classify-denial", response_model=ClassificationResponse)
    async def classify_denial_endpoint(denial_input: DenialInput):
        """Classify a denial and return recommended actions"""
        try:
            classifier = EnhancedDenialClassifier()
            classification = classifier.classify_denial(denial_input)
            
            return ClassificationResponse(
                claim_id=denial_input.claim_id,
                cause_category=classification.cause_category.value,
                confidence=classification.confidence,
                subcategory=classification.subcategory,
                resolution_workflow=classification.resolution_workflow.value,
                appeal_success_probability=classification.appeal_success_probability,
                recommended_actions=classification.recommended_actions,
                priority_score=classification.priority_score,
                estimated_resolution_time=24,  # hours
                automated_actions_available=classification.resolution_workflow != ResolutionWorkflow.MANUAL_REVIEW
            )
            
        except Exception as e:
            logging.error(f"Error classifying denial: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/process-denial")
    async def process_denial_endpoint(
        denial_input: DenialInput,
        background_tasks: BackgroundTasks,
        db: Session = None  # Would use Depends(get_db) in production
    ):
        """Process a denial through the complete automation pipeline"""
        try:
            # Initialize session if not provided (for demo)
            if db is None:
                db = SessionLocal()
            
            remediation_engine = AutoRemediationEngine(db, redis_client)
            result = await remediation_engine.process_denial(denial_input)
            
            return {
                "message": "Denial processed successfully",
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error processing denial: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if db:
                db.close()
    
    @app.post("/execute-remediation")
    async def execute_remediation_endpoint(
        request: RemediationRequest,
        db: Session = None  # Would use Depends(get_db) in production
    ):
        """Execute remediation actions for a specific denial"""
        try:
            if db is None:
                db = SessionLocal()
            
            # Get denial record
            denial_record = db.query(DenialRecord).filter(
                DenialRecord.id == request.denial_record_id
            ).first()
            
            if not denial_record:
                raise HTTPException(status_code=404, detail="Denial record not found")
            
            # Get classification from stored data
            classification_data = json.loads(denial_record.classification_result)
            
            # Create mock denial input for processing
            mock_denial_input = DenialInput(
                claim_id=denial_record.claim_id,
                denial_codes=json.loads(denial_record.denial_codes),
                denial_reason_text=denial_record.denial_reason_text,
                claim_data={}  # Would be populated from claim database
            )
            
            remediation_engine = AutoRemediationEngine(db, redis_client)
            
            # Execute specific workflow
            workflow_type = ResolutionWorkflow(classification_data['resolution_workflow'])
            if request.override_workflow:
                workflow_type = ResolutionWorkflow(request.override_workflow)
            
            # Create classification object
            classification = DenialClassification(
                cause_category=DenialCause(classification_data['cause_category']),
                confidence=classification_data['confidence'],
                subcategory=classification_data['subcategory'],
                resolution_workflow=workflow_type,
                appeal_success_probability=classification_data['appeal_success_probability'],
                recommended_actions=[],
                priority_score=classification_data['priority_score']
            )
            
            result = await remediation_engine._execute_workflow(
                workflow_type,
                request.denial_record_id,
                mock_denial_input,
                classification
            )
            
            return {
                "message": "Remediation executed successfully",
                "denial_record_id": request.denial_record_id,
                "workflow_executed": workflow_type.value,
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error executing remediation: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if db:
                db.close()
    
    @app.get("/denial-status/{denial_record_id}")
    async def get_denial_status(denial_record_id: int, db: Session = None):
        """Get status of a denial and its remediation actions"""
        try:
            if db is None:
                db = SessionLocal()
            
            denial_record = db.query(DenialRecord).filter(
                DenialRecord.id == denial_record_id
            ).first()
            
            if not denial_record:
                raise HTTPException(status_code=404, detail="Denial record not found")
            
            # Get remediation actions
            actions = db.query(RemediationAction).filter(
                RemediationAction.denial_record_id == denial_record_id
            ).all()
            
            return {
                "denial_record": {
                    "id": denial_record.id,
                    "claim_id": denial_record.claim_id,
                    "denial_date": denial_record.denial_date.isoformat(),
                    "classification": json.loads(denial_record.classification_result),
                    "resolution_status": denial_record.resolution_status,
                    "workflow_id": denial_record.workflow_id
                },
                "remediation_actions": [
                    {
                        "id": action.id,
                        "action_type": action.action_type,
                        "status": action.status,
                        "executed_at": action.executed_at.isoformat() if action.executed_at else None,
                        "result": json.loads(action.result) if action.result else None
                    }
                    for action in actions
                ],
                "total_actions": len(actions),
                "pending_actions": len([a for a in actions if a.status == "pending"])
            }
            
        except Exception as e:
            logging.error(f"Error getting denial status: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if db:
                db.close()
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "denial-automation-phase2",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    return app

# 4. Example Usage and Testing
if __name__ == "__main__":
    # Example of how to use the Phase 2 system
    import asyncio
    
    async def example_usage():
        """Demonstrate Phase 2 functionality"""
        
        # Example denial input
        sample_denial = DenialInput(
            claim_id="CLM_20250810_001",
            denial_codes=["CO-16", "4"],
            denial_reason_text="Prior authorization required for this procedure. Please obtain authorization and resubmit.",
            claim_data={
                "provider_id": "PROV_12345",
                "payer_id": "PAYER_ABC",
                "patient_id": "PAT_67890",
                "cpt_codes": ["99213", "12031"],
                "icd_codes": ["Z00.00"],
                "claim_amount": 425.00,
                "service_date": "2025-08-05",
                "submission_date": "2025-08-06",
                "modifiers": []
            }
        )
        
        # Initialize classifier
        classifier = EnhancedDenialClassifier()
        
        # Classify the denial
        classification = classifier.classify_denial(sample_denial)
        
        print("=== Denial Classification Results ===")
        print(f"Claim ID: {sample_denial.claim_id}")
        print(f"Cause Category: {classification.cause_category.value}")
        print(f"Confidence: {classification.confidence:.2f}")
        print(f"Subcategory: {classification.subcategory}")
        print(f"Resolution Workflow: {classification.resolution_workflow.value}")
        print(f"Appeal Success Probability: {classification.appeal_success_probability:.2f}")
        print(f"Priority Score: {classification.priority_score}")
        print(f"Recommended Actions: {classification.recommended_actions}")
        print("\n")
        
        # Simulate database session
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        engine = create_engine("sqlite:///test_denials.db")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Initialize remediation engine
        redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)
        remediation_engine = AutoRemediationEngine(db, redis_client)
        
        try:
            # Process the denial
            result = await remediation_engine.process_denial(sample_denial)
            
            print("=== Remediation Results ===")
            print(f"Status: {result['status']}")
            print(f"Denial Record ID: {result['denial_record_id']}")
            print(f"Workflow Result: {result['workflow_result']}")
            print("\n")
            
        except Exception as e:
            print(f"Error during processing: {str(e)}")
        finally:
            db.close()
    
    # Run example (comment out in production)
    # asyncio.run(example_usage())
                    denial_record_id,
                    "auto_resubmit_with_auth",
                    {
                        "auth_number": auth_result['auth_number'],
                        "resubmit_data": resubmit_result
                    },
                    "completed"
                )
                
                return {
                    "status": "automated_resolution",
                    "workflow_id": f"auth_resubmit_{denial_record_id}",
                    "actions_taken": [
                        f"Requested authorization: {auth_result['auth_number']}",
                        "Prepared claim resubmission"
                    ],
                    "next_steps": ["Monitor resubmission status"],
                    "estimated_resolution_days": 5
                }
            else:
                # Authorization denied - escalate to manual review
                return await self._escalate_to_manual_review(
                    denial_record_id,
                    "Authorization request denied",
                    classification
                )
        else:
            # Cannot auto-request auth - provide instructions
            manual_actions = [
                "Contact payer to request prior authorization",
                "Gather required clinical documentation",
                "Submit PA request through payer portal"
            ]
            
            self._log_remediation_action(
                denial_record_id,
                "manual_auth_required",
                {"manual_actions": manual_actions},
                "pending_manual"
            )
            
            return {
                "status": "manual_intervention_required",
                "workflow_id": f"manual_auth_{denial_record_id}",
                "manual_actions": manual_actions,
                "estimated_resolution_days": 10
            }
    
    async def _handle_code_correction(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle invalid code workflow"""
        
        # 1. Analyze the coding issue
        code_analysis = await self._analyze_coding_issue(denial_input)
        
        if code_analysis.get('auto_correctable'):
            # 2. Apply automatic corrections
            corrections = code_analysis['suggested_corrections']
            corrected_claim = await self._apply_code_corrections(denial_input, corrections)
            
            # 3. Prepare resubmission
            resubmit_result = await self._prepare_resubmission(
                denial_input,
                corrected_data=corrected_claim
            )
            
            self._log_remediation_action(
                denial_record_id,
                "auto_code_correction",
                {
                    "corrections": corrections,
                    "resubmit_data": resubmit_result
                },
                "completed"
            )
            
            return {
                "status": "automated_resolution",
                "workflow_id": f"code_correct_{denial_record_id}",
                "actions_taken": [f"Applied corrections: {corrections}"],
                "estimated_resolution_days": 3
            }
        else:
            # Requires manual coding review
            return await self._escalate_to_coding_team(
                denial_record_id,
                code_analysis,
                classification
            )
    
    async def _handle_eligibility_verification(
        self,
        denial_record_id: int,
        denial_input: DenialInput,
        classification: DenialClassification
    ) -> Dict[str, Any]:
        """Handle eligibility issue workflow"""
        
        # 1. Perform real-time eligibility check
        eligibility_result = await self._check_patient_eligibility(
            denial_input.claim_data['patient_id'],
            denial_input.claim_data['service_date']
        )
        
        if eligibility_result.get('eligible'):
            # 2. Patient was eligible - resubmit with eligibility proof
            resubmit_result = await self._prepare_resubmission(
                denial_input,
                eligibility_proof=eligibility_result
            )
            
            self._log_remediation_action(
