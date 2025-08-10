#!/usr/bin/env python3
"""
Example Usage of Claims Anomaly Detection System

This script demonstrates how to use the system for real-world scenarios.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data_generator import SyntheticClaimsDataGenerator
from src.models import ClaimsAnomalyDetector
from src.inference import ClaimsInferenceEngine


def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    # 1. Generate some test data
    generator = SyntheticClaimsDataGenerator(seed=42)
    data = generator.generate_claims_data(n_claims=1000, anomaly_rate=0.1)
    
    print(f"Generated {len(data)} claims with {data['is_anomaly'].sum()} anomalies")
    
    # 2. Train the model
    model = ClaimsAnomalyDetector()
    model.train(data)
    
    print(f"Model trained with {len(model.feature_columns)} features")
    
    # 3. Set up inference engine
    engine = ClaimsInferenceEngine()
    engine.model = model
    
    # 4. Score some claims
    test_claims = data.head(5)
    results = engine.score_claims_batch(test_claims)
    
    print("\nSample Results:")
    for _, row in results.iterrows():
        print(f"Claim {row['claim_id']}: {row['risk_score']}/100 ({row['classification']})")
    
    return engine


def example_single_claim():
    """Example of scoring a single claim"""
    print("\n=== Single Claim Scoring Example ===")
    
    # Load a trained model (or train one)
    engine = example_basic_usage()
    
    # Example claim data
    claim = {
        'claim_id': 'EXAMPLE_001',
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
        'is_anomaly': 0  # Unknown in real scenario
    }
    
    # Score the claim
    result = engine.score_single_claim(claim)
    
    print(f"Claim {result['claim_id']}: {result['risk_score']}/100")
    print(f"Classification: {result['classification']}")
    print(f"Top Risk Drivers: {', '.join(result['top_drivers'][:3])}")


def example_suspicious_claim():
    """Example of scoring a suspicious claim"""
    print("\n=== Suspicious Claim Example ===")
    
    # Load a trained model
    engine = example_basic_usage()
    
    # Suspicious claim (high billing amount)
    suspicious_claim = {
        'claim_id': 'SUSPICIOUS_001',
        'submission_date': '2025-08-01',
        'provider_id': 'PROV_00002',
        'provider_specialty': 'Internal Medicine',
        'patient_age': 35,
        'patient_gender': 'F',
        'cpt_code': '99214',
        'icd_code': 'I10',
        'units_of_service': 1,
        'billed_amount': 1500.0,  # Suspiciously high
        'paid_amount': 200.0,
        'place_of_service': '11',
        'prior_authorization': 'N',
        'modifier': '',
        'is_anomaly': 0
    }
    
    # Score the suspicious claim
    result = engine.score_single_claim(suspicious_claim)
    
    print(f"Claim {result['claim_id']}: {result['risk_score']}/100")
    print(f"Classification: {result['classification']}")
    print(f"Top Risk Drivers: {', '.join(result['top_drivers'][:3])}")


def example_model_persistence():
    """Example of saving and loading models"""
    print("\n=== Model Persistence Example ===")
    
    # Train a model
    generator = SyntheticClaimsDataGenerator(seed=42)
    data = generator.generate_claims_data(n_claims=500, anomaly_rate=0.1)
    
    model = ClaimsAnomalyDetector()
    model.train(data)
    
    # Set up engine and save model
    engine = ClaimsInferenceEngine()
    engine.model = model
    
    model_path = "models/example_model.pkl"
    engine.save_model(model_path)
    print(f"Model saved to {model_path}")
    
    # Load model in new engine
    new_engine = ClaimsInferenceEngine(model_path)
    print("Model loaded successfully")
    
    # Test loaded model
    test_claim = data.iloc[0].to_dict()
    result = new_engine.score_single_claim(test_claim)
    print(f"Loaded model prediction: {result['risk_score']}/100")


if __name__ == "__main__":
    print("Claims Anomaly Detection System - Example Usage")
    print("=" * 60)
    
    try:
        example_basic_usage()
        example_single_claim()
        example_suspicious_claim()
        example_model_persistence()
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        import traceback
        traceback.print_exc() 