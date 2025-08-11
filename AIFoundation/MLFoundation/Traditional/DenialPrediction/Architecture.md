# Healthcare Denial Prediction & Automation System
## Implementation Architecture & Tech Stack

## 1. Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│  Data Pipeline  │───▶│  Feature Store  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  ML Platform    │◀───│  Inference API  │◀───│  ML Models      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dashboards    │    │   Workflows     │    │   Monitoring    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 2. Proven Tech Stack

### **Data Infrastructure**
- **Message Streaming**: Apache Kafka + Confluent Platform
- **Data Lake**: AWS S3 / Azure Data Lake Gen2 / GCP Cloud Storage
- **Data Warehouse**: Snowflake / BigQuery / Azure Synapse
- **Workflow Orchestration**: Apache Airflow / Prefect 2.0
- **CDC**: Debezium for real-time data capture

### **ML Platform**
- **Feature Store**: Feast / Tecton / AWS SageMaker Feature Store
- **ML Framework**: 
  - Training: MLflow + XGBoost/LightGBM + Transformers (Hugging Face)
  - Serving: MLflow Model Registry + Seldon Core / KServe
- **Model Monitoring**: Evidently AI / Arize AI / Neptune
- **Experimentation**: Weights & Biases / MLflow

### **APIs & Services**
- **API Framework**: FastAPI (Python) with Pydantic validation
- **Container**: Docker + Kubernetes
- **Load Balancer**: NGINX / AWS ALB / GCP Load Balancer
- **Caching**: Redis for feature caching
- **Database**: PostgreSQL for metadata, TimescaleDB for metrics

### **Frontend & Workflows**
- **Dashboard**: Streamlit / Plotly Dash for internal tools
- **Workflow Engine**: Temporal.io / Camunda for complex business processes
- **Notifications**: Apache Kafka + Custom microservices

### **Observability & Security**
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Metrics**: Prometheus + Grafana
- **Tracing**: Jaeger / OpenTelemetry
- **Security**: HashiCorp Vault for secrets, OAuth 2.0/SAML
- **HIPAA Compliance**: AWS/Azure/GCP compliance frameworks

## 3. Implementation Phases

### **Phase 1: Foundation (Weeks 0-12)**

#### 3.1 Data Pipeline Implementation
```python
# Apache Airflow DAG example
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

def ingest_claims_data():
    """Ingest claims data from various sources"""
    # Implementation for 837/835/997 file processing
    pass

def validate_and_clean():
    """Data validation and cleaning"""
    # Implement validation rules from section 4.4
    pass

def update_feature_store():
    """Update Feast feature store"""
    # Push features to online/offline stores
    pass

dag = DAG(
    'claims_data_pipeline',
    schedule_interval='@hourly',
    catchup=False
)

ingest_task = PythonOperator(
    task_id='ingest_claims',
    python_callable=ingest_claims_data,
    dag=dag
)
```

#### 3.2 Feature Store Setup (Feast)
```python
# feature_definitions.py
from feast import Entity, Feature, FeatureView, ValueType
from feast.data_source import BigQuerySource

# Entities
provider = Entity(name="provider_id", value_type=ValueType.STRING)
payer = Entity(name="payer_id", value_type=ValueType.STRING)
claim = Entity(name="claim_id", value_type=ValueType.STRING)

# Feature Views
claims_features = FeatureView(
    name="claims_features",
    entities=["provider_id", "payer_id"],
    ttl=timedelta(days=30),
    features=[
        Feature(name="historical_denial_rate", dtype=ValueType.FLOAT),
        Feature(name="avg_days_to_pay", dtype=ValueType.INT64),
        Feature(name="authorization_required", dtype=ValueType.BOOL),
        Feature(name="prior_auth_status", dtype=ValueType.STRING),
    ],
    batch_source=BigQuerySource(
        table_ref="project.dataset.claims_features",
        event_timestamp_column="created_timestamp",
    )
)
```

#### 3.3 Pre-submission Prediction Model
```python
# model_training.py
import mlflow
import mlflow.sklearn
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import shap

class DenialPredictor:
    def __init__(self):
        self.model = XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        self.explainer = None
    
    def train(self, X, y):
        """Train the denial prediction model"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        with mlflow.start_run():
            # Train model
            self.model.fit(X_train, y_train)
            
            # Calculate metrics
            train_auc = roc_auc_score(y_train, self.model.predict_proba(X_train)[:, 1])
            test_auc = roc_auc_score(y_test, self.model.predict_proba(X_test)[:, 1])
            
            # Log metrics
            mlflow.log_metric("train_auc", train_auc)
            mlflow.log_metric("test_auc", test_auc)
            
            # Setup explainer
            self.explainer = shap.Explainer(self.model)
            
            # Log model
            mlflow.sklearn.log_model(self.model, "denial_predictor")
    
    def predict_with_explanation(self, X):
        """Predict with SHAP explanations"""
        predictions = self.model.predict_proba(X)
        explanations = self.explainer(X)
        return predictions, explanations
```

