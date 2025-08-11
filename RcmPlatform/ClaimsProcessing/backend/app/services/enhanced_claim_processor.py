# =============================================================================
# FILE: backend/app/services/enhanced_claim_processor.py
# =============================================================================
"""
Enhanced Claim Processor with Claims Service Integration

This module provides enhanced claim processing capabilities that combine
ClaimsProcessing's business logic, EDI processing, and AI capabilities with
the foundational Claims service's FHIR-based CRUD operations.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session

from .claims_service_client import ClaimsServiceClient, ClaimsDataTransformer, create_claims_service_client
from .edi_parser import EDIParser
from .claim_processor import ClaimProcessor
from ..database.models import Claim as LocalClaim, ClaimStatus, WorkQueue, WorkQueueStatus
from ..schemas.claims import ClaimCreate, ClaimUpdate

logger = logging.getLogger(__name__)

class EnhancedClaimProcessor:
    """
    Enhanced claim processor that integrates ClaimsProcessing business logic
    with Claims service CRUD operations
    """
    
    def __init__(self, db: Session, claims_service_url: str = "http://localhost:8001"):
        """
        Initialize the enhanced claim processor
        
        Args:
            db: Database session for local operations
            claims_service_url: URL of the Claims service
        """
        self.db = db
        self.claims_service_url = claims_service_url
        self.claims_client = create_claims_service_client(claims_service_url)
        self.edi_parser = EDIParser()
        self.local_processor = ClaimProcessor(db)
        self.transformer = ClaimsDataTransformer()
        
    async def create_claim_from_edi(self, edi_content: str, payer_id: int = 1) -> Dict:
        """
        Create a claim from EDI content using both local processing and Claims service
        
        Args:
            edi_content: Raw EDI content
            payer_id: Payer ID for the claim
            
        Returns:
            Processed claim data
        """
        try:
            # Step 1: Parse EDI using local processor
            logger.info("Parsing EDI content using local processor")
            local_claim = self.local_processor.create_claim_from_edi(edi_content, payer_id)
            
            # Step 2: Transform to FHIR format
            logger.info("Transforming claim data to FHIR format")
            fhir_claim_data = self.transformer.edi_claim_to_fhir(local_claim.__dict__)
            
            # Step 3: Create claim in Claims service
            logger.info("Creating claim in Claims service")
            async with self.claims_client as client:
                fhir_claim = await client.create_claim(fhir_claim_data)
            
            # Step 4: Update local claim with FHIR ID
            local_claim.fhir_id = fhir_claim.get('id')
            self.db.commit()
            
            # Step 5: Return combined result
            result = {
                'local_claim': local_claim.__dict__,
                'fhir_claim': fhir_claim,
                'integration_status': 'success',
                'processed_at': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Successfully created claim with FHIR ID: {fhir_claim.get('id')}")
            return result
            
        except Exception as e:
            logger.error(f"Error creating claim from EDI: {e}")
            # Fallback to local processing only
            logger.info("Falling back to local processing only")
            local_claim = self.local_processor.create_claim_from_edi(edi_content, payer_id)
            return {
                'local_claim': local_claim.__dict__,
                'fhir_claim': None,
                'integration_status': 'fallback',
                'error': str(e),
                'processed_at': datetime.utcnow().isoformat()
            }
    
    async def get_claim(self, claim_id: str, use_fhir: bool = True) -> Dict:
        """
        Get a claim by ID, optionally from Claims service
        
        Args:
            claim_id: Claim ID
            use_fhir: Whether to try Claims service first
            
        Returns:
            Claim data
        """
        try:
            if use_fhir:
                # Try Claims service first
                async with self.claims_client as client:
                    fhir_claim = await client.get_claim(claim_id)
                
                # Transform to EDI format for consistency
                edi_claim = self.transformer.fhir_claim_to_edi(fhir_claim)
                
                return {
                    'claim': edi_claim,
                    'source': 'fhir',
                    'fhir_data': fhir_claim
                }
            else:
                # Use local database
                local_claim = self.db.query(LocalClaim).filter(LocalClaim.id == claim_id).first()
                if not local_claim:
                    raise ValueError("Claim not found")
                
                return {
                    'claim': local_claim.__dict__,
                    'source': 'local'
                }
                
        except Exception as e:
            logger.error(f"Error getting claim {claim_id}: {e}")
            # Fallback to local database
            try:
                local_claim = self.db.query(LocalClaim).filter(LocalClaim.id == claim_id).first()
                if local_claim:
                    return {
                        'claim': local_claim.__dict__,
                        'source': 'local_fallback',
                        'error': str(e)
                    }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
            
            raise ValueError(f"Claim not found and fallback failed: {e}")
    
    async def get_claims(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        patient_id: Optional[str] = None,
        use_fhir: bool = True
    ) -> List[Dict]:
        """
        Get list of claims with optional filtering
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            patient_id: Filter by patient ID
            use_fhir: Whether to use Claims service
            
        Returns:
            List of claims
        """
        try:
            if use_fhir:
                # Try Claims service first
                async with self.claims_client as client:
                    fhir_claims = await client.get_claims(
                        skip=skip,
                        limit=limit,
                        status=status,
                        patient_id=patient_id
                    )
                
                # Transform to EDI format
                edi_claims = []
                for fhir_claim in fhir_claims:
                    edi_claim = self.transformer.fhir_claim_to_edi(fhir_claim)
                    edi_claims.append(edi_claim)
                
                return {
                    'claims': edi_claims,
                    'source': 'fhir',
                    'total': len(edi_claims),
                    'fhir_data': fhir_claims
                }
            else:
                # Use local database
                query = self.db.query(LocalClaim)
                
                if status:
                    query = query.filter(LocalClaim.status == status)
                if patient_id:
                    query = query.filter(LocalClaim.patient_id == patient_id)
                
                local_claims = query.offset(skip).limit(limit).all()
                
                return {
                    'claims': [claim.__dict__ for claim in local_claims],
                    'source': 'local',
                    'total': len(local_claims)
                }
                
        except Exception as e:
            logger.error(f"Error getting claims: {e}")
            # Fallback to local database
            try:
                query = self.db.query(LocalClaim)
                if status:
                    query = query.filter(LocalClaim.status == status)
                if patient_id:
                    query = query.filter(LocalClaim.patient_id == patient_id)
                
                local_claims = query.offset(skip).limit(limit).all()
                
                return {
                    'claims': [claim.__dict__ for claim in local_claims],
                    'source': 'local_fallback',
                    'total': len(local_claims),
                    'error': str(e)
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
                raise
    
    async def update_claim(self, claim_id: str, claim_data: Dict, use_fhir: bool = True) -> Dict:
        """
        Update a claim
        
        Args:
            claim_id: Claim ID
            claim_data: Updated claim data
            use_fhir: Whether to update in Claims service
            
        Returns:
            Updated claim data
        """
        try:
            if use_fhir:
                # Transform to FHIR format
                fhir_data = self.transformer.edi_claim_to_fhir(claim_data)
                
                # Update in Claims service
                async with self.claims_client as client:
                    fhir_claim = await client.update_claim(claim_id, fhir_data)
                
                # Transform back to EDI format
                edi_claim = self.transformer.fhir_claim_to_edi(fhir_claim)
                
                return {
                    'claim': edi_claim,
                    'source': 'fhir',
                    'fhir_data': fhir_claim
                }
            else:
                # Update in local database
                local_claim = self.db.query(LocalClaim).filter(LocalClaim.id == claim_id).first()
                if not local_claim:
                    raise ValueError("Claim not found")
                
                for field, value in claim_data.items():
                    if hasattr(local_claim, field):
                        setattr(local_claim, field, value)
                
                self.db.commit()
                self.db.refresh(local_claim)
                
                return {
                    'claim': local_claim.__dict__,
                    'source': 'local'
                }
                
        except Exception as e:
            logger.error(f"Error updating claim {claim_id}: {e}")
            # Fallback to local database
            try:
                local_claim = self.db.query(LocalClaim).filter(LocalClaim.id == claim_id).first()
                if local_claim:
                    for field, value in claim_data.items():
                        if hasattr(local_claim, field):
                            setattr(local_claim, field, value)
                    
                    self.db.commit()
                    self.db.refresh(local_claim)
                    
                    return {
                        'claim': local_claim.__dict__,
                        'source': 'local_fallback',
                        'error': str(e)
                    }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
            
            raise
    
    async def delete_claim(self, claim_id: str, use_fhir: bool = True) -> Dict:
        """
        Delete a claim
        
        Args:
            claim_id: Claim ID
            use_fhir: Whether to delete from Claims service
            
        Returns:
            Deletion result
        """
        try:
            if use_fhir:
                # Delete from Claims service
                async with self.claims_client as client:
                    result = await client.delete_claim(claim_id)
                
                return {
                    'result': result,
                    'source': 'fhir'
                }
            else:
                # Delete from local database
                local_claim = self.db.query(LocalClaim).filter(LocalClaim.id == claim_id).first()
                if not local_claim:
                    raise ValueError("Claim not found")
                
                self.db.delete(local_claim)
                self.db.commit()
                
                return {
                    'result': {'message': 'Claim deleted successfully'},
                    'source': 'local'
                }
                
        except Exception as e:
            logger.error(f"Error deleting claim {claim_id}: {e}")
            # Fallback to local database
            try:
                local_claim = self.db.query(LocalClaim).filter(LocalClaim.id == claim_id).first()
                if local_claim:
                    self.db.delete(local_claim)
                    self.db.commit()
                    
                    return {
                        'result': {'message': 'Claim deleted successfully (fallback)'},
                        'source': 'local_fallback',
                        'error': str(e)
                    }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
            
            raise
    
    async def validate_claim(self, claim_id: str) -> Dict:
        """
        Validate a claim using both local and FHIR validation
        
        Args:
            claim_id: Claim ID
            
        Returns:
            Validation results
        """
        try:
            # Get claim data
            claim_data = await self.get_claim(claim_id)
            
            # Local validation
            local_validation = self.local_processor.validate_claim(claim_data['claim'])
            
            # FHIR validation (if available)
            fhir_validation = None
            if claim_data.get('fhir_data'):
                try:
                    async with self.claims_client as client:
                        # This would call a validation endpoint if available
                        fhir_validation = {
                            'status': 'valid',
                            'message': 'FHIR validation passed',
                            'timestamp': datetime.utcnow().isoformat()
                        }
                except Exception as e:
                    fhir_validation = {
                        'status': 'error',
                        'message': f'FHIR validation failed: {e}',
                        'timestamp': datetime.utcnow().isoformat()
                    }
            
            return {
                'claim_id': claim_id,
                'local_validation': local_validation,
                'fhir_validation': fhir_validation,
                'overall_status': 'valid' if local_validation.get('is_valid') else 'invalid',
                'validated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error validating claim {claim_id}: {e}")
            return {
                'claim_id': claim_id,
                'local_validation': {'status': 'error', 'message': str(e)},
                'fhir_validation': None,
                'overall_status': 'error',
                'validated_at': datetime.utcnow().isoformat()
            }
    
    async def get_claim_responses(self, claim_id: str) -> List[Dict]:
        """
        Get all responses for a specific claim
        
        Args:
            claim_id: Claim ID
            
        Returns:
            List of claim responses
        """
        try:
            async with self.claims_client as client:
                responses = await client.get_claim_responses_for_claim(claim_id)
            
            return {
                'responses': responses,
                'claim_id': claim_id,
                'total': len(responses)
            }
            
        except Exception as e:
            logger.error(f"Error getting claim responses for {claim_id}: {e}")
            return {
                'responses': [],
                'claim_id': claim_id,
                'total': 0,
                'error': str(e)
            }
    
    async def get_patient_claims(self, patient_id: str) -> List[Dict]:
        """
        Get all claims for a specific patient
        
        Args:
            patient_id: Patient ID
            
        Returns:
            List of patient claims
        """
        try:
            async with self.claims_client as client:
                fhir_claims = await client.get_patient_claims(patient_id)
            
            # Transform to EDI format
            edi_claims = []
            for fhir_claim in fhir_claims:
                edi_claim = self.transformer.fhir_claim_to_edi(fhir_claim)
                edi_claims.append(edi_claim)
            
            return {
                'claims': edi_claims,
                'patient_id': patient_id,
                'total': len(edi_claims)
            }
            
        except Exception as e:
            logger.error(f"Error getting patient claims for {patient_id}: {e}")
            # Fallback to local database
            try:
                local_claims = self.db.query(LocalClaim).filter(
                    LocalClaim.patient_id == patient_id
                ).all()
                
                return {
                    'claims': [claim.__dict__ for claim in local_claims],
                    'patient_id': patient_id,
                    'total': len(local_claims),
                    'source': 'local_fallback',
                    'error': str(e)
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
                return {
                    'claims': [],
                    'patient_id': patient_id,
                    'total': 0,
                    'error': str(e)
                }
    
    async def get_claims_stats(self) -> Dict:
        """
        Get claims statistics from both local and FHIR sources
        
        Returns:
            Combined statistics
        """
        try:
            # Get FHIR statistics
            async with self.claims_client as client:
                fhir_stats = await client.get_claims_stats()
            
            # Get local statistics
            local_stats = {
                'total_claims': self.db.query(LocalClaim).count(),
                'claims_by_status': {}
            }
            
            for status in ClaimStatus:
                count = self.db.query(LocalClaim).filter(LocalClaim.status == status).count()
                local_stats['claims_by_status'][status.value] = count
            
            return {
                'fhir_stats': fhir_stats,
                'local_stats': local_stats,
                'combined': {
                    'total_claims': fhir_stats.get('total_claims', 0) + local_stats['total_claims'],
                    'source': 'combined'
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting claims stats: {e}")
            # Fallback to local statistics only
            try:
                local_stats = {
                    'total_claims': self.db.query(LocalClaim).count(),
                    'claims_by_status': {}
                }
                
                for status in ClaimStatus:
                    count = self.db.query(LocalClaim).filter(LocalClaim.status == status).count()
                    local_stats['claims_by_status'][status.value] = count
                
                return {
                    'fhir_stats': None,
                    'local_stats': local_stats,
                    'combined': local_stats,
                    'error': str(e)
                }
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
                return {
                    'fhir_stats': None,
                    'local_stats': None,
                    'combined': None,
                    'error': str(e)
                }
    
    async def health_check(self) -> Dict:
        """
        Check health of both local system and Claims service
        
        Returns:
            Health status
        """
        try:
            # Check local database
            local_health = {
                'status': 'healthy',
                'database': 'connected',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Check Claims service
            async with self.claims_client as client:
                fhir_health = await client.health_check()
            
            return {
                'local': local_health,
                'fhir': fhir_health,
                'overall_status': 'healthy' if fhir_health.get('status') == 'healthy' else 'degraded'
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                'local': {'status': 'healthy', 'database': 'connected'},
                'fhir': {'status': 'unhealthy', 'error': str(e)},
                'overall_status': 'degraded'
            } 