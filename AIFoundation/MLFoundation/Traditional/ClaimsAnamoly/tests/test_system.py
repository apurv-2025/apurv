"""
Unit tests for the Claims Anomaly Detection System

This module contains comprehensive tests for all components of the system.
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
import sys
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.data_generator import SyntheticClaimsDataGenerator
from src.models import ClaimsAnomalyDetector
from src.inference import ClaimsInferenceEngine


class TestSyntheticClaimsDataGenerator:
    """Test cases for the synthetic data generator"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.generator = SyntheticClaimsDataGenerator(seed=42)
    
    def test_generator_initialization(self):
        """Test that generator initializes correctly"""
        assert self.generator is not None
        assert len(self.generator.cpt_codes) > 0
        assert len(self.generator.icd_codes) > 0
        assert len(self.generator.provider_specialties) > 0
        assert len(self.generator.fee_schedule) > 0
    
    def test_generate_claims_data(self):
        """Test claims data generation"""
        df = self.generator.generate_claims_data(n_claims=100, anomaly_rate=0.1)
        
        # Check basic structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 100
        assert 'claim_id' in df.columns
        assert 'is_anomaly' in df.columns
        
        # Check anomaly rate
        actual_anomaly_rate = df['is_anomaly'].mean()
        assert abs(actual_anomaly_rate - 0.1) < 0.05  # Allow some variance
    
    def test_required_fields_present(self):
        """Test that all required fields are present in generated data"""
        df = self.generator.generate_claims_data(n_claims=50)
        
        required_fields = [
            'claim_id', 'submission_date', 'provider_id', 'provider_specialty',
            'patient_age', 'patient_gender', 'cpt_code', 'icd_code',
            'units_of_service', 'billed_amount', 'paid_amount',
            'place_of_service', 'prior_authorization', 'modifier', 'is_anomaly'
        ]
        
        for field in required_fields:
            assert field in df.columns, f"Missing required field: {field}"
    
    def test_data_quality(self):
        """Test data quality constraints"""
        df = self.generator.generate_claims_data(n_claims=200)
        
        # Check for missing values in critical fields
        critical_fields = ['claim_id', 'billed_amount', 'provider_id']
        for field in critical_fields:
            assert df[field].isna().sum() == 0, f"Critical field {field} has missing values"
        
        # Check data types
        assert df['billed_amount'].dtype in ['float64', 'float32']
        assert df['patient_age'].dtype in ['int64', 'int32']
        assert df['is_anomaly'].dtype in ['int64', 'int32']
        
        # Check value ranges
        assert df['billed_amount'].min() > 0
        assert df['patient_age'].min() >= 18
        assert df['patient_age'].max() <= 85


class TestClaimsAnomalyDetector:
    """Test cases for the anomaly detection model"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.model = ClaimsAnomalyDetector()
        self.generator = SyntheticClaimsDataGenerator(seed=42)
        self.test_data = self.generator.generate_claims_data(n_claims=200, anomaly_rate=0.1)
    
    def test_model_initialization(self):
        """Test that model initializes correctly"""
        assert self.model is not None
        assert not self.model.is_trained
        assert len(self.model.feature_columns) == 0
    
    def test_feature_preparation(self):
        """Test feature engineering"""
        features = self.model.prepare_features(self.test_data)
        
        assert isinstance(features, pd.DataFrame)
        assert len(features) == len(self.test_data)
        assert len(features.columns) > 0
        
        # Check that no infinite values
        assert not np.isinf(features.values).any()
        
        # Check that no NaN values after fillna
        assert not features.isna().any().any()
    
    def test_model_training(self):
        """Test model training"""
        training_results = self.model.train(self.test_data)
        
        assert self.model.is_trained
        assert len(self.model.feature_columns) > 0
        assert 'X_test' in training_results
        assert 'y_test' in training_results
        assert 'feature_names' in training_results
    
    def test_predictions(self):
        """Test model predictions"""
        # Train the model first
        self.model.train(self.test_data)
        
        # Test predictions
        predictions = self.model.predict(self.test_data.head(10))
        
        assert isinstance(predictions, list)
        assert len(predictions) == 10
        
        # Check prediction structure
        for pred in predictions:
            assert 'claim_id' in pred
            assert 'risk_score' in pred
            assert 'classification' in pred
            assert 'top_drivers' in pred
            
            # Check value ranges
            assert 0 <= pred['risk_score'] <= 100
            assert pred['classification'] in ['Normal', 'Suspicious', 'High Risk']
            assert isinstance(pred['top_drivers'], list)
    
    def test_untrained_model_error(self):
        """Test that untrained model raises error on prediction"""
        with pytest.raises(ValueError, match="Model must be trained"):
            self.model.predict(self.test_data.head(5))


class TestClaimsInferenceEngine:
    """Test cases for the inference engine"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.generator = SyntheticClaimsDataGenerator(seed=42)
        self.test_data = self.generator.generate_claims_data(n_claims=100, anomaly_rate=0.1)
        
        # Train a model
        self.model = ClaimsAnomalyDetector()
        self.model.train(self.test_data)
        
        # Set up inference engine
        self.engine = ClaimsInferenceEngine()
        self.engine.model = self.model
    
    def test_engine_initialization(self):
        """Test inference engine initialization"""
        engine = ClaimsInferenceEngine()
        assert engine is not None
        assert not engine.model.is_trained
    
    def test_batch_scoring(self):
        """Test batch claim scoring"""
        results = self.engine.score_claims_batch(self.test_data.head(10))
        
        assert isinstance(results, pd.DataFrame)
        assert len(results) == 10
        assert 'claim_id' in results.columns
        assert 'risk_score' in results.columns
        assert 'classification' in results.columns
        assert 'timestamp' in results.columns
    
    def test_single_claim_scoring(self):
        """Test single claim scoring"""
        sample_claim = {
            'claim_id': 'TEST_001',
            'submission_date': '2025-08-01',
            'provider_id': 'PROV_00001',
            'provider_specialty': 'Internal Medicine',
            'patient_age': 45,
            'patient_gender': 'M',
            'cpt_code': '99214',
            'icd_code': 'I10',
            'units_of_service': 1,
            'billed_amount': 200.0,
            'paid_amount': 180.0,
            'place_of_service': '11',
            'prior_authorization': 'N',
            'modifier': '',
            'is_anomaly': 0
        }
        
        result = self.engine.score_single_claim(sample_claim)
        
        assert isinstance(result, dict)
        assert 'claim_id' in result
        assert 'risk_score' in result
        assert 'classification' in result
        assert 'top_drivers' in result
        assert 'timestamp' in result
    
    def test_model_persistence(self):
        """Test model save and load functionality"""
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp_file:
            model_path = tmp_file.name
        
        try:
            # Save model
            self.engine.save_model(model_path)
            assert os.path.exists(model_path)
            
            # Load model in new engine
            new_engine = ClaimsInferenceEngine(model_path)
            assert new_engine.model.is_trained
            
            # Test that loaded model works
            sample_claim = self.test_data.iloc[0].to_dict()
            result = new_engine.score_single_claim(sample_claim)
            assert 'risk_score' in result
            
        finally:
            # Clean up
            if os.path.exists(model_path):
                os.unlink(model_path)
    
    def test_model_info(self):
        """Test model information retrieval"""
        info = self.engine.get_model_info()
        
        assert isinstance(info, dict)
        assert 'is_trained' in info
        assert 'model_type' in info
        assert 'last_updated' in info
        assert info['is_trained'] is True
        assert 'Ensemble' in info['model_type']


