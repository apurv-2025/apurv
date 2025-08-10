# Health Insurance Claims Anomaly Detection System

A comprehensive machine learning system for detecting anomalous health insurance claims using ensemble methods (Isolation Forest + Random Forest).

## 🏗️ Project Structure

```
ClaimsAnamoly/
├── src/                          # Source code
│   ├── __init__.py
│   ├── data_generator.py         # Synthetic data generation
│   ├── models.py                 # ML models and training
│   ├── inference.py              # Production inference engine
│   └── main.py                   # Main execution module
├── api/                          # API server
│   ├── __init__.py
│   ├── app.py                    # Flask API (legacy)
│   └── fastapi_app.py            # FastAPI server
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── test_system.py           # Comprehensive test suite
├── models/                       # Saved trained models
│   └── __init__.py
├── data/                         # Data storage
│   └── __init__.py
├── requirements.txt              # Python dependencies
├── run_demo.py                   # Demo runner script
├── run_tests.py                  # Test runner script
├── run_fastapi.py                # FastAPI runner script
├── example_usage.py              # Usage examples
├── fastapi_client_example.py     # FastAPI client examples
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose setup
├── docker-run.sh                 # Docker management script
├── docker-test.sh                # Docker testing script
├── .dockerignore                 # Docker ignore rules
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
└── DOCKER_README.md              # Docker documentation
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Build the Docker image
./docker-run.sh build

# 2. Run the demo
./docker-run.sh demo

# 3. Start the API server
./docker-run.sh start

# 4. Test the API
./docker-run.sh test-api
```

**Access the API:**
- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Option 2: Local Installation

#### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv claims_env
source claims_env/bin/activate  # On Windows: claims_env\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

#### 2. Run the Complete Demo

```bash
# Run the full system demonstration
python run_demo.py
```

**Expected Output:**
- Generates 5,000 synthetic claims (400 anomalies)
- Trains ensemble model with performance metrics
- Demonstrates batch and single claim scoring
- Saves trained model to `models/claims_anomaly_model.pkl`

#### 3. Run Tests

```bash
# Run all unit tests
python run_tests.py
```

## 📊 System Components

### 1. Synthetic Data Generator (`src/data_generator.py`)
- Generates realistic health insurance claims data
- Supports controlled anomaly injection
- Includes various anomaly types: overbilling, code mismatches, excessive units, etc.

### 2. Anomaly Detection Model (`src/models.py`)
- **Isolation Forest**: Unsupervised anomaly detection
- **Random Forest**: Supervised classification with feature importance
- **Ensemble Approach**: Combines both models for robust predictions
- **Feature Engineering**: 20+ engineered features from raw claims data

### 3. Inference Engine (`src/inference.py`)
- Production-ready scoring engine
- Batch and single claim processing
- Model persistence (save/load)
- Real-time risk scoring (0-100 scale)

## 🔧 Usage Examples

### Basic Usage

```python
from src.data_generator import SyntheticClaimsDataGenerator
from src.models import ClaimsAnomalyDetector
from src.inference import ClaimsInferenceEngine

# Generate synthetic data
generator = SyntheticClaimsDataGenerator()
data = generator.generate_claims_data(n_claims=1000, anomaly_rate=0.08)

# Train model
model = ClaimsAnomalyDetector()
model.train(data)

# Set up inference engine
engine = ClaimsInferenceEngine()
engine.model = model

# Score claims
results = engine.score_claims_batch(data.head(10))
print(results)
```

### Single Claim Scoring

```python
# Score a single claim
claim = {
    'claim_id': 'CLM_001',
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

result = engine.score_single_claim(claim)
print(f"Risk Score: {result['risk_score']}/100")
print(f"Classification: {result['classification']}")
```

## 🧪 Testing

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test Categories
```bash
# Run only data generator tests
pytest tests/test_system.py::TestSyntheticClaimsDataGenerator -v

# Run only model tests
pytest tests/test_system.py::TestClaimsAnomalyDetector -v

# Run only inference tests
pytest tests/test_system.py::TestClaimsInferenceEngine -v
```

