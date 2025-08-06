# ClaimsProcessing3.0 - AI-Enhanced EDI Claims Processing System

## 🎯 **Overview**

ClaimsProcessing3.0 is a comprehensive healthcare claims processing system that combines advanced AI agent capabilities with specialized dental claims processing. This merged system provides intelligent automation, natural language interaction, and robust EDI transaction handling for healthcare providers.

## ✨ **Key Features**

### 🤖 **AI Agent System**
- **LangGraph Workflow** - Structured AI processing pipeline
- **Natural Language Interface** - Chat with your claims system
- **10+ Specialized Tools** - Claims validation, analysis, reporting
- **Multi-Model Support** - OpenAI, Anthropic, Custom models
- **Performance Monitoring** - Real-time metrics and health checks

### 🦷 **Dental Claims Specialization**
- **837D Transaction Support** - Complete dental claims processing
- **CDT Code Validation** - Current Dental Terminology validation
- **Dental-Specific Segments** - DN1, DN2, PWK, CR1 support
- **Tooth Numbering Systems** - Universal and primary tooth numbering
- **Treatment Plan Sequences** - Multi-visit treatment validation

### 📊 **Enhanced Claims Processing**
- **EDI X12 Support** - 837P, 837D, 837I transactions
- **Advanced Validation** - Multi-level validation with insights
- **835 Remittance Processing** - Payment and denial handling
- **Financial Reporting** - Automated KPI calculation
- **Claim Submission Workflow** - End-to-end processing

### 🏥 **Healthcare Standards**
- **HIPAA Compliance** - Secure PHI handling
- **Payer-Specific Rules** - Configurable validation rules
- **Clearinghouse Integration** - Multiple transmission methods
- **Audit Logging** - Complete transaction tracking

## 🏗️ **Architecture**

### **Backend Services**
```
backend/app/
├── agent/           # AI Agent System
│   ├── graph.py     # LangGraph workflow
│   ├── tools.py     # Agent tools
│   ├── manager.py   # Agent management
│   └── monitoring.py # Performance monitoring
├── services/        # Business Logic
│   ├── edi_parser.py      # EDI parsing
│   ├── claim_processor.py # Claim processing
│   └── validators.py      # Validation rules
├── api/routes/      # API Endpoints
│   ├── claims.py    # Claims endpoints
│   ├── payers.py    # Payers endpoints
│   ├── reports.py   # Reports endpoints
│   └── agent.py     # AI agent endpoints
└── database/        # Data Layer
    ├── models.py    # Database models
    └── connection.py # Database connection
```

### **Frontend Components**
```
frontend/src/
├── components/      # React components
├── pages/          # Page components
├── services/       # API services
├── utils/          # Utility functions
└── styles/         # Styling
```

## 🚀 **Quick Start**

### **Prerequisites**
- Docker and Docker Compose
- Node.js 16+ (for frontend development)
- Python 3.9+ (for backend development)

### **1. Clone and Setup**
```bash
git clone <repository-url>
cd ClaimsProcessing3.0
```

### **2. Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

**Required Environment Variables:**
```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/edi_claims

# Redis
REDIS_URL=redis://localhost:6379

# AI Agent (Optional - for AI features)
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4
OPENAI_API_KEY=your_openai_key_here

# Alternative AI providers
ANTHROPIC_API_KEY=your_anthropic_key_here
CUSTOM_MODEL_ENDPOINT=your_custom_endpoint
CUSTOM_MODEL_API_KEY=your_custom_key
```

### **3. Deploy with Docker**
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### **4. Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🤖 **AI Agent Usage**

### **Natural Language Interface**
```bash
# Chat with the agent
curl -X POST http://localhost:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What claims were rejected today?",
    "user_id": "user123"
  }'
```

### **Claim Analysis**
```bash
# Analyze a specific claim
curl -X POST http://localhost:8000/api/agent/tasks/analyze-claim/123 \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'
```

### **Report Generation**
```bash
# Generate financial report
curl -X POST http://localhost:8000/api/agent/tasks/generate-report \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "financial_summary",
    "user_id": "user123",
    "context": {"date_range": "this_month"}
  }'
```

## 📋 **API Endpoints**

