# Healthcare Denial Prediction & Automation System

A comprehensive machine learning system for predicting and automating healthcare claim denials using advanced ML techniques, real-time processing, and automated remediation workflows.

## 🏥 Overview

This system provides end-to-end solutions for healthcare claim denial management:

- **Pre-submission Prediction**: Predict denial probability before claim submission
- **Post-denial Automation**: Automatically classify and remediate denials
- **Continuous Learning**: Monitor model performance and auto-retrain
- **Real-time Analytics**: Dashboard for monitoring and insights
- **HIPAA Compliant**: Secure and compliant healthcare data processing

## 🏗️ Architecture

The system follows a modern MLOps architecture with the following components:

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

## 🚀 Features

### Phase 1: Foundation
- Data ingestion pipeline for 837/835 EDI files
- Feature engineering and ML model training
- FastAPI inference service with SHAP explanations
- Streamlit dashboard for real-time monitoring
- PostgreSQL database with comprehensive schema

### Phase 2: Post-Denial Automation
- NLP-based denial classification using transformers
- Automated remediation workflows
- Temporal workflow orchestration
- Multi-channel resolution strategies

### Phase 3: Advanced Features
- Continuous learning and drift detection
- Auto-retraining pipeline
- Feature evolution management
- Performance monitoring

### Phase 4-8: Production & Monitoring
- Comprehensive testing framework
- Prometheus metrics and alerting
- Canary deployment testing
- Production monitoring and observability

## 🛠️ Tech Stack

### Core Technologies
- **Python 3.9+**: Primary development language
- **FastAPI**: High-performance API framework
- **XGBoost**: Machine learning model
- **MLflow**: Model lifecycle management
- **PostgreSQL**: Primary database
- **Redis**: Caching and session management

### ML & Data
- **Transformers**: NLP for denial classification
- **SHAP**: Model explainability
- **Evidently AI**: Data drift detection
- **Pandas/NumPy**: Data processing
- **Scikit-learn**: ML utilities

### Infrastructure
- **Docker**: Containerization
- **Kubernetes**: Orchestration (production)
- **Apache Airflow**: Data pipeline orchestration
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards

### Frontend
- **Streamlit**: Interactive dashboards
- **Plotly**: Data visualization

## 📁 Project Structure

```
healthcare-denial-prediction/
├── api/                          # FastAPI application
│   ├── main.py                   # Main API server
│   ├── models.py                 # Pydantic models
│   └── dependencies.py           # API dependencies
├── models/                       # ML models and training
│   ├── denial_predictor.py       # Main prediction model
│   ├── denial_classifier.py      # NLP classification model
│   └── database.py               # Database models
├── data_pipeline/                # Data processing
│   ├── ingestion.py              # Data ingestion
│   ├── validation.py             # Data validation
│   └── transformation.py         # Data transformation
├── features/                     # Feature engineering
│   ├── feature_engineering.py    # Feature creation
│   ├── feature_store.py          # Feature store integration
│   └── feature_monitoring.py     # Feature drift detection
├── workflows/                    # Business workflows
│   ├── remediation_engine.py     # Auto-remediation
│   ├── temporal_workflows.py     # Workflow orchestration
│   └── notification_service.py   # Notifications
├── dashboard/                    # Streamlit dashboard
│   ├── app.py                    # Main dashboard
│   ├── components/               # Dashboard components
│   └── pages/                    # Dashboard pages
├── monitoring/                   # Monitoring and observability
│   ├── metrics.py                # Prometheus metrics
│   ├── alerts.py                 # Alert management
│   └── drift_detection.py        # Model drift monitoring
├── tests/                        # Test suites
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── e2e/                      # End-to-end tests
├── deployment/                   # Deployment configurations
│   ├── docker/                   # Docker configurations
│   ├── kubernetes/               # K8s manifests
│   └── terraform/                # Infrastructure as code
├── docs/                         # Documentation
├── scripts/                      # Utility scripts
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Local development
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- PostgreSQL 13+
- Redis 6+

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd healthcare-denial-prediction
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up -d postgres redis
   ```

4. **Initialize database**
   ```bash
   python scripts/init_db.py
   ```

5. **Start the API server**
   ```bash
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Start the dashboard**
   ```bash
   streamlit run dashboard/app.py
   ```

7. **Access the services**
   - API: http://localhost:8000
   - Dashboard: http://localhost:8501
   - API Docs: http://localhost:8000/docs

### Production Deployment

1. **Build Docker images**
   ```bash
   docker build -t healthcare-denial-api:latest .
   docker build -t healthcare-denial-dashboard:latest -f dashboard/Dockerfile .
   ```

2. **Deploy with Kubernetes**
   ```bash
   kubectl apply -f deployment/kubernetes/
   ```

## 📊 Usage Examples

### Making Predictions

```python
import requests

# Single claim prediction
claim_data = {
    "claim_id": "CLM_001",
    "provider_id": "PROV_123",
    "payer_id": "PAY_456",
    "patient_id": "PAT_789",
    "cpt_codes": ["99213", "90834"],
    "icd_codes": ["F32.9", "Z00.00"],
    "claim_amount": 1500.0,
    "service_date": "2024-01-15",
    "patient_age": 45,
    "patient_gender": "M",
    "place_of_service": "11"
}

response = requests.post(
    "http://localhost:8000/predict",
    json=claim_data,
    headers={"Authorization": "Bearer demo_token_123"}
)

print(f"Denial Probability: {response.json()['denial_probability']:.2%}")
```

### Processing Denials

```python
# Denial classification and remediation
denial_input = {
    "claim_id": "CLM_001",
    "denial_codes": ["CO_16", "CO_18"],
    "denial_reason_text": "Missing authorization for procedure",
    "claim_data": claim_data
}

response = requests.post(
    "http://localhost:8000/classify-denial",
    json=denial_input
)

print(f"Cause: {response.json()['cause_category']}")
print(f"Resolution: {response.json()['resolution_workflow']}")
```

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/healthcare_denials

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000

# API Security
API_SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
```

### Model Configuration

The system supports multiple model configurations:

- **XGBoost**: Primary prediction model
- **Transformer**: NLP classification model
- **Ensemble**: Combined model approach

## 📈 Monitoring & Observability

### Metrics
- Prediction latency and throughput
- Model accuracy and drift
- System resource utilization
- Business KPIs

### Alerts
- Model performance degradation
- Data drift detection
- System health issues
- Business rule violations

### Dashboards
- Real-time prediction monitoring
- Model performance trends
- Business analytics
- System health overview

## 🧪 Testing

### Running Tests

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# End-to-end tests
pytest tests/e2e/

# All tests with coverage
pytest --cov=. --cov-report=html
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **API Tests**: Endpoint functionality testing
- **Model Tests**: ML model validation
- **Performance Tests**: Load and stress testing

## 🔒 Security & Compliance

### HIPAA Compliance
- Data encryption at rest and in transit
- Access controls and audit logging
- PHI data handling procedures
- Secure API authentication

### Security Features
- JWT-based authentication
- Role-based access control
- Input validation and sanitization
- Rate limiting and DDoS protection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation in `/docs`

## 🔄 Version History

- **v1.0.0**: Initial release with core prediction functionality
- **v1.1.0**: Added post-denial automation
- **v1.2.0**: Continuous learning and drift detection
- **v1.3.0**: Production monitoring and testing framework

---

**Note**: This is a demonstration system. For production healthcare use, ensure proper compliance with HIPAA and other healthcare regulations. 