# =============================================================================
# FILE: src/enhanced_inference.py
# =============================================================================
"""
Enhanced Inference Engine with Claims Service Integration

This module provides enhanced inference capabilities that combine
ClaimsAnomaly's ML anomaly detection with the foundational Claims service's
FHIR-based CRUD operations.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
import numpy as np

from .inference import ClaimsInferenceEngine
from ..api.claims_service_client import ClaimsServiceClient, ClaimsDataTransformer, create_claims_service_client

logger = logging.getLogger(__name__)

class EnhancedClaimsInferenceEngine:
    """
    Enhanced inference engine that integrates ClaimsAnomaly ML capabilities
    with Claims service CRUD operations
    """
    
    def __init__(self, model_path: str, claims_service_url: str = None):
        """
        Initialize the enhanced inference engine
        
        Args:
            model_path: Path to the trained ML model
            claims_service_url: URL of the Claims service (defaults to env var)
        """
        import os
        
        self.model_path = model_path
        # Use environment variable if not provided, fallback to default
        self.claims_service_url = claims_service_url or os.getenv('CLAIMS_SERVICE_URL', 'http://localhost:8001')
        self.claims_client = create_claims_service_client(self.claims_service_url)
        self.inference_engine = ClaimsInferenceEngine(model_path)
        self.transformer = ClaimsDataTransformer()
        
    async def score_single_claim(self, claim_data: Dict, use_fhir: bool = True) -> Dict:
        """
        Score a single claim for anomaly detection with integration
        
        Args:
            claim_data: Claim data in ClaimsAnomaly format
            use_fhir: Whether to store in Claims service
            
        Returns:
            Scoring result with integration status
        """
        try:
            # Step 1: Score using local ML model
            logger.info("Scoring claim using local ML model")
            scoring_result = self.inference_engine.score_single_claim(claim_data)
            
            # Step 2: Transform to FHIR format and store in Claims service
            if use_fhir:
                logger.info("Storing claim in Claims service")
                fhir_claim_data = self.transformer.anomaly_claim_to_fhir(claim_data)
                
                async with self.claims_client as client:
                    fhir_claim = await client.create_claim(fhir_claim_data)
                
                # Step 3: Update scoring result with FHIR information
                scoring_result.update({
                    'fhir_claim_id': fhir_claim.get('id'),
                    'integration_status': 'success',
                    'stored_in_fhir': True
                })
            else:
                scoring_result.update({
                    'integration_status': 'local_only',
                    'stored_in_fhir': False
                })
            
            scoring_result['processed_at'] = datetime.utcnow().isoformat()
            
            logger.info(f"Successfully scored claim with FHIR ID: {scoring_result.get('fhir_claim_id')}")
            return scoring_result
            
        except Exception as e:
            logger.error(f"Error scoring claim: {e}")
            # Fallback to local scoring only
            logger.info("Falling back to local scoring only")
            scoring_result = self.inference_engine.score_single_claim(claim_data)
            scoring_result.update({
                'integration_status': 'fallback',
                'stored_in_fhir': False,
                'error': str(e),
                'processed_at': datetime.utcnow().isoformat()
            })
            return scoring_result
    
    async def score_batch_claims(self, batch_claims: List[Dict], use_fhir: bool = True) -> Dict:
        """
        Score a batch of claims for anomaly detection with integration
        
        Args:
            batch_claims: List of claim data in ClaimsAnomaly format
            use_fhir: Whether to store in Claims service
            
        Returns:
            Batch scoring results with integration status
        """
        try:
            # Step 1: Score using local ML model
            logger.info(f"Scoring {len(batch_claims)} claims using local ML model")
            batch_result = self.inference_engine.score_batch_claims(batch_claims)
            
            # Step 2: Transform to FHIR format and store in Claims service
            if use_fhir:
                logger.info("Storing claims in Claims service")
                fhir_claims_data = self.transformer.batch_anomaly_to_fhir(batch_claims)
                
                stored_claims = []
                async with self.claims_client as client:
                    for fhir_claim_data in fhir_claims_data:
                        try:
                            fhir_claim = await client.create_claim(fhir_claim_data)
                            stored_claims.append(fhir_claim.get('id'))
                        except Exception as e:
                            logger.warning(f"Failed to store claim in FHIR: {e}")
                            stored_claims.append(None)
                
                # Step 3: Update batch result with FHIR information
                batch_result.update({
                    'fhir_claim_ids': stored_claims,
                    'integration_status': 'success',
                    'stored_in_fhir': True,
                    'successfully_stored': len([x for x in stored_claims if x is not None])
                })
            else:
                batch_result.update({
                    'integration_status': 'local_only',
                    'stored_in_fhir': False,
                    'successfully_stored': 0
                })
            
            batch_result['processed_at'] = datetime.utcnow().isoformat()
            
            logger.info(f"Successfully scored batch with {batch_result.get('successfully_stored', 0)} claims stored in FHIR")
            return batch_result
            
        except Exception as e:
            logger.error(f"Error scoring batch claims: {e}")
            # Fallback to local scoring only
            logger.info("Falling back to local scoring only")
            batch_result = self.inference_engine.score_batch_claims(batch_claims)
            batch_result.update({
                'integration_status': 'fallback',
                'stored_in_fhir': False,
                'error': str(e),
                'processed_at': datetime.utcnow().isoformat()
            })
            return batch_result
    
    async def get_claims_for_scoring(self, limit: int = 100, use_fhir: bool = True) -> List[Dict]:
        """
        Get claims from Claims service for scoring
        
        Args:
            limit: Maximum number of claims to retrieve
            use_fhir: Whether to get from Claims service
            
        Returns:
            List of claims in ClaimsAnomaly format
        """
        try:
            if use_fhir:
                # Get claims from Claims service
                async with self.claims_client as client:
                    fhir_claims = await client.get_claims(limit=limit)
                
                # Transform to ClaimsAnomaly format
                anomaly_claims = self.transformer.batch_fhir_to_anomaly(fhir_claims)
                
                return {
                    'claims': anomaly_claims,
                    'source': 'fhir',
                    'total': len(anomaly_claims)
                }
            else:
                # Return empty list for local-only mode
                return {
                    'claims': [],
                    'source': 'local_only',
                    'total': 0
                }
                
        except Exception as e:
            logger.error(f"Error getting claims for scoring: {e}")
            return {
                'claims': [],
                'source': 'error',
                'total': 0,
                'error': str(e)
            }
    
    async def score_claims_from_service(self, limit: int = 100, use_fhir: bool = True) -> Dict:
        """
        Get claims from Claims service and score them
        
        Args:
            limit: Maximum number of claims to retrieve and score
            use_fhir: Whether to get from Claims service
            
        Returns:
            Scoring results for claims from service
        """
        try:
            # Get claims from service
            claims_data = await self.get_claims_for_scoring(limit, use_fhir)
            
            if not claims_data['claims']:
                return {
                    'message': 'No claims available for scoring',
                    'results': [],
                    'count': 0,
                    'source': claims_data['source']
                }
            
            # Score the claims
            batch_result = await self.score_batch_claims(claims_data['claims'], use_fhir=False)
            
            return {
                'message': f"Scored {len(claims_data['claims'])} claims from {claims_data['source']}",
                'results': batch_result.get('results', []),
                'count': len(claims_data['claims']),
                'source': claims_data['source'],
                'integration_status': batch_result.get('integration_status', 'local_only')
            }
            
        except Exception as e:
            logger.error(f"Error scoring claims from service: {e}")
            return {
                'message': f'Error: {str(e)}',
                'results': [],
                'count': 0,
                'source': 'error',
                'error': str(e)
            }
    
    async def get_anomaly_statistics(self, use_fhir: bool = True) -> Dict:
        """
        Get anomaly detection statistics from both local and FHIR sources
        
        Args:
            use_fhir: Whether to include FHIR statistics
            
        Returns:
            Combined statistics
        """
        try:
            # Get local statistics
            local_stats = {
                'model_loaded': self.inference_engine.is_model_loaded(),
                'model_type': 'ClaimsAnomaly ML Model',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Get FHIR statistics if requested
            fhir_stats = None
            if use_fhir:
                try:
                    async with self.claims_client as client:
                        fhir_stats = await client.get_claims_stats()
                except Exception as e:
                    logger.warning(f"Could not get FHIR stats: {e}")
                    fhir_stats = {'error': str(e)}
            
            return {
                'local_stats': local_stats,
                'fhir_stats': fhir_stats,
                'combined': {
                    'total_sources': 2 if fhir_stats else 1,
                    'integration_status': 'healthy' if fhir_stats else 'degraded'
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting anomaly statistics: {e}")
            return {
                'local_stats': {'error': str(e)},
                'fhir_stats': None,
                'combined': {
                    'total_sources': 0,
                    'integration_status': 'error'
                }
            }
    
    async def health_check(self) -> Dict:
        """
        Check health of both local ML system and Claims service integration
        
        Returns:
            Health status
        """
        try:
            # Check local ML system
            local_health = {
                'status': 'healthy' if self.inference_engine.is_model_loaded() else 'unhealthy',
                'model_loaded': self.inference_engine.is_model_loaded(),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Check Claims service
            async with self.claims_client as client:
                fhir_health = await client.health_check()
            
            return {
                'local': local_health,
                'fhir': fhir_health,
                'overall_status': 'healthy' if (
                    local_health['status'] == 'healthy' and 
                    fhir_health.get('status') == 'healthy'
                ) else 'degraded'
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                'local': {'status': 'error', 'error': str(e)},
                'fhir': {'status': 'unknown'},
                'overall_status': 'error'
            }
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded ML model
        
        Returns:
            Model information
        """
        try:
            model_info = self.inference_engine.get_model_info()
            model_info.update({
                'integration_enabled': True,
                'claims_service_url': self.claims_service_url,
                'enhanced_features': [
                    'FHIR Integration',
                    'Batch Processing',
                    'Real-time Scoring',
                    'Service Health Monitoring'
                ]
            })
            return model_info
            
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {
                'error': str(e),
                'integration_enabled': True,
                'claims_service_url': self.claims_service_url
            }
    
    async def validate_claim_data(self, claim_data: Dict) -> Dict:
        """
        Validate claim data for both ML scoring and FHIR storage
        
        Args:
            claim_data: Claim data to validate
            
        Returns:
            Validation results
        """
        try:
            # ML validation
            ml_validation = self.inference_engine.validate_claim_data(claim_data)
            
            # FHIR validation
            fhir_validation = None
            try:
                fhir_claim_data = self.transformer.anomaly_claim_to_fhir(claim_data)
                fhir_validation = {
                    'status': 'valid',
                    'message': 'FHIR transformation successful',
                    'fhir_data': fhir_claim_data
                }
            except Exception as e:
                fhir_validation = {
                    'status': 'invalid',
                    'message': f'FHIR transformation failed: {e}'
                }
            
            return {
                'claim_id': claim_data.get('claim_id', 'unknown'),
                'ml_validation': ml_validation,
                'fhir_validation': fhir_validation,
                'overall_status': 'valid' if (
                    ml_validation.get('is_valid', False) and 
                    fhir_validation.get('status') == 'valid'
                ) else 'invalid',
                'validated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error validating claim data: {e}")
            return {
                'claim_id': claim_data.get('claim_id', 'unknown'),
                'ml_validation': {'status': 'error', 'message': str(e)},
                'fhir_validation': None,
                'overall_status': 'error',
                'validated_at': datetime.utcnow().isoformat()
            } 