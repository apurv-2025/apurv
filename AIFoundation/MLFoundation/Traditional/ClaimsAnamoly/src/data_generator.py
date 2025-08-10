"""
Synthetic Claims Data Generator Module

This module provides functionality to generate realistic synthetic health insurance claims data
for testing and development of anomaly detection systems.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import logging
from typing import Dict, List, Tuple, Any

logger = logging.getLogger(__name__)


class SyntheticClaimsDataGenerator:
    """Generate realistic synthetic health insurance claims data"""
    
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        
        # Reference data for realistic generation
        self.cpt_codes = [
            '99213', '99214', '99215', '99203', '99204', '99205',  # Office visits
            '73721', '73722', '73723', '70450', '70460',  # Imaging
            '80053', '80061', '85025', '84443', '84439',  # Lab tests
            '29881', '64721', '47562', '43239', '45378'   # Procedures
        ]
        
        self.icd_codes = [
            'Z00.00', 'I10', 'E11.9', 'M79.3', 'J44.1',  # Common diagnoses
            'F32.9', 'K21.9', 'N39.0', 'M25.511', 'H52.4'
        ]
        
        self.provider_specialties = [
            'Internal Medicine', 'Family Medicine', 'Cardiology', 
            'Orthopedics', 'Radiology', 'Pathology', 'Emergency Medicine'
        ]
        
        # Fee schedules (simplified)
        self.fee_schedule = {
            '99213': 150, '99214': 200, '99215': 250, '99203': 180, '99204': 240, '99205': 300,
            '73721': 300, '73722': 350, '73723': 400, '70450': 500, '70460': 600,
            '80053': 75, '80061': 100, '85025': 50, '84443': 80, '84439': 85,
            '29881': 1200, '64721': 800, '47562': 2500, '43239': 600, '45378': 1000
        }
    
    def generate_claims_data(self, n_claims=10000, anomaly_rate=0.05):
        """Generate synthetic claims dataset with controlled anomalies"""
        
        claims = []
        n_anomalies = int(n_claims * anomaly_rate)
        n_normal = n_claims - n_anomalies
        
        # Generate provider IDs and their characteristics
        provider_ids = [f"PROV_{i:05d}" for i in range(1, 501)]
        provider_data = {}
        
        for prov_id in provider_ids:
            provider_data[prov_id] = {
                'specialty': random.choice(self.provider_specialties),
                'years_active': random.randint(1, 20),
                'avg_monthly_claims': random.randint(10, 200),
                'fraud_history': random.choice([True, False]) if random.random() < 0.02 else False
            }
        
        # Generate normal claims
        for i in range(n_normal):
            claim = self._generate_normal_claim(i, provider_ids, provider_data)
            claims.append(claim)
        
        # Generate anomalous claims
        for i in range(n_anomalies):
            claim = self._generate_anomalous_claim(n_normal + i, provider_ids, provider_data)
            claims.append(claim)
        
        df = pd.DataFrame(claims)
        
        # Shuffle the dataset
        df = df.sample(frac=1).reset_index(drop=True)
        
        logger.info(f"Generated {len(df)} claims with {n_anomalies} anomalies ({anomaly_rate:.1%})")
        return df
    
    def _generate_normal_claim(self, claim_id, provider_ids, provider_data):
        """Generate a normal claim"""
        
        provider_id = random.choice(provider_ids)
        provider_info = provider_data[provider_id]
        
        cpt_code = random.choice(self.cpt_codes)
        base_amount = self.fee_schedule.get(cpt_code, 100)
        
        # Add some natural variation
        billed_amount = base_amount * random.uniform(0.9, 1.1)
        
        claim = {
            'claim_id': f"CLM_{claim_id:08d}",
            'submission_date': self._random_date(),
            'provider_id': provider_id,
            'provider_specialty': provider_info['specialty'],
            'patient_age': random.randint(18, 85),
            'patient_gender': random.choice(['M', 'F']),
            'cpt_code': cpt_code,
            'icd_code': random.choice(self.icd_codes),
            'units_of_service': random.randint(1, 3),
            'billed_amount': round(billed_amount, 2),
            'place_of_service': random.choice(['11', '22', '23', '81']),  # Office, Outpatient, Emergency, Lab
            'prior_authorization': random.choice(['Y', 'N']),
            'modifier': random.choice(['', '25', '59', 'TC']) if random.random() < 0.3 else '',
            'is_anomaly': 0
        }
        
        # Set paid amount (normally close to billed amount)
        claim['paid_amount'] = claim['billed_amount'] * random.uniform(0.85, 1.0)
        
        return claim
    
    def _generate_anomalous_claim(self, claim_id, provider_ids, provider_data):
        """Generate an anomalous claim with various types of anomalies"""
        
        # Start with a normal claim
        claim = self._generate_normal_claim(claim_id, provider_ids, provider_data)
        
        # Apply different types of anomalies
        anomaly_type = random.choice([
            'overbilling', 'unusual_frequency', 'code_mismatch', 
            'excessive_units', 'geographic_anomaly', 'bundling_violation'
        ])
        
        if anomaly_type == 'overbilling':
            # Significantly higher billing than usual
            claim['billed_amount'] *= random.uniform(2.0, 5.0)
            
        elif anomaly_type == 'unusual_frequency':
            # Same procedure multiple times (simulate by adding flag)
            claim['units_of_service'] = random.randint(10, 50)
            
        elif anomaly_type == 'code_mismatch':
            # Inappropriate code for specialty
            if claim['provider_specialty'] == 'Radiology':
                claim['cpt_code'] = '29881'  # Orthopedic procedure
            elif claim['provider_specialty'] == 'Internal Medicine':
                claim['cpt_code'] = '47562'  # Surgery
                
        elif anomaly_type == 'excessive_units':
            claim['units_of_service'] = random.randint(20, 100)
            claim['billed_amount'] *= claim['units_of_service']
            
        elif anomaly_type == 'geographic_anomaly':
            # Unusual place of service for procedure
            if claim['cpt_code'] in ['47562', '29881']:  # Surgical procedures
                claim['place_of_service'] = '11'  # Office (unusual for surgery)
                
        elif anomaly_type == 'bundling_violation':
            # Multiple related procedures that should be bundled
            claim['billed_amount'] *= 1.5
        
        claim['is_anomaly'] = 1
        claim['anomaly_type'] = anomaly_type
        
        return claim
    
    def _random_date(self):
        """Generate random date within last 2 years"""
        start_date = datetime.now() - timedelta(days=730)
        random_days = random.randint(0, 730)
        return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d') 