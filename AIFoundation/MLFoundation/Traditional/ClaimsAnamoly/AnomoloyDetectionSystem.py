# Health Insurance Claims Anomaly Detection System
# Complete implementation with synthetic data generation, model training, and inference engine

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import logging
from typing import Dict, List, Tuple, Any
import json
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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

class ClaimsAnomalyDetector:
    """Machine Learning model for detecting anomalous claims"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.isolation_forest = IsolationForest(
            contamination=0.05, 
            random_state=42, 
            n_estimators=100
        )
        self.random_forest = RandomForestClassifier(
            n_estimators=200, 
            random_state=42, 
            max_depth=10,
            class_weight='balanced'
        )
        self.feature_columns = []
        self.is_trained = False
    
    def prepare_features(self, df):
        """Feature engineering for claims data"""
        
        features_df = df.copy()
        
        # Date features
        features_df['submission_date'] = pd.to_datetime(features_df['submission_date'])
        features_df['day_of_week'] = features_df['submission_date'].dt.dayofweek
        features_df['month'] = features_df['submission_date'].dt.month
        features_df['is_weekend'] = (features_df['day_of_week'] >= 5).astype(int)
        
        # Provider features
        provider_stats = features_df.groupby('provider_id').agg({
            'billed_amount': ['mean', 'std', 'count'],
            'units_of_service': 'mean',
            'is_anomaly': 'mean'  # Historical anomaly rate for provider
        }).round(2)
        
        provider_stats.columns = ['provider_avg_bill', 'provider_std_bill', 'provider_claim_count',
                                'provider_avg_units', 'provider_anomaly_rate']
        
        features_df = features_df.merge(
            provider_stats, 
            left_on='provider_id', 
            right_index=True, 
            how='left'
        )
        
        # Amount-based features
        features_df['bill_to_avg_ratio'] = (
            features_df['billed_amount'] / features_df['provider_avg_bill']
        ).fillna(1)
        
        features_df['amount_per_unit'] = (
            features_df['billed_amount'] / features_df['units_of_service']
        )
        
        # Categorical encoding
        categorical_features = ['provider_specialty', 'patient_gender', 'cpt_code', 
                              'icd_code', 'place_of_service', 'prior_authorization']
        
        for feature in categorical_features:
            if feature not in self.label_encoders:
                self.label_encoders[feature] = LabelEncoder()
                features_df[f'{feature}_encoded'] = self.label_encoders[feature].fit_transform(
                    features_df[feature].astype(str)
                )
            else:
                # Handle unseen categories in test data
                features_df[f'{feature}_encoded'] = features_df[feature].apply(
                    lambda x: self.label_encoders[feature].transform([str(x)])[0] 
                    if str(x) in self.label_encoders[feature].classes_ else -1
                )
        
        # Select final feature columns
        feature_columns = [
            'patient_age', 'units_of_service', 'billed_amount', 'paid_amount',
            'day_of_week', 'month', 'is_weekend', 'provider_avg_bill', 
            'provider_std_bill', 'provider_claim_count', 'provider_avg_units',
            'provider_anomaly_rate', 'bill_to_avg_ratio', 'amount_per_unit'
        ]
        
        # Add encoded categorical features
        feature_columns.extend([f'{cat}_encoded' for cat in categorical_features])
        
        self.feature_columns = feature_columns
        
        return features_df[feature_columns].fillna(0)
    
    def train(self, df):
        """Train the anomaly detection models"""
        
        logger.info("Preparing features for training...")
        X = self.prepare_features(df)
        y = df['is_anomaly']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Isolation Forest (unsupervised)
        logger.info("Training Isolation Forest...")
        self.isolation_forest.fit(X_train_scaled)
        
        # Train Random Forest (supervised)
        logger.info("Training Random Forest...")
        self.random_forest.fit(X_train_scaled, y_train)
        
        # Evaluate models
        self._evaluate_models(X_test_scaled, y_test)
        
        self.is_trained = True
        logger.info("Training completed successfully!")
        
        return {
            'X_test': X_test_scaled,
            'y_test': y_test,
            'feature_names': self.feature_columns
        }
    
    def _evaluate_models(self, X_test, y_test):
        """Evaluate model performance"""
        
        # Isolation Forest predictions
        iso_scores = self.isolation_forest.decision_function(X_test)
        iso_preds = self.isolation_forest.predict(X_test)
        iso_preds = np.where(iso_preds == -1, 1, 0)  # Convert to 0/1
        
        # Random Forest predictions
        rf_preds = self.random_forest.predict(X_test)
        rf_proba = self.random_forest.predict_proba(X_test)[:, 1]
        
        logger.info("=== Isolation Forest Results ===")
        logger.info(f"Classification Report:\n{classification_report(y_test, iso_preds)}")
        
        logger.info("=== Random Forest Results ===")
        logger.info(f"Classification Report:\n{classification_report(y_test, rf_preds)}")
        logger.info(f"AUC Score: {roc_auc_score(y_test, rf_proba):.3f}")
    
    def predict(self, df):
        """Make predictions on new claims"""
        
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.prepare_features(df)
        X_scaled = self.scaler.transform(X)
        
        # Get predictions from both models
        iso_scores = self.isolation_forest.decision_function(X_scaled)
        rf_proba = self.random_forest.predict_proba(X_scaled)[:, 1]
        
        # Combine scores (weighted average)
        combined_score = 0.3 * (iso_scores - iso_scores.min()) / (iso_scores.max() - iso_scores.min()) + \
                        0.7 * rf_proba
        
        # Convert to 0-100 scale
        risk_scores = (combined_score * 100).round(1)
        
        # Classification thresholds
        classifications = np.where(
            risk_scores >= 80, 'High Risk',
            np.where(risk_scores >= 50, 'Suspicious', 'Normal')
        )
        
        # Feature importance (top drivers)
        feature_importance = self.random_forest.feature_importances_
        top_features_idx = np.argsort(feature_importance)[::-1][:5]
        
        results = []
        for i, (score, classification) in enumerate(zip(risk_scores, classifications)):
            top_drivers = [self.feature_columns[idx] for idx in top_features_idx]
            
            results.append({
                'claim_id': df.iloc[i]['claim_id'] if 'claim_id' in df.columns else f"claim_{i}",
                'risk_score': score,
                'classification': classification,
                'top_drivers': top_drivers
            })
        
        return results

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

# Main execution and demonstration
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
    model_path = "claims_anomaly_model.pkl"
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
