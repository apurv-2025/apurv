# ============================================================================
# PHASE 1: HEALTHCARE DENIAL PREDICTION SYSTEM - COMPLETE IMPLEMENTATION
# ============================================================================

# requirements.txt
"""
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pandas==2.1.4
numpy==1.24.3
scikit-learn==1.3.2
xgboost==2.0.2
mlflow==2.8.1
feast==0.35.0
apache-airflow==2.7.3
psycopg2-binary==2.9.9
redis==5.0.1
kafka-python==2.0.2
sqlalchemy==2.0.23
alembic==1.13.0
shap==0.43.0
evidently==0.4.11
prometheus-client==0.19.0
streamlit==1.28.2
plotly==5.17.0
boto3==1.34.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
"""

# ============================================================================
# 1. DATABASE MODELS AND SCHEMA
# ============================================================================

# models/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

DATABASE_URL = "postgresql://user:password@localhost/healthcare_denials"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"
    
    claim_id = Column(String, primary_key=True, index=True)
    provider_id = Column(String, index=True)
    payer_id = Column(String, index=True)
    patient_id = Column(String, index=True)
    cpt_codes = Column(JSON)
    icd_codes = Column(JSON)
    claim_amount = Column(Float)
    service_date = Column(DateTime)
    submission_date = Column(DateTime)
    patient_age = Column(Integer)
    patient_gender = Column(String)
    authorization_number = Column(String, nullable=True)
    modifiers = Column(JSON)
    place_of_service = Column(String)
    diagnosis_codes = Column(JSON)
    is_denied = Column(Boolean, nullable=True)
    denial_date = Column(DateTime, nullable=True)
    denial_codes = Column(JSON, nullable=True)
    denial_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Provider(Base):
    __tablename__ = "providers"
    
    provider_id = Column(String, primary_key=True)
    name = Column(String)
    specialty = Column(String)
    state = Column(String)
    zip_code = Column(String)
    historical_denial_rate = Column(Float)
    avg_claim_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Payer(Base):
    __tablename__ = "payers"
    
    payer_id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String)  # commercial, medicare, medicaid
    state = Column(String)
    avg_days_to_pay = Column(Integer)
    denial_rate = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id = Column(String, index=True)
    model_version = Column(String)
    denial_probability = Column(Float)
    predicted_causes = Column(JSON)
    shap_values = Column(JSON)
    prediction_timestamp = Column(DateTime, default=datetime.utcnow)
    actual_outcome = Column(Boolean, nullable=True)
    feedback_received = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)

# ============================================================================
# 2. DATA INGESTION PIPELINE
# ============================================================================

# data_pipeline/ingestion.py
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from models.database import SessionLocal, Claim, Provider, Payer
import logging

class DataIngestionPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def process_837_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Process 837 (claim submission) file"""
        claims = []
        
        # Simulated 837 processing - in reality, would use specialized EDI library
        # This is a simplified example
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('CLM'):  # Claim segment
                    claim_data = self._parse_claim_segment(line)
                    claims.append(claim_data)
        
        return claims
    
    def process_835_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Process 835 (remittance advice) file"""
        payments = []
        
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('CLP'):  # Claim payment segment
                    payment_data = self._parse_payment_segment(line)
                    payments.append(payment_data)
        
        return payments
    
    def _parse_claim_segment(self, segment: str) -> Dict[str, Any]:
        """Parse individual claim segment from 837"""
        # Simplified parsing - real implementation would be more complex
        parts = segment.split('*')
        return {
            'claim_id': parts[1] if len(parts) > 1 else '',
            'claim_amount': float(parts[2]) if len(parts) > 2 and parts[2] else 0.0,
            'provider_id': parts[3] if len(parts) > 3 else '',
            'service_date': datetime.now().strftime('%Y-%m-%d')
        }
    
    def _parse_payment_segment(self, segment: str) -> Dict[str, Any]:
        """Parse payment segment from 835"""
        parts = segment.split('*')
        return {
            'claim_id': parts[1] if len(parts) > 1 else '',
            'payment_amount': float(parts[2]) if len(parts) > 2 and parts[2] else 0.0,
            'status_code': parts[3] if len(parts) > 3 else ''
        }
    
    def ingest_claims_data(self, claims_data: List[Dict[str, Any]]):
        """Ingest claims data into database"""
        db = SessionLocal()
        try:
            for claim_data in claims_data:
                # Validate and clean data
                cleaned_claim = self._validate_claim_data(claim_data)
                if cleaned_claim:
                    claim = Claim(**cleaned_claim)
                    db.merge(claim)
            
            db.commit()
            self.logger.info(f"Ingested {len(claims_data)} claims")
            
        except Exception as e:
            db.rollback()
            self.logger.error(f"Error ingesting claims: {str(e)}")
            raise
        finally:
            db.close()
    
    def _validate_claim_data(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean claim data"""
        required_fields = ['claim_id', 'provider_id', 'payer_id', 'claim_amount']
        
        # Check required fields
        for field in required_fields:
            if field not in claim_data or not claim_data[field]:
                self.logger.warning(f"Missing required field {field} in claim")
                return None
        
        # Data type validation
        try:
            claim_data['claim_amount'] = float(claim_data['claim_amount'])
            claim_data['patient_age'] = int(claim_data.get('patient_age', 0))
        except (ValueError, TypeError):
            self.logger.warning("Invalid data types in claim")
            return None
        
        # Business rule validation
        if claim_data['claim_amount'] <= 0:
            self.logger.warning("Invalid claim amount")
            return None
        
        if claim_data['patient_age'] < 0 or claim_data['patient_age'] > 120:
            self.logger.warning("Invalid patient age")
            return None
        
        return claim_data

# ============================================================================
# 3. FEATURE ENGINEERING
# ============================================================================

# features/feature_engineering.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from models.database import SessionLocal

class FeatureEngineer:
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
        denial_rate_query = """
        SELECT 
            AVG(CASE WHEN is_denied THEN 1.0 ELSE 0.0 END) as denial_rate,
            AVG(claim_amount) as avg_amount,
            COUNT(*) as claim_count
        FROM claims 
        WHERE provider_id = :provider_id 
        AND submission_date >= :start_date
        """
        
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

# ============================================================================
# 4. ML MODEL TRAINING
# ============================================================================

# models/denial_predictor.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
import xgboost as xgb
import shap
import mlflow
import mlflow.xgboost
import joblib
from typing import Dict, Tuple, Any
import logging

class DenialPredictor:
    def __init__(self, model_name: str = "denial_predictor_v1"):
        self.model_name = model_name
        self.model = None
        self.scaler = StandardScaler()
        self.explainer = None
        self.feature_names = None
        self.logger = logging.getLogger(__name__)
        
        # Model hyperparameters
        self.params = {
            'objective': 'binary:logistic',
            'max_depth': 6,
            'learning_rate': 0.1,
            'n_estimators': 100,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'eval_metric': 'auc'
        }
    
    def prepare_training_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare training data from database"""
        db = SessionLocal()
        try:
            # Get claims with known outcomes
            query = """
            SELECT * FROM claims 
            WHERE is_denied IS NOT NULL 
            AND submission_date >= :start_date
            """
            start_date = datetime.now() - timedelta(days=365)
            
            claims_df = pd.read_sql(query, db.bind, params={'start_date': start_date})
            
            if claims_df.empty:
                raise ValueError("No training data available")
            
            # Create features for each claim
            feature_engineer = FeatureEngineer()
            features_list = []
            
            for _, claim in claims_df.iterrows():
                try:
                    features = feature_engineer.create_features(claim['claim_id'])
                    features['claim_id'] = claim['claim_id']
                    features['is_denied'] = claim['is_denied']
                    features_list.append(features)
                except Exception as e:
                    self.logger.warning(f"Error creating features for claim {claim['claim_id']}: {e}")
                    continue
            
            if not features_list:
                raise ValueError("No valid features created")
            
            # Convert to DataFrame
            features_df = pd.DataFrame(features_list)
            features_df = features_df.fillna(0)  # Handle missing values
            
            # Separate features and target
            X = features_df.drop(['claim_id', 'is_denied'], axis=1)
            y = features_df['is_denied'].astype(int)
            
            self.feature_names = X.columns.tolist()
            
            return X, y
            
        finally:
            db.close()
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Train the denial prediction model"""
        self.logger.info("Starting model training...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Start MLflow run
        with mlflow.start_run(run_name=f"{self.model_name}_training"):
            # Log parameters
            mlflow.log_params(self.params)
            
            # Train model
            self.model = xgb.XGBClassifier(**self.params)
            self.model.fit(
                X_train_scaled, y_train,
                eval_set=[(X_test_scaled, y_test)],
                early_stopping_rounds=10,
                verbose=False
            )
            
            # Make predictions
            y_train_pred = self.model.predict_proba(X_train_scaled)[:, 1]
            y_test_pred = self.model.predict_proba(X_test_scaled)[:, 1]
            y_test_pred_binary = self.model.predict(X_test_scaled)
            
            # Calculate metrics
            metrics = {
                'train_auc': roc_auc_score(y_train, y_train_pred),
                'test_auc': roc_auc_score(y_test, y_test_pred),
                'test_precision': precision_score(y_test, y_test_pred_binary),
                'test_recall': recall_score(y_test, y_test_pred_binary),
                'test_f1': f1_score(y_test, y_test_pred_binary)
            }
            
            # Log metrics
            for metric, value in metrics.items():
                mlflow.log_metric(metric, value)
            
            # Cross-validation
            cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
            mlflow.log_metric('cv_auc_mean', cv_scores.mean())
            mlflow.log_metric('cv_auc_std', cv_scores.std())
            
            # Setup SHAP explainer
            self.explainer = shap.Explainer(self.model, X_train_scaled[:100])  # Sample for efficiency
            
            # Log model
            mlflow.xgboost.log_model(
                self.model, 
                "model",
                registered_model_name=self.model_name
            )
            
            # Save scaler
            joblib.dump(self.scaler, f"{self.model_name}_scaler.joblib")
            mlflow.log_artifact(f"{self.model_name}_scaler.joblib")
            
            self.logger.info(f"Model training completed. Test AUC: {metrics['test_auc']:.4f}")
            
            return metrics
    
    def predict_with_explanation(self, X: pd.DataFrame) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Predict denial probability with SHAP explanations"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict
        probabilities = self.model.predict_proba(X_scaled)[:, 1]
        
        # Generate explanations
        if self.explainer is not None:
            shap_values = self.explainer(X_scaled)
            
            explanations = {
                'shap_values': shap_values.values.tolist(),
                'feature_names': self.feature_names,
                'base_value': shap_values.base_values.tolist() if hasattr(shap_values, 'base_values') else [0.0] * len(X)
            }
        else:
            explanations = {'error': 'SHAP explainer not available'}
        
        return probabilities, explanations
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from trained model"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        importance = self.model.feature_importances_
        feature_importance = dict(zip(self.feature_names, importance))
        
        # Sort by importance
        return dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))

# ============================================================================
# 5. INFERENCE API
# ============================================================================

# api/main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import redis
import json
import mlflow
import mlflow.xgboost
import joblib
from datetime import datetime
import logging
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Denial Prediction API",
    description="API for predicting healthcare claim denials",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Prometheus metrics
PREDICTION_COUNTER = Counter('denial_predictions_total', 'Total predictions made')
PREDICTION_LATENCY = Histogram('denial_prediction_duration_seconds', 'Prediction latency')
HIGH_RISK_COUNTER = Counter('high_risk_predictions_total', 'High risk predictions')

# Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Global model and scaler
model = None
scaler = None
feature_engineer = None

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ClaimData(BaseModel):
    claim_id: str = Field(..., description="Unique claim identifier")
    provider_id: str = Field(..., description="Provider identifier")
    payer_id: str = Field(..., description="Payer identifier")
    patient_id: str = Field(..., description="Patient identifier")
    cpt_codes: List[str] = Field(..., description="CPT procedure codes")
    icd_codes: List[str] = Field(..., description="ICD diagnosis codes")
    claim_amount: float = Field(..., gt=0, description="Claim amount in dollars")
    service_date: str = Field(..., description="Service date (YYYY-MM-DD)")
    patient_age: int = Field(..., ge=0, le=120, description="Patient age")
    patient_gender: str = Field(..., regex="^[MF]$", description="Patient gender (M/F)")
    authorization_number: Optional[str] = Field(None, description="Prior authorization number")
    modifiers: List[str] = Field(default=[], description="Procedure modifiers")
    place_of_service: str = Field(..., description="Place of service code")

class PredictionResponse(BaseModel):
    claim_id: str
    denial_probability: float = Field(..., ge=0, le=1)
    risk_level: str = Field(..., description="LOW, MEDIUM, HIGH")
    top_risk_factors: List[Dict[str, Any]]
    recommended_actions: List[str]
    model_version: str
    prediction_timestamp: str

class BatchPredictionRequest(BaseModel):
    claims: List[ClaimData]

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    summary: Dict[str, Any]

# ============================================================================
# STARTUP AND LIFECYCLE
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load model and initialize components on startup"""
    global model, scaler, feature_engineer
    
    try:
        # Load latest model from MLflow
        model_name = "denial_predictor_v1"
        model_version = "latest"
        
        model_uri = f"models:/{model_name}/{model_version}"
        model = mlflow.xgboost.load_model(model_uri)
        
        # Load scaler
        scaler = joblib.load(f"{model_name}_scaler.joblib")
        
        # Initialize feature engineer
        feature_engineer = FeatureEngineer()
        
        logging.info("Model loaded successfully")
        
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        raise

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API token - simplified for demo"""
    token = credentials.credentials
    if token != "demo_token_123":  # In production, use proper JWT validation
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "model_loaded": model is not None
    }

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict", response_model=PredictionResponse)
async def predict_single_claim(
    claim_data: ClaimData,
    token: str = Depends(verify_token)
):
    """Predict denial probability for a single claim"""
    start_time = time.time()
    
    try:
        # Check cache first
        cache_key = f"prediction:{claim_data.claim_id}"
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            result = json.loads(cached_result)
            PREDICTION_COUNTER.inc()
            return PredictionResponse(**result)
        
        # Create claim record for feature engineering
        claim_dict = claim_data.dict()
        claim_dict['submission_date'] = datetime.utcnow().isoformat()
        claim_dict['service_date'] = datetime.fromisoformat(claim_data.service_date)
        
        # Store temporarily in database for feature engineering
        db = SessionLocal()
        try:
            claim = Claim(**claim_dict)
            db.merge(claim)
            db.commit()
        finally:
            db.close()
        
        # Generate features
        features = feature_engineer.create_features(claim_data.claim_id)
        
        # Convert to DataFrame
        feature_df = pd.DataFrame([features])
        feature_df = feature_df.fillna(0)
        
        # Ensure all required features are present
        required_features = model.get_booster().feature_names
        for feature in required_features:
            if feature not in feature_df.columns:
                feature_df[feature] = 0.0
        
        feature_df = feature_df[required_features]
        
        # Scale features
        features_scaled = scaler.transform(feature_df)
        
        # Make prediction
        denial_probability = model.predict_proba(features_scaled)[0][1]
        
        # Generate explanations
        predictor = DenialPredictor()
        predictor.model = model
        predictor.scaler = scaler
        predictor.feature_names = required_features
        
        _, explanations = predictor.predict_with_explanation(feature_df)
        
        # Determine risk level
        if denial_probability >= 0.7:
            risk_level = "HIGH"
            HIGH_RISK_COUNTER.inc()
        elif denial_probability >= 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Generate risk factors and recommendations
        top_risk_factors = _generate_risk_factors(features, explanations, denial_probability)
        recommended_actions = _generate_recommendations(claim_data, denial_probability, top_risk_factors)
        
        # Create response
        response = PredictionResponse(
            claim_id=claim_data.claim_id,
            denial_probability=round(denial_probability, 4),
            risk_level=risk_level,
            top_risk_factors=top_risk_factors,
            recommended_actions=recommended_actions,
            model_version="v1.0",
            prediction_timestamp=datetime.utcnow().isoformat()
        )
        
        # Cache result for 1 hour
        redis_client.setex(cache_key, 3600, response.json())
        
        # Store prediction in database
        _store_prediction(claim_data.claim_id, response)
        
        # Update metrics
        PREDICTION_COUNTER.inc()
        PREDICTION_LATENCY.observe(time.time() - start_time)
        
        return response
        
    except Exception as e:
        logging.error(f"Error predicting claim {claim_data.claim_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch_claims(
    request: BatchPredictionRequest,
    token: str = Depends(verify_token)
):
    """Predict denial probability for multiple claims"""
    start_time = time.time()
    
    try:
        predictions = []
        high_risk_count = 0
        total_risk_score = 0.0
        
        for claim_data in request.claims:
            try:
                # Reuse single prediction logic
                prediction = await predict_single_claim(claim_data)
                predictions.append(prediction)
                
                if prediction.risk_level == "HIGH":
                    high_risk_count += 1
                
                total_risk_score += prediction.denial_probability
                
            except Exception as e:
                logging.warning(f"Failed to predict claim {claim_data.claim_id}: {e}")
                continue
        
        # Calculate summary statistics
        avg_risk_score = total_risk_score / len(predictions) if predictions else 0.0
        
        summary = {
            "total_claims": len(request.claims),
            "successful_predictions": len(predictions),
            "high_risk_claims": high_risk_count,
            "average_risk_score": round(avg_risk_score, 4),
            "processing_time_seconds": round(time.time() - start_time, 2)
        }
        
        return BatchPredictionResponse(
            predictions=predictions,
            summary=summary
        )
        
    except Exception as e:
        logging.error(f"Batch prediction failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )

@app.post("/feedback")
async def submit_feedback(
    claim_id: str,
    actual_outcome: bool,
    feedback_notes: Optional[str] = None,
    token: str = Depends(verify_token)
):
    """Submit feedback on prediction accuracy"""
    try:
        db = SessionLocal()
        try:
            # Update prediction record
            prediction = db.query(Prediction).filter(
                Prediction.claim_id == claim_id
            ).first()
            
            if prediction:
                prediction.actual_outcome = actual_outcome
                prediction.feedback_received = True
                db.commit()
                
                # Invalidate cache
                redis_client.delete(f"prediction:{claim_id}")
                
                return {
                    "status": "success",
                    "message": "Feedback recorded successfully"
                }
            else:
                raise HTTPException(status_code=404, detail="Prediction not found")
                
        finally:
            db.close()
            
    except Exception as e:
        logging.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

@app.get("/model/performance")
async def get_model_performance(token: str = Depends(verify_token)):
    """Get current model performance metrics"""
    try:
        db = SessionLocal()
        try:
            # Calculate metrics from recent predictions with feedback
            query = """
            SELECT 
                COUNT(*) as total_predictions,
                AVG(CASE WHEN actual_outcome = true THEN 1.0 ELSE 0.0 END) as actual_denial_rate,
                AVG(denial_probability) as avg_predicted_probability,
                COUNT(CASE WHEN feedback_received THEN 1 END) as feedback_count
            FROM predictions 
            WHERE prediction_timestamp >= NOW() - INTERVAL '30 days'
            """
            
            result = db.execute(query).fetchone()
            
            return {
                "period_days": 30,
                "total_predictions": result.total_predictions,
                "actual_denial_rate": result.actual_denial_rate,
                "avg_predicted_probability": result.avg_predicted_probability,
                "feedback_coverage": result.feedback_count / result.total_predictions if result.total_predictions > 0 else 0,
                "model_version": "v1.0",
                "last_updated": datetime.utcnow().isoformat()
            }
            
        finally:
            db.close()
            
    except Exception as e:
        logging.error(f"Error getting model performance: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get performance metrics")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _generate_risk_factors(features: Dict[str, Any], explanations: Dict[str, Any], probability: float) -> List[Dict[str, Any]]:
    """Generate top risk factors based on SHAP values"""
    risk_factors = []
    
    try:
        if 'shap_values' in explanations and explanations['shap_values']:
            shap_values = explanations['shap_values'][0]  # First prediction
            feature_names = explanations['feature_names']
            
            # Get top contributing features
            feature_contributions = list(zip(feature_names, shap_values))
            feature_contributions.sort(key=lambda x: abs(x[1]), reverse=True)
            
            for i, (feature, contribution) in enumerate(feature_contributions[:5]):
                risk_factors.append({
                    "factor": _humanize_feature_name(feature),
                    "impact": "increases" if contribution > 0 else "decreases",
                    "magnitude": abs(contribution),
                    "rank": i + 1
                })
    except Exception as e:
        logging.warning(f"Error generating risk factors: {e}")
        # Fallback to simple rule-based factors
        if probability > 0.5:
            risk_factors = [
                {"factor": "High claim amount", "impact": "increases", "magnitude": 0.1, "rank": 1},
                {"factor": "Provider history", "impact": "increases", "magnitude": 0.08, "rank": 2}
            ]
    
    return risk_factors

def _generate_recommendations(claim_data: ClaimData, probability: float, risk_factors: List[Dict[str, Any]]) -> List[str]:
    """Generate recommendations based on risk factors"""
    recommendations = []
    
    if probability >= 0.7:
        recommendations.append("HIGH RISK: Review claim carefully before submission")
        
        if not claim_data.authorization_number:
            recommendations.append("Verify prior authorization requirements")
        
        recommendations.append("Double-check CPT and ICD code accuracy")
        recommendations.append("Confirm patient eligibility and coverage")
        
        if claim_data.claim_amount > 10000:
            recommendations.append("Consider breaking down high-value claim into components")
            
    elif probability >= 0.4:
        recommendations.append("MEDIUM RISK: Standard review recommended")
        recommendations.append("Verify coding accuracy")
        
    else:
        recommendations.append("LOW RISK: Proceed with standard processing")
    
    # Add specific recommendations based on risk factors
    for factor in risk_factors:
        if "authorization" in factor["factor"].lower():
            recommendations.append("Request prior authorization if not obtained")
        elif "coding" in factor["factor"].lower():
            recommendations.append("Review CPT/ICD code selection with clinical team")
    
    return list(set(recommendations))  # Remove duplicates

def _humanize_feature_name(feature_name: str) -> str:
    """Convert technical feature names to human-readable descriptions"""
    name_mapping = {
        "provider_historical_denial_rate": "Provider denial history",
        "payer_denial_rate": "Payer denial rate",
        "claim_amount_log": "Claim amount",
        "patient_age": "Patient age",
        "has_authorization": "Prior authorization status",
        "number_of_cpt_codes": "Number of procedures",
        "high_dollar_claim": "High-value claim flag",
        "weekend_service": "Weekend service date",
        "payer_type_medicare": "Medicare payer",
        "provider_specialty_denial_rate": "Specialty-specific denial rate"
    }
    
    return name_mapping.get(feature_name, feature_name.replace("_", " ").title())

def _store_prediction(claim_id: str, response: PredictionResponse):
    """Store prediction in database"""
    try:
        db = SessionLocal()
        try:
            prediction = Prediction(
                claim_id=claim_id,
                model_version=response.model_version,
                denial_probability=response.denial_probability,
                predicted_causes=[factor["factor"] for factor in response.top_risk_factors],
                shap_values={}  # Would store actual SHAP values in production
            )
            db.add(prediction)
            db.commit()
        finally:
            db.close()
    except Exception as e:
        logging.warning(f"Failed to store prediction: {e}")

# ============================================================================
# 6. DASHBOARD APPLICATION
# ============================================================================

# dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json

# Configure Streamlit page
st.set_page_config(
    page_title="Healthcare Denial Prediction Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_TOKEN = "demo_token_123"

class DashboardAPI:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def predict_claim(self, claim_data: dict) -> dict:
        """Make prediction API call"""
        response = requests.post(
            f"{self.base_url}/predict",
            json=claim_data,
            headers=self.headers
        )
        return response.json()
    
    def get_model_performance(self) -> dict:
        """Get model performance metrics"""
        response = requests.get(
            f"{self.base_url}/model/performance",
            headers=self.headers
        )
        return response.json()

# Initialize API client
api = DashboardAPI(API_BASE_URL, API_TOKEN)

# ============================================================================
# DASHBOARD LAYOUT
# ============================================================================

def main():
    """Main dashboard application"""
    
    st.title("🏥 Healthcare Denial Prediction Dashboard")
    st.markdown("Real-time prediction and analysis of healthcare claim denials")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Single Claim Prediction", "Batch Analysis", "Model Performance", "Risk Analytics"]
    )
    
    if page == "Single Claim Prediction":
        single_claim_page()
    elif page == "Batch Analysis":
        batch_analysis_page()
    elif page == "Model Performance":
        model_performance_page()
    elif page == "Risk Analytics":
        risk_analytics_page()

def single_claim_page():
    """Single claim prediction page"""
    st.header("Single Claim Prediction")
    
    # Create input form
    with st.form("claim_prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            claim_id = st.text_input("Claim ID", value="CLM_001")
            provider_id = st.text_input("Provider ID", value="PROV_123")
            payer_id = st.text_input("Payer ID", value="PAY_456")
            patient_id = st.text_input("Patient ID", value="PAT_789")
            claim_amount = st.number_input("Claim Amount ($)", min_value=0.0, value=1500.0)
            
        with col2:
            patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=45)
            patient_gender = st.selectbox("Patient Gender", ["M", "F"])
            service_date = st.date_input("Service Date", datetime.now().date())
            place_of_service = st.text_input("Place of Service", value="11")
            authorization_number = st.text_input("Authorization Number (optional)", value="")
        
        # CPT and ICD codes
        cpt_codes = st.text_input("CPT Codes (comma-separated)", value="99213,90834").split(",")
        icd_codes = st.text_input("ICD Codes (comma-separated)", value="F32.9,Z00.00").split(",")
        modifiers = st.text_input("Modifiers (comma-separated)", value="").split(",") if st.text_input("Modifiers (comma-separated)", value="") else []
        
        submitted = st.form_submit_button("Predict Denial Risk")
        
        if submitted:
            # Prepare claim data
            claim_data = {
                "claim_id": claim_id,
                "provider_id": provider_id,
                "payer_id": payer_id,
                "patient_id": patient_id,
                "cpt_codes": [code.strip() for code in cpt_codes if code.strip()],
                "icd_codes": [code.strip() for code in icd_codes if code.strip()],
                "claim_amount": claim_amount,
                "service_date": service_date.isoformat(),
                "patient_age": patient_age,
                "patient_gender": patient_gender,
                "authorization_number": authorization_number if authorization_number else None,
                "modifiers": [mod.strip() for mod in modifiers if mod.strip()],
                "place_of_service": place_of_service
            }
            
            try:
                # Make prediction
                with st.spinner("Making prediction..."):
                    result = api.predict_claim(claim_data)
                
                # Display results
                display_prediction_results(result)
                
            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")

def display_prediction_results(result: dict):
    """Display prediction results"""
    
    # Main metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        denial_prob = result["denial_probability"]
        st.metric(
            "Denial Probability",
            f"{denial_prob:.1%}",
            delta=f"{denial_prob - 0.15:.1%}" if denial_prob > 0.15 else None
        )
    
    with col2:
        risk_level = result["risk_level"]
        risk_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
        st.metric("Risk Level", f"{risk_color.get(risk_level, '⚪')} {risk_level}")
    
    with col3:
        st.metric("Model Version", result["model_version"])
    
    # Risk gauge chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = denial_prob * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Denial Risk %"},
        delta = {'reference': 15},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Risk factors
    st.subheader("Top Risk Factors")
    if result["top_risk_factors"]:
        risk_df = pd.DataFrame(result["top_risk_factors"])
        
        fig_factors = px.bar(
            risk_df,
            x="magnitude",
            y="factor",
            color="impact",
            orientation="h",
            title="Risk Factor Contributions"
        )
        fig_factors.update_layout(height=300)
        st.plotly_chart(fig_factors, use_container_width=True)
    
    # Recommendations
    st.subheader("Recommended Actions")
    for i, action in enumerate(result["recommended_actions"], 1):
        st.write(f"{i}. {action}")

def batch_analysis_page():
    """Batch analysis page"""
    st.header("Batch Claim Analysis")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Claims CSV",
        type=["csv"],
        help="Upload a CSV file with claim data for batch analysis"
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            st.write(f"Loaded {len(df)} claims")
            st.dataframe(df.head())
            
            if st.button("Analyze Claims"):
                # Process batch prediction
                with st.spinner("Processing claims..."):
                    results = process_batch_claims(df)
                
                # Display batch results
                display_batch_results(results)
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def process_batch_claims(df: pd.DataFrame) -> pd.DataFrame:
    """Process batch claims (simulated)"""
    # In a real implementation, this would call the batch API
    # For now, simulate results
    results = []
    
    for _, row in df.iterrows():
        # Simulate prediction
        denial_prob = np.random.beta(2, 8)  # Skewed toward lower probabilities
        risk_level = "HIGH" if denial_prob > 0.7 else "MEDIUM" if denial_prob > 0.4 else "LOW"
        
        results.append({
            "claim_id": row.get("claim_id", f"CLM_{len(results)}"),
            "denial_probability": denial_prob,
            "risk_level": risk_level,
            "claim_amount": row.get("claim_amount", 1000),
            "provider_id": row.get("provider_id", "PROV_001")
        })
    
    return pd.DataFrame(results)

def display_batch_results(results_df: pd.DataFrame):
    """Display batch analysis results"""
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Claims", len(results_df))
    
    with col2:
        high_risk_count = len(results_df[results_df["risk_level"] == "HIGH"])
        st.metric("High Risk Claims", high_risk_count)
    
    with col3:
        avg_risk = results_df["denial_probability"].mean()
        st.metric("Average Risk", f"{avg_risk:.1%}")
    
    with col4:
        total_amount = results_df["claim_amount"].sum()
        st.metric("Total Amount at Risk", f"${total_amount:,.0f}")
    
    # Risk distribution
    fig_hist = px.histogram(
        results_df,
        x="denial_probability",
        nbins=20,
        title="Risk Distribution",
        labels={"denial_probability": "Denial Probability", "count": "Number of Claims"}
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Risk by provider
    provider_risk = results_df.groupby("provider_id")["denial_probability"].mean().reset_index()
    fig_provider = px.bar(
        provider_risk,
        x="provider_id",
        y="denial_probability",
        title="Average Risk by Provider"
    )
    st.plotly_chart(fig_provider, use_container_width=True)
    
    # Detailed results table
    st.subheader("Detailed Results")
    st.dataframe(results_df.sort_values("denial_probability", ascending=False))

def model_performance_page():
    """Model performance monitoring page"""
    st.header("Model Performance Dashboard")
    
    try:
        # Get performance metrics
        performance = api.get_model_performance()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Predictions", performance.get("total_predictions", 0))
        
        with col2:
            actual_rate = performance.get("actual_denial_rate", 0)
            st.metric("Actual Denial Rate", f"{actual_rate:.1%}")
        
        with col3:
            pred_rate = performance.get("avg_predicted_probability", 0)
            st.metric("Predicted Rate", f"{pred_rate:.1%}")
        
        with col4:
            feedback_coverage = performance.get("feedback_coverage", 0)
            st.metric("Feedback Coverage", f"{feedback_coverage:.1%}")
        
        # Generate sample performance charts
        generate_performance_charts()
        
    except Exception as e:
        st.error(f"Error loading performance data: {str(e)}")

def generate_performance_charts():
    """Generate sample performance monitoring charts"""
    
    # Sample data for demonstration
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    
    # Model accuracy over time
    accuracy_data = pd.DataFrame({
        "date": dates,
        "accuracy": np.random.normal(0.85, 0.03, 30),
        "auc": np.random.normal(0.88, 0.02, 30)
    })
    
    fig_performance = go.Figure()
    fig_performance.add_trace(go.Scatter(
        x=accuracy_data["date"],
        y=accuracy_data["accuracy"],
        mode="lines+markers",
        name="Accuracy",
        line=dict(color="blue")
    ))
    fig_performance.add_trace(go.Scatter(
        x=accuracy_data["date"],
        y=accuracy_data["auc"],
        mode="lines+markers",
        name="AUC",
        line=dict(color="red")
    ))
    
    fig_performance.update_layout(
        title="Model Performance Over Time",
        xaxis_title="Date",
        yaxis_title="Score",
        height=400
    )
    st.plotly_chart(fig_performance, use_container_width=True)
    
    # Prediction calibration
    prob_bins = np.arange(0, 1.1, 0.1)
    actual_rates = np.random.uniform(0.05, 0.95, len(prob_bins)-1)
    
    fig_calibration = go.Figure()
    fig_calibration.add_trace(go.Scatter(
        x=prob_bins[:-1] + 0.05,
        y=actual_rates,
        mode="markers+lines",
        name="Actual",
        line=dict(color="blue")
    ))
    fig_calibration.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode="lines",
        name="Perfect Calibration",
        line=dict(color="red", dash="dash")
    ))
    
    fig_calibration.update_layout(
        title="Model Calibration",
        xaxis_title="Predicted Probability",
        yaxis_title="Actual Rate",
        height=400
    )
    st.plotly_chart(fig_calibration, use_container_width=True)

def risk_analytics_page():
    """Risk analytics and insights page"""
    st.header("Risk Analytics & Insights")
    
    # Generate sample analytics data
    generate_risk_analytics()

def generate_risk_analytics():
    """Generate risk analytics dashboard"""
    
    # Sample data
    providers = [f"PROV_{i:03d}" for i in range(1, 21)]
    payers = ["Medicare", "Medicaid", "Aetna", "BCBS", "UnitedHealth"]
    
    # Provider risk analysis
    provider_data = pd.DataFrame({
        "provider_id": providers,
        "denial_rate": np.random.beta(2, 8, len(providers)),
        "claim_volume": np.random.poisson(100, len(providers)),
        "avg_amount": np.random.normal(2000, 500, len(providers))
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_provider_risk = px.scatter(
            provider_data,
            x="claim_volume",
            y="denial_rate",
            size="avg_amount",
            hover_data=["provider_id"],
            title="Provider Risk Analysis"
        )
        st.plotly_chart(fig_provider_risk, use_container_width=True)
    
    with col2:
        # Top risk providers
        top_risk = provider_data.nlargest(5, "denial_rate")
        fig_top_risk = px.bar(
            top_risk,
            x="denial_rate",
            y="provider_id",
            orientation="h",
            title="Highest Risk Providers"
        )
        st.plotly_chart(fig_top_risk, use_container_width=True)
    
    # Payer analysis
    payer_data = pd.DataFrame({
        "payer": payers,
        "denial_rate": np.random.beta(2, 6, len(payers)),
        "avg_days_to_pay": np.random.poisson(25, len(payers))
    })
    
    fig_payer = px.bar(
        payer_data,
        x="payer",
        y="denial_rate",
        title="Denial Rates by Payer"
    )
    st.plotly_chart(fig_payer, use_container_width=True)

# ============================================================================
# 7. AIRFLOW DATA PIPELINE
# ============================================================================

# airflow_dags/claims_pipeline.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import logging

# Default arguments
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

# Create DAG
dag = DAG(
    'healthcare_claims_pipeline',
    default_args=default_args,
    description='Healthcare claims data pipeline',
    schedule_interval='@hourly',
    catchup=False,
    max_active_runs=1
)

def ingest_claims_data(**context):
    """Ingest claims data from various sources"""
    from data_pipeline.ingestion import DataIngestionPipeline
    
    pipeline = DataIngestionPipeline()
    
    # Process 837 files
    claims_data = pipeline.process_837_file('/data/claims/latest_837.txt')
    pipeline.ingest_claims_data(claims_data)
    
    # Process 835 files
    payment_data = pipeline.process_835_file('/data/payments/latest_835.txt')
    # Update claims with payment information
    
    logging.info(f"Processed {len(claims_data)} claims")

def validate_data_quality(**context):
    """Validate data quality"""
    db = SessionLocal()
    try:
        # Check for duplicate claims
        duplicate_count = db.execute("""
            SELECT COUNT(*) as count FROM (
                SELECT claim_id, COUNT(*) 
                FROM claims 
                GROUP BY claim_id 
                HAVING COUNT(*) > 1
            ) duplicates
        """).fetchone().count
        
        if duplicate_count > 0:
            raise ValueError(f"Found {duplicate_count} duplicate claims")
        
        # Check for missing required fields
        missing_data = db.execute("""
            SELECT COUNT(*) as count 
            FROM claims 
            WHERE provider_id IS NULL 
            OR payer_id IS NULL 
            OR claim_amount IS NULL
        """).fetchone().count
        
        if missing_data > 0:
            logging.warning(f"Found {missing_data} claims with missing data")
        
        logging.info("Data quality validation passed")
        
    finally:
        db.close()

def update_features(**context):
    """Update feature store"""
    from features.feature_engineering import FeatureEngineer
    
    engineer = FeatureEngineer()
    
    # Update provider features
    db = SessionLocal()
    try:
        providers = db.query(Provider).all()
        for provider in providers:
            # Calculate updated features
            features = engineer._create_provider_features(db, provider.provider_id)
            provider.historical_denial_rate = features['provider_historical_denial_rate']
            provider.avg_claim_amount = features['provider_avg_claim_amount']
