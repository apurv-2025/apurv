"""
Feature Engineering for Healthcare Denial Prediction
Creates features from raw claim data for ML model training and inference
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from models.database import SessionLocal, Claim, Provider, Payer
import logging

logger = logging.getLogger(__name__)

class FeatureEngineer:
    """Feature engineering for healthcare claim denial prediction"""
    
    def __init__(self):
        self.feature_definitions = {
            'provider_features': [
                'provider_historical_denial_rate',
                'provider_avg_claim_amount',
                'provider_specialty_denial_rate',
                'provider_claims_last_30_days'
            ],
            'payer_features': [
                'payer_denial_rate',
                'payer_avg_days_to_pay',
                'payer_type_encoded',
                'payer_state_denial_rate'
            ],
            'claim_features': [
                'claim_amount_normalized',
                'patient_age_group',
                'service_to_submission_days',
                'cpt_code_risk_score',
                'has_authorization',
                'number_of_cpt_codes',
                'weekend_service',
                'high_dollar_claim'
            ],
            'temporal_features': [
                'month_of_service',
                'day_of_week',
                'quarter',
                'days_since_last_claim'
            ]
        }
    
    def create_features(self, claim_id: str) -> Dict[str, Any]:
        """Create all features for a given claim"""
        db = SessionLocal()
        try:
            # Get claim data
            claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
            if not claim:
                raise ValueError(f"Claim {claim_id} not found")
            
            features = {}
            
            # Provider features
            features.update(self._create_provider_features(db, claim.provider_id))
            
            # Payer features
            features.update(self._create_payer_features(db, claim.payer_id))
            
            # Claim features
            features.update(self._create_claim_features(claim))
            
            # Temporal features
            features.update(self._create_temporal_features(claim))
            
            return features
            
        finally:
            db.close()
    
    def _create_provider_features(self, db: Session, provider_id: str) -> Dict[str, float]:
        """Create provider-specific features"""
        # Historical denial rate
        from sqlalchemy import text
        denial_rate_query = text("""
        SELECT 
            AVG(CASE WHEN is_denied THEN 1.0 ELSE 0.0 END) as denial_rate,
            AVG(claim_amount) as avg_amount,
            COUNT(*) as claim_count
        FROM claims 
        WHERE provider_id = :provider_id 
        AND submission_date >= :start_date
        """)
        
        start_date = datetime.now() - timedelta(days=365)
        result = db.execute(denial_rate_query, {
            'provider_id': provider_id,
            'start_date': start_date
        }).fetchone()
        
        return {
            'provider_historical_denial_rate': result.denial_rate if result.denial_rate else 0.1,
            'provider_avg_claim_amount': result.avg_amount if result.avg_amount else 1000.0,
            'provider_claims_last_30_days': self._get_recent_claim_count(db, provider_id, 30),
            'provider_specialty_denial_rate': self._get_specialty_denial_rate(db, provider_id)
        }
    
    def _create_payer_features(self, db: Session, payer_id: str) -> Dict[str, float]:
        """Create payer-specific features"""
        payer = db.query(Payer).filter(Payer.payer_id == payer_id).first()
        
        return {
            'payer_denial_rate': payer.denial_rate if payer else 0.15,
            'payer_avg_days_to_pay': payer.avg_days_to_pay if payer else 30.0,
            'payer_type_commercial': 1.0 if payer and payer.type == 'commercial' else 0.0,
            'payer_type_medicare': 1.0 if payer and payer.type == 'medicare' else 0.0,
            'payer_type_medicaid': 1.0 if payer and payer.type == 'medicaid' else 0.0
        }
    
    def _create_claim_features(self, claim: Claim) -> Dict[str, float]:
        """Create claim-specific features"""
        features = {
            'claim_amount_log': np.log1p(claim.claim_amount),
            'patient_age': float(claim.patient_age),
            'patient_age_squared': float(claim.patient_age) ** 2,
            'patient_gender_male': 1.0 if claim.patient_gender == 'M' else 0.0,
            'has_authorization': 1.0 if claim.authorization_number else 0.0,
            'number_of_cpt_codes': len(claim.cpt_codes) if claim.cpt_codes else 0.0,
            'number_of_icd_codes': len(claim.icd_codes) if claim.icd_codes else 0.0,
            'high_dollar_claim': 1.0 if claim.claim_amount > 10000 else 0.0
        }
        
        # Age groups
        age = claim.patient_age
        features.update({
            'age_0_17': 1.0 if age < 18 else 0.0,
            'age_18_29': 1.0 if 18 <= age < 30 else 0.0,
            'age_30_49': 1.0 if 30 <= age < 50 else 0.0,
            'age_50_64': 1.0 if 50 <= age < 65 else 0.0,
            'age_65_plus': 1.0 if age >= 65 else 0.0
        })
        
        return features
    
    def _create_temporal_features(self, claim: Claim) -> Dict[str, float]:
        """Create temporal features"""
        service_date = claim.service_date
        submission_date = claim.submission_date
        
        return {
            'month_of_service': float(service_date.month),
            'day_of_week': float(service_date.weekday()),
            'quarter': float((service_date.month - 1) // 3 + 1),
            'weekend_service': 1.0 if service_date.weekday() >= 5 else 0.0,
            'service_to_submission_days': (submission_date - service_date).days,
            'days_since_year_start': (service_date - datetime(service_date.year, 1, 1)).days
        }
    
    def _get_recent_claim_count(self, db: Session, provider_id: str, days: int) -> float:
        """Get count of recent claims for provider"""
        start_date = datetime.now() - timedelta(days=days)
        count = db.query(Claim).filter(
            Claim.provider_id == provider_id,
            Claim.submission_date >= start_date
        ).count()
        return float(count)
    
    def _get_specialty_denial_rate(self, db: Session, provider_id: str) -> float:
        """Get denial rate for provider's specialty"""
        # Simplified - would join with provider specialty
        return 0.12  # Default specialty denial rate
    
    def create_batch_features(self, claim_ids: List[str]) -> pd.DataFrame:
        """Create features for multiple claims"""
        features_list = []
        
        for claim_id in claim_ids:
            try:
                features = self.create_features(claim_id)
                features['claim_id'] = claim_id
                features_list.append(features)
            except Exception as e:
                logger.warning(f"Error creating features for claim {claim_id}: {e}")
                continue
        
        if not features_list:
            raise ValueError("No valid features created")
        
        return pd.DataFrame(features_list)
    
    def get_feature_names(self) -> List[str]:
        """Get list of all feature names"""
        all_features = []
        for feature_group in self.feature_definitions.values():
            all_features.extend(feature_group)
        return all_features
    
    def validate_features(self, features: Dict[str, Any]) -> bool:
        """Validate that all required features are present and valid"""
        required_features = self.get_feature_names()
        
        for feature in required_features:
            if feature not in features:
                logger.warning(f"Missing required feature: {feature}")
                return False
            
            value = features[feature]
            if not isinstance(value, (int, float)) or np.isnan(value):
                logger.warning(f"Invalid feature value for {feature}: {value}")
                return False
        
        return True
    
    def normalize_features(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """Normalize features for model input"""
        # Log transform for amount features
        amount_features = ['claim_amount_log', 'provider_avg_claim_amount']
        for feature in amount_features:
            if feature in features_df.columns:
                features_df[feature] = np.log1p(features_df[feature])
        
        # Clip extreme values
        numeric_features = features_df.select_dtypes(include=[np.number]).columns
        for feature in numeric_features:
            if feature != 'claim_id':  # Skip ID columns
                q1 = features_df[feature].quantile(0.01)
                q99 = features_df[feature].quantile(0.99)
                features_df[feature] = features_df[feature].clip(q1, q99)
        
        return features_df
    
    def create_interaction_features(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features"""
        # Provider-Payer interaction
        if 'provider_historical_denial_rate' in features_df.columns and 'payer_denial_rate' in features_df.columns:
            features_df['provider_payer_risk'] = (
                features_df['provider_historical_denial_rate'] * features_df['payer_denial_rate']
            )
        
        # Amount-Authorization interaction
        if 'claim_amount_log' in features_df.columns and 'has_authorization' in features_df.columns:
            features_df['amount_no_auth_risk'] = (
                features_df['claim_amount_log'] * (1 - features_df['has_authorization'])
            )
        
        # Age-Gender interaction
        if 'patient_age' in features_df.columns and 'patient_gender_male' in features_df.columns:
            features_df['age_gender_interaction'] = features_df['patient_age'] * features_df['patient_gender_male']
        
        return features_df

def create_demo_features():
    """Create demo features for testing"""
    # Create a sample claim
    sample_claim = Claim(
        claim_id="DEMO_001",
        provider_id="PROV_123",
        payer_id="PAY_456",
        patient_id="PAT_789",
        cpt_codes=["99213", "90834"],
        icd_codes=["F32.9", "Z00.00"],
        claim_amount=1500.0,
        service_date=datetime.now(),
        submission_date=datetime.now(),
        patient_age=45,
        patient_gender="M",
        authorization_number="AUTH_123",
        modifiers=["25"],
        place_of_service="11"
    )
    
    # Create features
    feature_engineer = FeatureEngineer()
    
    # Mock database session
    class MockSession:
        def query(self, model):
            return self
        
        def filter(self, condition):
            return self
        
        def first(self):
            if 'provider' in str(condition):
                return Provider(
                    provider_id="PROV_123",
                    historical_denial_rate=0.15,
                    avg_claim_amount=2000.0
                )
            elif 'payer' in str(condition):
                return Payer(
                    payer_id="PAY_456",
                    denial_rate=0.12,
                    avg_days_to_pay=25,
                    type="commercial"
                )
            return None
        
        def execute(self, query, params):
            class MockResult:
                def fetchone(self):
                    class MockRow:
                        denial_rate = 0.15
                        avg_amount = 2000.0
                        claim_count = 100
                    return MockRow()
            return MockResult()
    
    # Create features with mock session
    features = feature_engineer._create_claim_features(sample_claim)
    features.update(feature_engineer._create_temporal_features(sample_claim))
    
    # Add mock provider and payer features
    features.update({
        'provider_historical_denial_rate': 0.15,
        'provider_avg_claim_amount': 2000.0,
        'provider_claims_last_30_days': 10.0,
        'provider_specialty_denial_rate': 0.12,
        'payer_denial_rate': 0.12,
        'payer_avg_days_to_pay': 25.0,
        'payer_type_commercial': 1.0,
        'payer_type_medicare': 0.0,
        'payer_type_medicaid': 0.0
    })
    
    return features

if __name__ == "__main__":
    # Test feature engineering
    demo_features = create_demo_features()
    print("Demo features created:")
    for feature, value in demo_features.items():
        print(f"  {feature}: {value}") 