### Test Coverage
The test suite covers:
- ✅ Data generation quality and consistency
- ✅ Model training and prediction accuracy
- ✅ Feature engineering pipeline
- ✅ Inference engine functionality
- ✅ Model persistence (save/load)
- ✅ Performance requirements
- ✅ Integration workflows

## 📈 Performance Metrics

### Model Performance
- **Precision** (top 10% claims): ≥85%
- **Recall**: ≥70%
- **Processing Speed**: ≥10,000 claims/minute
- **Risk Score Range**: 0-100

### Feature Engineering
The system creates 20+ engineered features:
- **Temporal Features**: Day of week, month, weekend flags
- **Provider Features**: Historical averages, claim counts, anomaly rates
- **Amount Features**: Billing ratios, per-unit costs
- **Categorical Features**: Encoded specialties, codes, locations

## 🔍 Anomaly Types Detected

1. **Overbilling**: Excessive charges compared to usual amounts
2. **Code Mismatches**: Inappropriate CPT/ICD codes for provider specialty
3. **Excessive Units**: Unusually high units of service
4. **Geographic Anomalies**: Unusual place of service for procedures
5. **Bundling Violations**: Multiple procedures that should be bundled
6. **Unusual Frequency**: Abnormal claim submission patterns

## 🚀 Production Deployment

### Docker Deployment (Recommended)

```bash
# Build and deploy with Docker
./docker-run.sh build
./docker-run.sh start

# Scale the service
docker-compose up -d --scale claims-anomaly-api=3
```

### API Integration

The system provides a production-ready FastAPI with:
- **Interactive Documentation**: http://localhost:8000/docs
- **Single claim scoring**: POST `/api/v1/score`
- **Batch processing**: POST `/api/v1/score/batch`
- **Health monitoring**: GET `/health`
- **Model information**: GET `/api/v1/model/info`

### Model Persistence
```python
# Save trained model
engine.save_model("models/production_model.pkl")

# Load model in production
production_engine = ClaimsInferenceEngine("models/production_model.pkl")
```

### Scaling Considerations
- **Memory**: ~500MB for 10,000 claims
- **CPU**: Multi-threaded processing support
- **Storage**: Model files ~50MB each
- **Network**: Minimal bandwidth requirements

## 🔧 Configuration

### Model Parameters
```python
# Isolation Forest
isolation_forest = IsolationForest(
    contamination=0.05,  # Expected anomaly rate
    random_state=42,
    n_estimators=100
)

# Random Forest
random_forest = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    max_depth=10,
    class_weight='balanced'
)
```

### Feature Engineering
- **Provider History**: Uses historical data for provider statistics
- **Categorical Encoding**: Handles unseen categories gracefully
- **Missing Values**: Robust handling with appropriate defaults

## 📋 Requirements

### Python Dependencies
- pandas >= 1.5.0
- numpy >= 1.21.0
- scikit-learn >= 1.1.0
- joblib >= 1.2.0
- matplotlib >= 3.5.0 (for visualization)
- pytest >= 7.0.0 (for testing)

### System Requirements
- **Python**: 3.8+
- **Memory**: 4GB+ RAM recommended
- **Storage**: 1GB+ free space
- **CPU**: Multi-core recommended for large datasets

## 🛠️ Development

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html
```

### Adding New Features
1. Create feature in appropriate module
2. Add unit tests in `tests/test_system.py`
3. Update documentation
4. Run full test suite

## 📚 API Reference

### SyntheticClaimsDataGenerator
- `generate_claims_data(n_claims, anomaly_rate)`: Generate synthetic dataset

### ClaimsAnomalyDetector
- `train(df)`: Train the ensemble model
- `predict(df)`: Make predictions on new data
- `prepare_features(df)`: Feature engineering pipeline

### ClaimsInferenceEngine
- `score_claims_batch(df)`: Score multiple claims
- `score_single_claim(claim)`: Score single claim
- `save_model(path)`: Save trained model
- `load_model(path)`: Load trained model

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the test suite for usage examples
2. Review the API reference above
3. Run `python run_tests.py` to verify system health
4. Check logs for detailed error messages

---

**Note**: This system is designed for educational and development purposes. For production use in healthcare, ensure compliance with HIPAA and other relevant regulations.
