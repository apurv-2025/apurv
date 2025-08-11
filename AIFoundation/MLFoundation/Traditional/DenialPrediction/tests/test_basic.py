#!/usr/bin/env python3
"""
Basic tests for the healthcare denial prediction system
"""

import sys
import os
import pytest
import requests
import time
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import SessionLocal, Claim
from models.denial_predictor import DenialPredictor
from features.feature_engineering import FeatureEngineer

class TestBasicFunctionality:
    """Basic functionality tests"""
    
    def test_database_connection(self):
        """Test database connection"""
        try:
            from sqlalchemy import text
            db = SessionLocal()
            # Try a simple query
            result = db.execute(text("SELECT 1")).fetchone()
            assert result[0] == 1
            db.close()
            print("✅ Database connection test passed")
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")
    
    def test_feature_engineering(self):
        """Test feature engineering"""
        try:
            feature_engineer = FeatureEngineer()
            
            # Create a sample claim for testing
            from models.database import Claim
            sample_claim = Claim(
                claim_id="TEST_001",
                provider_id="PROV_001",
                payer_id="PAY_001",
                patient_id="PAT_001",
                cpt_codes=["99213"],
                icd_codes=["Z00.00"],
                claim_amount=1500.0,
                service_date=datetime.now(),
                submission_date=datetime.now(),
                patient_age=45,
                patient_gender="M",
                authorization_number="AUTH_001",
                modifiers=[],
                place_of_service="11"
            )
            
            # Test feature creation
            features = feature_engineer._create_claim_features(sample_claim)
            assert isinstance(features, dict)
            assert "claim_amount_log" in features
            assert "patient_age" in features
            assert "has_authorization" in features
            
            print("✅ Feature engineering test passed")
            
        except Exception as e:
            pytest.fail(f"Feature engineering test failed: {e}")
    
    def test_model_training(self):
        """Test model training with synthetic data"""
        try:
            import numpy as np
            import pandas as pd
            
            # Create synthetic data
            np.random.seed(42)
            n_samples = 100
            
            data = {
                'provider_historical_denial_rate': np.random.beta(2, 8, n_samples),
                'payer_denial_rate': np.random.beta(2, 6, n_samples),
                'claim_amount_log': np.random.normal(7, 1, n_samples),
                'patient_age': np.random.normal(50, 20, n_samples),
                'has_authorization': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
                'number_of_cpt_codes': np.random.poisson(2, n_samples),
                'high_dollar_claim': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
                'weekend_service': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
                'payer_type_medicare': np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
            }
            
            X = pd.DataFrame(data)
            
            # Create synthetic target
            denial_prob = (
                0.1 +
                0.3 * (1 - X['has_authorization']) +
                0.2 * X['high_dollar_claim'] +
                0.1 * X['provider_historical_denial_rate'] +
                0.1 * X['payer_denial_rate']
            )
            denial_prob += np.random.normal(0, 0.05, n_samples)
            denial_prob = np.clip(denial_prob, 0, 1)
            y = (denial_prob > 0.5).astype(int)
            
            # Train model
            predictor = DenialPredictor("test_model")
            metrics = predictor.train(X, y)
            
            # Check metrics
            assert "test_auc" in metrics
            assert metrics["test_auc"] > 0.5  # Should be better than random
            
            print("✅ Model training test passed")
            
        except Exception as e:
            pytest.fail(f"Model training test failed: {e}")

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.token = "demo_token_123"
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            print("✅ Health endpoint test passed")
        except Exception as e:
            pytest.fail(f"Health endpoint test failed: {e}")
    
    def test_prediction_endpoint(self):
        """Test prediction endpoint"""
        try:
            claim_data = {
                "claim_id": "TEST_001",
                "provider_id": "PROV_001",
                "payer_id": "PAY_001",
                "patient_id": "PAT_001",
                "cpt_codes": ["99213"],
                "icd_codes": ["Z00.00"],
                "claim_amount": 1500.0,
                "service_date": datetime.now().date().isoformat(),
                "patient_age": 45,
                "patient_gender": "M",
                "place_of_service": "11"
            }
            
            response = requests.post(
                f"{self.base_url}/predict",
                json=claim_data,
                headers=self.headers,
                timeout=30
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "denial_probability" in data
            assert "risk_level" in data
            assert "top_risk_factors" in data
            
            print("✅ Prediction endpoint test passed")
            
        except Exception as e:
            pytest.fail(f"Prediction endpoint test failed: {e}")

def run_basic_tests():
    """Run basic tests"""
    print("🧪 Running basic functionality tests...")
    
    # Test basic functionality
    basic_tests = TestBasicFunctionality()
    
    try:
        basic_tests.test_database_connection()
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
    
    try:
        basic_tests.test_feature_engineering()
    except Exception as e:
        print(f"❌ Feature engineering test failed: {e}")
    
    try:
        basic_tests.test_model_training()
    except Exception as e:
        print(f"❌ Model training test failed: {e}")
    
    print("\n🧪 Running API tests...")
    
    # Test API endpoints
    api_tests = TestAPIEndpoints()
    
    try:
        api_tests.test_health_endpoint()
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
    
    try:
        api_tests.test_prediction_endpoint()
    except Exception as e:
        print(f"❌ Prediction endpoint test failed: {e}")
    
    print("\n✅ Basic tests completed!")

if __name__ == "__main__":
    run_basic_tests() 