# Health Insurance Verification System - Setup Instructions

## System Overview

This full-stack application provides comprehensive health insurance eligibility and benefits verification with EDI 270/271 support. The system includes:

- **Backend**: FastAPI with PostgreSQL database
- **Frontend**: React application with Tailwind CSS
- **OCR Processing**: Tesseract for insurance card text extraction
- **EDI Support**: Full EDI 270 (inquiry) and 271 (response) transaction handling
- **Database**: PostgreSQL with comprehensive schema
- **File Processing**: Support for images (JPG, PNG, TIFF) and PDF documents

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 15+**
- **Docker & Docker Compose** (recommended)
- **Tesseract OCR**

### Installing Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## Quick Start with Docker

1. **Clone the repository structure:**
```bash
mkdir health-insurance-verification
cd health-insurance-verification
mkdir backend frontend database
```

2. **Set up the backend:**
```bash
cd backend
# Copy the backend code from the artifact
# Copy requirements.txt content
# Create Dockerfile
```

3. **Set up the frontend:**
```bash
cd ../frontend
# Copy the React component code
# Create package.json
# Create Dockerfile
```

4. **Set up the database:**
```bash
cd ../database
# Copy the schema.sql file
```

5. **Create environment file:**
```bash
cp .env.example .env
# Edit .env with your actual values
```

6. **Start the application:**
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Database: localhost:5432

## Manual Installation

### Backend Setup

1. **Create Python virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL database:**
```bash
# Create database
createdb health_insurance_db

# Run schema
psql health_insurance_db < ../database/schema.sql
```

4. **Configure environment variables:**
```bash
export DATABASE_URL="postgresql://username:password@localhost/health_insurance_db"
export SECRET_KEY="your-secret-key-here"
```

5. **Start the backend:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Node.js dependencies:**
```bash
cd frontend
npm install
```

2. **Start the React development server:**
```bash
npm start
```

The frontend will be available at http://localhost:3000

## Key Features

### 1. Insurance Card Processing
- **Image Upload**: Drag-and-drop interface for insurance card images
- **PDF Support**: Extract text from insurance card PDFs
- **OCR Processing**: Automatic text extraction using Tesseract
- **Data Parsing**: Intelligent parsing of insurance information:
  - Member ID
  - Group Number
  - Patient Name
  - Insurance Company
  - Effective Date
  - Phone Number

### 2. EDI 270/271 Transactions
- **EDI 270 Generation**: Creates properly formatted eligibility inquiry transactions
- **EDI 271 Processing**: Handles eligibility response transactions
- **Standards Compliance**: Follows X12 EDI standards for healthcare transactions
- **Transaction Logging**: Complete audit trail of all EDI transactions

### 3. Eligibility Verification
- **Real-time Processing**: Submit eligibility inquiries and receive responses
- **Multiple Service Types**: Support for various healthcare service types
- **Benefits Information**: Detailed coverage and benefits display
- **Response Tracking**: Monitor request status and processing history

### 4. Database Schema
- **Comprehensive Tables**: Insurance cards, eligibility requests/responses, providers, payers
- **Audit Logging**: Complete transaction and change history
- **Performance Optimized**: Proper indexing for fast queries
- **Reporting Views**: Pre-built views for common reporting needs

## API Endpoints

### Insurance Card Processing
- `POST /api/upload-insurance-card` - Upload and process insurance card
- `GET /api/insurance-cards` - Retrieve processed cards

### Eligibility Verification
- `POST /api/eligibility-inquiry` - Submit EDI 270 eligibility inquiry
- `GET /api/eligibility-response/{request_id}` - Get EDI 271 response

### System Health
- `GET /` - API health check
- `GET /docs` - Interactive API documentation (Swagger UI)

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost/health_insurance_db

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256

# OCR Configuration
TESSERACT_CMD=/usr/bin/tesseract

# File Upload
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,pdf,tiff

