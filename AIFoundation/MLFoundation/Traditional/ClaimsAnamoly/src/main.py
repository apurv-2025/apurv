"""
Main execution module for the Claims Anomaly Detection System

This module demonstrates the complete anomaly detection system with synthetic data generation,
model training, and inference capabilities.
"""

import logging
import warnings
from datetime import datetime
from src.data_generator import SyntheticClaimsDataGenerator
from src.models import ClaimsAnomalyDetector
from src.inference import ClaimsInferenceEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Suppress warnings
warnings.filterwarnings('ignore')


def main():
    """Demonstrate the complete anomaly detection system"""
    
    logger.info("Starting Health Insurance Claims Anomaly Detection System Demo")
    
    # 1. Generate synthetic data
    logger.info("=== Step 1: Generating Synthetic Claims Data ===")
    data_generator = SyntheticClaimsDataGenerator()
    claims_df = data_generator.generate_claims_data(n_claims=5000, anomaly_rate=0.08)
    
    print(f"Dataset shape: {claims_df.shape}")
    print(f"Anomaly distribution:\n{claims_df['is_anomaly'].value_counts()}")
    print(f"\nSample claims data:")
    print(claims_df.head())
    
    # 2. Train the model
    logger.info("\n=== Step 2: Training Anomaly Detection Model ===")
    model = ClaimsAnomalyDetector()
    training_results = model.train(claims_df)
    
    # 3. Set up inference engine
    logger.info("\n=== Step 3: Setting up Inference Engine ===")
    inference_engine = ClaimsInferenceEngine()
    inference_engine.model = model
    
    # Save the model
    model_path = "models/claims_anomaly_model.pkl"
    inference_engine.save_model(model_path)
    
    # 4. Demonstrate inference on new claims
    logger.info("\n=== Step 4: Demonstrating Inference ===")
    
    # Generate some test claims
    test_claims = data_generator.generate_claims_data(n_claims=10, anomaly_rate=0.3)
    
    # Score the test claims
    results = inference_engine.score_claims_batch(test_claims)
    
    print("\nInference Results:")
    for _, row in results.iterrows():
        claim_id = row['claim_id']
        score = row['risk_score']
        classification = row['classification']
        print(f"Claim {claim_id}: {score}/100 ({classification})")
    
    # 5. API-style single claim scoring example
    logger.info("\n=== Step 5: Single Claim Scoring Example ===")
    
    sample_claim = {
        'claim_id': 'CLM_API_001',
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
    
    single_result = inference_engine.score_single_claim(sample_claim)
    print(f"\nSingle claim scoring result:")
    print(f"Risk Score: {single_result['risk_score']}/100")
    print(f"Classification: {single_result['classification']}")
    print(f"Top Risk Drivers: {', '.join(single_result['top_drivers'][:3])}")
    
    # 6. Model information
    model_info = inference_engine.get_model_info()
    print(f"\nModel Information:")
    print(f"Model Type: {model_info['model_type']}")
    print(f"Is Trained: {model_info['is_trained']}")
    print(f"Number of Features: {len(model_info['feature_columns']) if model_info['feature_columns'] else 0}")
    
    logger.info("Demo completed successfully!")


if __name__ == "__main__":
    main() 