#### 3.4 FastAPI Inference Service
```python
# inference_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.sklearn
import pandas as pd
from feast import FeatureStore
import redis

app = FastAPI(title="Healthcare Denial Prediction API")

# Initialize components
fs = FeatureStore(repo_path=".")
model = mlflow.sklearn.load_model("models:/denial_predictor/production")
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class PreSubmissionRequest(BaseModel):
    claim_id: str
    provider_id: str
    payer_id: str
    cpt_codes: list
    claim_amount: float
    patient_age: int
    # ... other claim features

class PredictionResponse(BaseModel):
    claim_id: str
    denial_probability: float
    top_risk_factors: list
    recommended_actions: list

@app.post("/predict-pre", response_model=PredictionResponse)
async def predict_pre_submission(request: PreSubmissionRequest):
    try:
        # Get features from feature store
        entity_dict = {
            "provider_id": request.provider_id,
            "payer_id": request.payer_id
        }
        
        features = fs.get_online_features(
            features=["claims_features:historical_denial_rate",
                     "claims_features:avg_days_to_pay"],
            entity_rows=[entity_dict]
        ).to_dict()
        
        # Prepare input data
        input_data = pd.DataFrame([{
            **features,
            "claim_amount": request.claim_amount,
            "patient_age": request.patient_age,
            # ... other features
        }])
        
        # Predict
        prediction_prob = model.predict_proba(input_data)[0][1]
        
        # Generate explanation (simplified)
        risk_factors = ["High claim amount", "Provider history"] if prediction_prob > 0.7 else []
        actions = ["Review authorization", "Check coding"] if prediction_prob > 0.7 else []
        
        return PredictionResponse(
            claim_id=request.claim_id,
            denial_probability=prediction_prob,
            top_risk_factors=risk_factors,
            recommended_actions=actions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### **Phase 2: Post-Denial Automation (Weeks 12-20)**

#### 3.5 Denial Classification Service
```python
# denial_classifier.py
from transformers import pipeline
import pandas as pd

class DenialClassifier:
    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased",
            return_all_scores=True
        )
        self.cause_mapping = {
            "missing_auth": "Missing Authorization",
            "invalid_code": "Invalid CPT/ICD Code",
            "eligibility": "Patient Eligibility Issue",
            "duplicate": "Duplicate Claim",
            # ... more mappings
        }
    
    def classify_denial(self, denial_text, denial_codes):
        """Classify denial reason and recommend resolution"""
        # Combine text and codes for classification
        input_text = f"Denial codes: {denial_codes}. Reason: {denial_text}"
        
        # Get classification
        results = self.classifier(input_text)
        top_cause = max(results, key=lambda x: x['score'])
        
        # Map to resolution workflow
        resolution_workflow = self.get_resolution_workflow(top_cause['label'])
        
        return {
            "cause_category": self.cause_mapping.get(top_cause['label'], "Other"),
            "confidence": top_cause['score'],
            "resolution_workflow": resolution_workflow,
            "appeal_success_probability": self.estimate_appeal_success(top_cause['label'])
        }
    
    def get_resolution_workflow(self, cause):
        """Map cause to resolution workflow"""
        workflows = {
            "missing_auth": "resubmit_with_auth",
            "invalid_code": "code_review_and_correct",
            "eligibility": "verify_eligibility",
            "duplicate": "investigate_duplicate"
        }
        return workflows.get(cause, "manual_review")
```

#### 3.6 Auto-Remediation Engine
```python
# auto_remediation.py
from temporal import workflow, activity
import asyncio

@activity.defn
async def add_modifier_activity(claim_data: dict, modifier: str):
    """Add modifier to claim"""
    # Implementation to add modifier to claim
    modified_claim = claim_data.copy()
    modified_claim['modifiers'].append(modifier)
    return modified_claim

@activity.defn
async def verify_eligibility_activity(patient_id: str, service_date: str):
    """Verify patient eligibility"""
    # Call eligibility verification service
    return {"eligible": True, "coverage": "active"}