### **Claims Processing**
- `POST /api/claims/upload` - Upload EDI file
- `GET /api/claims/{id}` - Get claim details
- `POST /api/claims/{id}/validate` - Validate claim
- `POST /api/claims/{id}/submit` - Submit claim to payer
- `POST /api/claims/835-remittance` - Process 835 remittance

### **AI Agent**
- `POST /api/agent/chat` - Natural language chat
- `POST /api/agent/tasks/analyze-claim/{id}` - Analyze claim
- `POST /api/agent/tasks/generate-report` - Generate reports
- `GET /api/agent/tools` - List available tools
- `GET /api/agent/metrics` - Performance metrics

### **Reports**
- `GET /api/reports/financial` - Financial summary
- `GET /api/reports/rejections` - Rejection analysis
- `GET /api/reports/performance` - Performance metrics

## 🦷 **Dental Claims Features**

### **CDT Code Validation**
The system includes comprehensive CDT (Current Dental Terminology) code validation:
- D0000-D9999 code range validation
- Multi-surface procedure validation
- Frequency limitation checks
- Age-based restrictions

### **Dental-Specific Data**
- **Tooth Numbers**: Universal (1-32) and Primary (A-T) numbering
- **Surfaces**: M, O, D, L, B, I surface codes
- **Treatment Plans**: Multi-visit sequence validation
- **Documentation**: X-ray and chart requirements

### **Payer-Specific Rules**
- **Delta Dental**: State-specific network validation
- **MetLife**: Documentation requirements
- **Cigna**: Taxonomy code validation

## 🔧 **Development**

### **Backend Development**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend Development**
```bash
cd frontend
npm install
npm start
```

### **Database Management**
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d edi_claims

# Run migrations
docker-compose exec backend python -m alembic upgrade head
```

## 🧪 **Testing**

### **Load Testing**
```bash
# Run load tests
python scripts/load_test.py

# Test specific endpoints
curl -X GET http://localhost:8000/health
```

### **AI Agent Testing**
```bash
# Test agent functionality
curl -X POST http://localhost:8000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "user_id": "test"}'
```

## 📊 **Monitoring**

### **Health Checks**
- **System Health**: `/health`
- **Agent Status**: `/api/agent/health`
- **Database**: Automatic health checks
- **Redis**: Connection monitoring

### **Metrics**
- **Performance**: `/api/agent/metrics/performance`
- **Real-time**: `/api/agent/metrics/realtime`
- **Tool Usage**: `/api/agent/metrics/tools`

## 🔒 **Security**

### **HIPAA Compliance**
- PHI encryption at rest and in transit
- Access logging and audit trails
- Role-based access control
- Secure API authentication

### **Data Protection**
- Database encryption
- Secure file uploads
- API rate limiting
- Input validation and sanitization

## 🚀 **Production Deployment**

### **Docker Production**
```bash
# Use production compose file
docker-compose -f production/docker-compose-prod.yml up -d
```

### **Kubernetes**
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

### **Environment Variables**
```env
# Production settings
DEBUG=false
SECRET_KEY=your-secure-secret-key
DATABASE_URL=postgresql://user:pass@prod-db:5432/edi_claims
REDIS_URL=redis://prod-redis:6379
```

## 📈 **Performance**

### **Benchmarks**
- **Claim Processing**: <500ms per claim
- **EDI Parsing**: <200ms per file
- **AI Agent Response**: <5 seconds
- **Database Queries**: <100ms average

### **Scalability**
- **Horizontal Scaling**: Multiple backend instances
- **Database**: Connection pooling and optimization
- **Redis**: Caching and session management
- **Load Balancing**: Nginx reverse proxy

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

- **Documentation**: Check the `/docs` endpoint
- **Issues**: Create GitHub issues
- **Email**: support@claimsprocessing.com

## 🔄 **Version History**

### **v3.0.0** (Current)
- Merged AI agent capabilities with dental claims processing
- Enhanced claim submission workflow
- 835 remittance processing
- Comprehensive dental validation
- Performance monitoring and metrics

### **v2.0.0** (AgenticClaimsProcessing)
- AI agent with LangGraph
- Natural language interface
- Advanced monitoring

### **v1.0.0** (NewClaimsProcessing)
- Basic EDI processing
- Dental claims specialization
- Enhanced frontend

---

**Built with ❤️ for the healthcare industry**