class TestIntegration:
    """Integration tests for the complete system"""
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # 1. Generate data
        generator = SyntheticClaimsDataGenerator(seed=42)
        data = generator.generate_claims_data(n_claims=500, anomaly_rate=0.08)
        
        # 2. Train model
        model = ClaimsAnomalyDetector()
        training_results = model.train(data)
        
        # 3. Set up inference engine
        engine = ClaimsInferenceEngine()
        engine.model = model
        
        # 4. Test inference
        test_claims = data.head(20)
        results = engine.score_claims_batch(test_claims)
        
        # 5. Verify results
        assert len(results) == 20
        assert all(0 <= score <= 100 for score in results['risk_score'])
        assert all(classification in ['Normal', 'Suspicious', 'High Risk'] 
                  for classification in results['classification'])
    
    def test_performance_requirements(self):
        """Test that system meets basic performance requirements"""
        # Generate larger dataset for performance test
        generator = SyntheticClaimsDataGenerator(seed=42)
        data = generator.generate_claims_data(n_claims=1000, anomaly_rate=0.05)
        
        # Train model
        model = ClaimsAnomalyDetector()
        model.train(data)
        
        # Set up inference engine
        engine = ClaimsInferenceEngine()
        engine.model = model
        
        # Test processing speed
        import time
        start_time = time.time()
        results = engine.score_claims_batch(data)
        end_time = time.time()
        
        processing_time = end_time - start_time
        claims_per_second = len(data) / processing_time
        
        # Should process at least 100 claims per second
        assert claims_per_second >= 100, f"Processing speed too slow: {claims_per_second:.1f} claims/sec"
    
    def test_anomaly_detection_accuracy(self):
        """Test basic anomaly detection accuracy"""
        # Generate data with known anomalies
        generator = SyntheticClaimsDataGenerator(seed=42)
        data = generator.generate_claims_data(n_claims=1000, anomaly_rate=0.1)
        
        # Train model
        model = ClaimsAnomalyDetector()
        model.train(data)
        
        # Test predictions
        predictions = model.predict(data)
        results_df = pd.DataFrame(predictions)
        
        # Merge with original data
        test_results = data[['claim_id', 'is_anomaly']].merge(
            results_df[['claim_id', 'risk_score']], on='claim_id'
        )
        
        # Check that anomalies have higher risk scores on average
        anomaly_scores = test_results[test_results['is_anomaly'] == 1]['risk_score']
        normal_scores = test_results[test_results['is_anomaly'] == 0]['risk_score']
        
        if len(anomaly_scores) > 0 and len(normal_scores) > 0:
            assert anomaly_scores.mean() > normal_scores.mean(), \
                "Anomalies should have higher risk scores on average"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 