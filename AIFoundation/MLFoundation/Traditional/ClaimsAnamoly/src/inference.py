"""
Claims Inference Engine Module

This module provides the production inference engine for real-time claim scoring.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import joblib
import logging
from typing import Dict, List, Tuple, Any
from src.models import ClaimsAnomalyDetector

logger = logging.getLogger(__name__)


class ClaimsInferenceEngine:
    """Production inference engine for real-time claim scoring"""
    
    def __init__(self, model_path=None):
        self.model = ClaimsAnomalyDetector()
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load trained model from disk"""
        model_data = joblib.load(model_path)
        self.model = model_data['model']
        logger.info(f"Model loaded from {model_path}")
    
    def save_model(self, model_path):
        """Save trained model to disk"""
        model_data = {
            'model': self.model,
            'version': '1.0',
            'training_date': datetime.now().isoformat()
        }
        joblib.dump(model_data, model_path)
        logger.info(f"Model saved to {model_path}")
    
    def score_claims_batch(self, claims_df):
        """Score a batch of claims"""
        
        if not self.model.is_trained:
            raise ValueError("Model must be trained before scoring claims")
        
        predictions = self.model.predict(claims_df)
        
        # Create results DataFrame
        results_df = pd.DataFrame(predictions)
        results_df['timestamp'] = datetime.now().isoformat()
        
        return results_df
    
    def score_single_claim(self, claim_data):
        """Score a single claim"""
        
        claim_df = pd.DataFrame([claim_data])
        results = self.score_claims_batch(claim_df)
        
        return results.iloc[0].to_dict()
    
    def get_model_info(self):
        """Get information about the loaded model"""
        
        return {
            'is_trained': self.model.is_trained,
            'feature_columns': self.model.feature_columns if hasattr(self.model, 'feature_columns') else None,
            'model_type': 'Ensemble (Isolation Forest + Random Forest)',
            'last_updated': datetime.now().isoformat()
        } 