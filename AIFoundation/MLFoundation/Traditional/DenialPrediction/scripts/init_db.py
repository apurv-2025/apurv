#!/usr/bin/env python3
"""
Database initialization script
Creates tables and populates with sample data
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import numpy as np

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import create_tables, SessionLocal, Claim, Provider, Payer
from models.denial_predictor import train_demo_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_data():
    """Create sample data for testing"""
    db = SessionLocal()
    try:
        # Create sample providers
        providers = [
            Provider(
                provider_id="PROV_001",
                name="Dr. John Smith",
                specialty="Cardiology",
                state="CA",
                zip_code="90210",
                historical_denial_rate=0.12,
                avg_claim_amount=2500.0
            ),
            Provider(
                provider_id="PROV_002",
                name="Dr. Jane Doe",
                specialty="Orthopedics",
                state="NY",
                zip_code="10001",
                historical_denial_rate=0.18,
                avg_claim_amount=3500.0
            ),
            Provider(
                provider_id="PROV_003",
                name="Dr. Bob Johnson",
                specialty="Primary Care",
                state="TX",
                zip_code="75001",
                historical_denial_rate=0.08,
                avg_claim_amount=1500.0
            )
        ]
        
        for provider in providers:
            db.merge(provider)
        
        # Create sample payers
        payers = [
            Payer(
                payer_id="PAY_001",
                name="Medicare",
                type="medicare",
                state="CA",
                avg_days_to_pay=20,
                denial_rate=0.10
            ),
            Payer(
                payer_id="PAY_002",
                name="Aetna",
                type="commercial",
                state="NY",
                avg_days_to_pay=25,
                denial_rate=0.15
            ),
            Payer(
                payer_id="PAY_003",
                name="Blue Cross Blue Shield",
                type="commercial",
                state="TX",
                avg_days_to_pay=30,
                denial_rate=0.12
            )
        ]
        
        for payer in payers:
            db.merge(payer)
        
        # Create sample claims
        claims = []
        np.random.seed(42)  # For reproducible results
        
        for i in range(100):
            # Random provider and payer
            provider_id = f"PROV_{np.random.randint(1, 4):03d}"
            payer_id = f"PAY_{np.random.randint(1, 4):03d}"
            
            # Random claim data
            claim_amount = np.random.lognormal(7, 0.5)  # Log-normal distribution
            patient_age = np.random.randint(18, 85)
            patient_gender = np.random.choice(["M", "F"])
            
            # Random service date (last 6 months)
            service_date = datetime.now() - timedelta(days=np.random.randint(0, 180))
            submission_date = service_date + timedelta(days=np.random.randint(1, 30))
            
            # Random CPT and ICD codes
            cpt_codes = [f"{np.random.randint(99200, 99300)}"]
            icd_codes = [f"Z{np.random.randint(10, 99)}.{np.random.randint(0, 9)}"]
            
            # Random denial outcome
            is_denied = np.random.choice([True, False], p=[0.15, 0.85])
            
            claim = Claim(
                claim_id=f"CLM_{i+1:06d}",
                provider_id=provider_id,
                payer_id=payer_id,
                patient_id=f"PAT_{np.random.randint(1000, 9999)}",
                cpt_codes=cpt_codes,
                icd_codes=icd_codes,
                claim_amount=claim_amount,
                service_date=service_date,
                submission_date=submission_date,
                patient_age=patient_age,
                patient_gender=patient_gender,
                authorization_number=f"AUTH_{np.random.randint(1000, 9999)}" if np.random.random() > 0.3 else None,
                modifiers=[],
                place_of_service="11",
                is_denied=is_denied,
                denial_date=submission_date + timedelta(days=np.random.randint(1, 15)) if is_denied else None,
                denial_codes=["CO_16", "CO_18"] if is_denied else None,
                denial_reason="Missing authorization" if is_denied else None
            )
            claims.append(claim)
        
        for claim in claims:
            db.merge(claim)
        
        db.commit()
        logger.info(f"Created {len(providers)} providers, {len(payers)} payers, and {len(claims)} claims")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating sample data: {e}")
        raise
    finally:
        db.close()

def main():
    """Main initialization function"""
    logger.info("Starting database initialization...")
    
    try:
        # Create tables
        create_tables()
        logger.info("Database tables created successfully")
        
        # Create sample data
        create_sample_data()
        logger.info("Sample data created successfully")
        
        # Train demo model
        logger.info("Training demo model...")
        model = train_demo_model()
        logger.info("Demo model trained successfully")
        
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 