# EDI Configuration
EDI_SUBMITTER_ID=YOUR_SUBMITTER_ID
EDI_RECEIVER_ID=YOUR_RECEIVER_ID
```

### Database Configuration

The PostgreSQL database includes:
- Insurance card storage
- EDI transaction logging
- Eligibility request/response tracking
- Provider and payer management
- Comprehensive audit trails

## Production Deployment

### Security Considerations

1. **Environment Variables**: Never commit sensitive data to version control
2. **HTTPS**: Always use HTTPS in production
3. **Database Security**: Use strong passwords and restrict access
4. **API Security**: Implement authentication and authorization
5. **File Upload Security**: Validate and sanitize uploaded files

### Performance Optimization

1. **Database Indexing**: Optimize queries with proper indexes
2. **Caching**: Implement Redis for frequently accessed data
3. **Connection Pooling**: Use connection pooling for database connections
4. **File Storage**: Consider cloud storage (AWS S3, Google Cloud) for uploaded files
5. **CDN**: Use CDN for static assets in production

### Monitoring and Logging

1. **Application Logging**: Comprehensive logging with different levels
2. **Performance Monitoring**: Track API response times and database queries
3. **Error Tracking**: Implement error tracking (Sentry, Rollbar)
4. **Health Checks**: Regular health checks for all services
5. **Metrics Collection**: Collect and analyze system metrics

## Testing

### Backend Testing

```bash
cd backend
pytest tests/
```

### Frontend Testing

```bash
cd frontend
npm test
```

### Integration Testing

```bash
# Test complete workflow
python tests/integration/test_complete_workflow.py
```

## EDI Standards Compliance

### EDI 270 (Eligibility Inquiry)
- **ISA Segment**: Interchange Control Header
- **GS Segment**: Functional Group Header
- **ST Segment**: Transaction Set Header
- **BHT Segment**: Beginning of Hierarchical Transaction
- **HL Segments**: Hierarchical Level (Information Source, Information Receiver, Subscriber, Dependent)
- **PRV Segment**: Provider Information
- **NM1 Segment**: Individual or Organizational Name
- **DMG Segment**: Demographic Information
- **EQ Segment**: Eligibility or Benefit Inquiry
- **SE Segment**: Transaction Set Trailer
- **GE Segment**: Functional Group Trailer
- **IEA Segment**: Interchange Control Trailer

### EDI 271 (Eligibility Response)
- **Same structure as 270 with response-specific segments**
- **EB Segment**: Eligibility or Benefit Information
- **MSG Segment**: Message Text
- **Additional benefit detail segments as needed**

## Real-World Integration

### Payer Integration
For production use, integrate with real payer systems:

1. **Change Healthcare**: Leading EDI clearinghouse
2. **Availity**: Healthcare information network
3. **Direct Payer APIs**: Some insurers provide direct API access
4. **Clearinghouse Services**: Use established clearinghouses for multiple payers

### HIPAA Compliance
Ensure HIPAA compliance for production deployment:

1. **Data Encryption**: Encrypt data at rest and in transit
2. **Access Controls**: Implement role-based access controls
3. **Audit Trails**: Maintain comprehensive audit logs
4. **Business Associate Agreements**: Execute BAAs with service providers
5. **Security Risk Assessments**: Regular security assessments

## Troubleshooting

### Common Issues

#### 1. OCR Not Working
```bash
# Check Tesseract installation
tesseract --version

# Install language packs if needed
sudo apt-get install tesseract-ocr-eng
```

#### 2. Database Connection Issues
```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Test connection
psql -h localhost -p 5432 -U username -d health_insurance_db
```

#### 3. File Upload Errors
- Check file size limits
- Verify file permissions
- Ensure upload directory exists

#### 4. CORS Issues
- Configure CORS settings in FastAPI
- Check frontend API URL configuration

### Performance Issues

#### 1. Slow OCR Processing
- Use image preprocessing to improve OCR accuracy
- Consider cloud OCR services for better performance
- Implement async processing for large files

#### 2. Database Performance
- Monitor slow queries
- Add database indexes where needed
- Consider database connection pooling

#### 3. Memory Usage
- Monitor memory usage during file processing
- Implement file streaming for large uploads
- Use background tasks for heavy processing

## Extensions and Enhancements

### Additional Features to Consider

1. **Real-time Eligibility**: WebSocket connections for real-time updates
2. **Batch Processing**: Process multiple eligibility requests in batches
3. **Provider Portal**: Web portal for healthcare providers
4. **Patient Portal**: Allow patients to check their own eligibility
5. **Analytics Dashboard**: Comprehensive reporting and analytics
6. **Mobile App**: React Native app for mobile access
7. **API Rate Limiting**: Implement rate limiting for API endpoints
8. **Multi-tenant Support**: Support multiple healthcare organizations

### Advanced OCR Features

1. **Machine Learning**: Train custom models for insurance card recognition
2. **Computer Vision**: Use advanced CV techniques for better extraction
3. **Document Classification**: Automatically classify different document types
4. **Quality Assessment**: Score extraction confidence and request manual review

### Advanced EDI Features

1. **EDI 999**: Implementation Acknowledgment
2. **EDI 277**: Claim Status Request/Response
3. **EDI 835**: Healthcare Claim Payment/Advice
4. **EDI 837**: Healthcare Claim Transaction

## Maintenance

### Regular Maintenance Tasks

1. **Database Maintenance**:
   ```sql
   -- Vacuum and analyze tables
   VACUUM ANALYZE;
   
   -- Check table sizes
   SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass)) 
   FROM pg_tables WHERE schemaname = 'public';
   ```

2. **Log Rotation**:
   ```bash
   # Configure logrotate for application logs
   sudo nano /etc/logrotate.d/health-insurance-app
   ```

3. **Backup Strategy**:
   ```bash
   # Database backup
   pg_dump health_insurance_db > backup_$(date +%Y%m%d).sql
   
   # Automated backups with cron
   0 2 * * * pg_dump health_insurance_db > /backups/backup_$(date +\%Y\%m\%d).sql
   ```

4. **Security Updates**:
   ```bash
   # Update Python packages
   pip list --outdated
   pip install --upgrade package_name
   
   # Update Node.js packages
   npm audit
   npm update
   ```

## Support and Documentation

### Getting Help

1. **Documentation**: Comprehensive API documentation at `/docs`
2. **Logging**: Check application logs for detailed error information
3. **Database Queries**: Use provided views for common reporting needs
4. **Community**: Join healthcare technology forums for additional support

### Additional Resources

- [X12 EDI Standards](https://x12.org/)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

This system provides a solid foundation for health insurance verification with room for expansion based on specific organizational needss