@workflow.defn
class DenialResolutionWorkflow:
    @workflow.run
    async def run(self, denial_data: dict) -> dict:
        """Execute denial resolution workflow"""
        
        # Classify the denial
        classification = await workflow.execute_activity(
            classify_denial_activity,
            denial_data,
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # Route to appropriate resolution
        if classification['cause_category'] == 'Missing Authorization':
            return await self.handle_missing_auth(denial_data)
        elif classification['cause_category'] == 'Invalid CPT/ICD Code':
            return await self.handle_invalid_code(denial_data)
        # ... other routes
        
        return {"status": "manual_review_required"}
    
    async def handle_missing_auth(self, denial_data: dict):
        """Handle missing authorization denials"""
        # Request authorization
        auth_result = await workflow.execute_activity(
            request_authorization_activity,
            denial_data,
            start_to_close_timeout=timedelta(minutes=30)
        )
        
        if auth_result['approved']:
            # Resubmit with auth number
            return await workflow.execute_activity(
                resubmit_claim_activity,
                {**denial_data, "auth_number": auth_result['auth_number']},
                start_to_close_timeout=timedelta(minutes=10)
            )
        
        return {"status": "auth_denied", "next_action": "appeal"}
```

### **Phase 3: Advanced Features (Post-20 weeks)**

#### 3.7 Continuous Learning Pipeline
```python
# continuous_learning.py
import mlflow
from evidently.report import Report
from evidently.metrics import DataDriftPreset, TargetDriftPreset

class ContinuousLearning:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = mlflow.tracking.MlflowClient()
    
    def monitor_drift(self, reference_data: pd.DataFrame, current_data: pd.DataFrame):
        """Monitor data and target drift"""
        report = Report(metrics=[
            DataDriftPreset(),
            TargetDriftPreset()
        ])
        
        report.run(reference_data=reference_data, current_data=current_data)
        drift_results = report.as_dict()
        
        return {
            "data_drift_detected": drift_results['metrics'][0]['result']['dataset_drift'],
            "target_drift_detected": drift_results['metrics'][1]['result']['target_drift'],
            "drift_score": drift_results['metrics'][0]['result']['drift_share']
        }
    
    def trigger_retraining(self, drift_results: dict, performance_metrics: dict):
        """Decide if retraining is needed"""
        retrain_needed = (
            drift_results['data_drift_detected'] or 
            drift_results['target_drift_detected'] or
            performance_metrics['auc'] < 0.8
        )
        
        if retrain_needed:
            # Trigger retraining pipeline
            return self.start_retraining_job()
        
        return {"status": "no_retraining_needed"}
    
    def start_retraining_job(self):
        """Start model retraining"""
        # Trigger Airflow DAG for retraining
        # Update feature definitions if needed
        # Test new model against validation set
        # Deploy if performance improves
        pass
```

## 4. Deployment Configuration

### 4.1 Kubernetes Deployment
```yaml
# k8s/inference-api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: denial-prediction-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: denial-prediction-api
  template:
    metadata:
      labels:
        app: denial-prediction-api
    spec:
      containers:
      - name: api
        image: your-registry/denial-prediction-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: MLFLOW_TRACKING_URI
          value: "http://mlflow-server:5000"
        - name: FEAST_REPO_PATH
          value: "/app/feast"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: denial-prediction-api-service
spec:
  selector:
    app: denial-prediction-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 4.2 Monitoring Setup
```yaml
# monitoring/prometheus-config.yaml
global:
  scrape_interval: 15s

scrape_configs:
- job_name: 'denial-prediction-api'
  static_configs:
  - targets: ['denial-prediction-api-service:80']
  metrics_path: '/metrics'

- job_name: 'mlflow'
  static_configs:
  - targets: ['mlflow-server:5000']

rule_files:
- "alert-rules.yml"

alerting:
  alertmanagers:
  - static_configs:
    - targets: ['alertmanager:9093']
```

## 5. Security & Compliance

### 5.1 HIPAA Compliance Checklist
- **Data Encryption**: At rest (AES-256) and in transit (TLS 1.3)
- **Access Controls**: Role-based access with OAuth 2.0/SAML
- **Audit Logging**: All data access and model predictions logged
- **Data Retention**: Automated purging of PHI per retention policies
- **Network Security**: VPC/VNet isolation, security groups/NSGs
- **Backup & Recovery**: Encrypted backups with tested recovery procedures

### 5.2 Data Privacy Implementation
```python
# privacy/data_anonymization.py
import hashlib
from typing import Dict, Any

class DataAnonymizer:
    def __init__(self, salt: str):
        self.salt = salt
    
    def anonymize_patient_data(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize patient identifiers while preserving ML utility"""
        anonymized = patient_data.copy()
        
        # Hash patient identifiers
        if 'patient_id' in anonymized:
            anonymized['patient_id_hash'] = self.hash_identifier(anonymized['patient_id'])
            del anonymized['patient_id']
        
        # Age binning instead of exact age
        if 'age' in anonymized:
            anonymized['age_group'] = self.bin_age(anonymized['age'])
        
        # Remove direct identifiers
        sensitive_fields = ['ssn', 'name', 'address', 'phone']
        for field in sensitive_fields:
            anonymized.pop(field, None)
        
        return anonymized
    
    def hash_identifier(self, identifier: str) -> str:
        """Create consistent hash of identifier"""
        return hashlib.sha256(f"{identifier}{self.salt}".encode()).hexdigest()
    
    def bin_age(self, age: int) -> str:
        """Bin age into groups"""
        if age < 18:
            return "0-17"
        elif age < 30:
            return "18-29"
        elif age < 50:
            return "30-49"
        elif age < 65:
            return "50-64"
        else:
            return "65+"
```

## 6. Performance Optimization

### 6.1 Caching Strategy
```python
# caching/feature_cache.py
import redis
import json
from typing import Dict, Any, Optional

class FeatureCache:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.ttl = 3600  # 1 hour TTL
    
    def get_cached_features(self, entity_key: str) -> Optional[Dict[str, Any]]:
        """Get cached features for entity"""
        cached_data = self.redis_client.get(f"features:{entity_key}")
        if cached_data:
            return json.loads(cached_data)
        return None
    
    def cache_features(self, entity_key: str, features: Dict[str, Any]):
        """Cache features with TTL"""
        self.redis_client.setex(
            f"features:{entity_key}",
            self.ttl,
            json.dumps(features, default=str)
        )
    
    def invalidate_cache(self, entity_key: str):
        """Invalidate cached features"""
        self.redis_client.delete(f"features:{entity_key}")
```

## 7. Testing Strategy

### 7.1 Model Testing Framework
```python
# tests/test_models.py
import pytest
import pandas as pd
from sklearn.metrics import roc_auc_score
from src.models.denial_predictor import DenialPredictor

class TestDenialPredictor:
    @pytest.fixture
    def sample_data(self):
        """Sample training data"""
        return pd.DataFrame({
            'claim_amount': [1000, 2000, 500],
            'provider_denial_rate': [0.1, 0.3, 0.05],
            'patient_age': [45, 65, 30],
            'is_denied': [0, 1, 0]
        })
    
    def test_model_training(self, sample_data):
        """Test model training process"""
        predictor = DenialPredictor()
        X = sample_data.drop('is_denied', axis=1)
        y = sample_data['is_denied']
        
        predictor.train(X, y)
        
        # Test predictions
        predictions = predictor.model.predict_proba(X)
        assert predictions.shape[1] == 2  # Binary classification
        assert all(0 <= p <= 1 for p in predictions[:, 1])  # Valid probabilities
    
    def test_prediction_latency(self, sample_data):
        """Test inference latency requirement (<300ms)"""
        import time
        
        predictor = DenialPredictor()
        X = sample_data.drop('is_denied', axis=1)
        
        start_time = time.time()
        predictions = predictor.model.predict_proba(X)
        end_time = time.time()
        
        latency_ms = (end_time - start_time) * 1000
        assert latency_ms < 300  # Meet latency requirement
```

## 8. Monitoring & Alerting

### 8.1 Key Metrics Dashboard
```python
# monitoring/metrics_collector.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
PREDICTION_COUNTER = Counter('denial_predictions_total', 'Total predictions made')
PREDICTION_LATENCY = Histogram('denial_prediction_duration_seconds', 'Prediction latency')
MODEL_ACCURACY = Gauge('denial_model_accuracy', 'Current model accuracy')
DENIAL_RATE = Gauge('claim_denial_rate', 'Current denial rate')

class MetricsCollector:
    def record_prediction(self, latency: float):
        """Record a prediction event"""
        PREDICTION_COUNTER.inc()
        PREDICTION_LATENCY.observe(latency)
    
    def update_model_performance(self, accuracy: float):
        """Update model accuracy metric"""
        MODEL_ACCURACY.set(accuracy)
    
    def update_denial_rate(self, rate: float):
        """Update current denial rate"""
        DENIAL_RATE.set(rate)
```

This implementation provides a robust, scalable, and compliant solution for healthcare denial prediction and automation. The tech stack is battle-tested in production environments and follows industry best practices for MLOps, security, and healthcare compliance.

