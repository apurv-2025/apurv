# PRD Review: Insurance Claims Processing Module (EDI)

## ✅ **Strengths**

### Well-Structured Foundation
- Clear separation of functional vs. non-functional requirements
- Good use of in-scope/out-of-scope boundaries
- Logical flow from high-level goals to technical details
- Appropriate focus on core EDI standards (X12 837/835)

### Technical Approach
- Correctly identifies key EDI transaction sets
- Includes essential validation layers (syntax, structural, business)
- Addresses security requirements (HIPAA compliance)
- Considers multiple transmission methods (FTP, AS2, API)

## 🚨 **Critical Gaps & Issues**

### 1. **837D Dental Claims Priority** ⚠️ **CRITICAL UPDATE**
**Issue:** PRD doesn't specify dental claims (837D) as Phase 1 priority
- **837D** = Dental claims - **PRIMARY FOCUS FOR PHASE 1**
- **837P** = Professional claims (physicians, labs)
- **837I** = Institutional claims (hospitals, facilities)  

**Dental-Specific Requirements Missing:**
- CDT (Current Dental Terminology) procedure code validation
- Dental-specific segments (DN1, DN2 for tooth information)
- Oral cavity area codes and tooth numbering systems
- Dental treatment plan sequences

### 2. **Incomplete Acknowledgment Handling**
**Current:** Mentions 277CA and 999 in passing
**Missing:**
- **999** - Functional Acknowledgment (syntax validation)
- **277CA** - Claim Acknowledgment (business validation)
- **TA1** - Interchange Acknowledgment
- Error handling for rejected acknowledgments

### 3. **Clearinghouse vs. Direct Payer Submission**
**Gap:** Document doesn't distinguish between:
- Clearinghouse routing (Availity, Change Healthcare)
- Direct payer submission
- Different validation rules for each path

### 4. **Payer-Specific Variations**
**Issue:** "Payer-specific rules (configurable)" is too vague
**Need to specify:**
- How companion guides will be implemented
- Override mechanisms for standard validation
- Payer enrollment/setup requirements

## 🦷 **DENTAL-SPECIFIC REQUIREMENTS (Phase 1 Priority)**

### Critical Dental Data Elements Missing from PRD

#### 1. **Dental Procedure Codes & Validation**
```
Required: CDT (Current Dental Terminology) code validation
- CDT codes (D0000-D9999) vs. medical CPT codes
- ADA (American Dental Association) code updates
- Procedure code to fee schedule mapping
- Multi-surface procedure validation (e.g., D2392 vs D2393)
```

#### 2. **Dental-Specific 837D Segments**
**Missing from current validation requirements:**
- **DN1** - Orthodontic Total Months of Treatment
- **DN2** - Tooth Status and Oral Cavity Information
- **PWK** - Additional Documentation (X-rays, perio charts)
- **CR1** - Ambulance Certification (for oral surgery transport)

#### 3. **Tooth Numbering & Oral Cavity Areas**
```
Required validation logic:
- Universal Numbering System (1-32 for adults)
- Primary tooth numbering (A-T)
- Quadrant and surface codes (M, O, D, L, B, I)
- Oral cavity area codes for non-tooth procedures
```

#### 4. **Dental Treatment Sequences**
**Business Logic Needed:**
- Multi-visit treatment plans (e.g., root canal series)
- Dependent procedure validation (crown after root canal)
- Frequency limitations (cleanings every 6 months)
- Prior procedure requirements

### Major Dental Payers & Their Quirks

#### 1. **Delta Dental (Multiple Entities)**
- Delta Dental of California, Michigan, etc. (different rules per state)
- Requires specific provider network validation
- Unique claim frequency rules
- PPO vs. Premier vs. Traditional plan handling

#### 2. **MetLife Dental**
- Strict documentation requirements for major procedures
- Specific formatting for predetermination requests
- Unique adjustment reason codes

#### 3. **Cigna Dental**
- Requires specific taxonomy codes for dental specialties
- Unique prior authorization workflows
- Different rules for in-network vs. out-of-network

### Dental-Specific Business Rules

#### 1. **Procedure Code Dependencies**
```
Examples that need validation:
- Crown (D2740) requires prior root canal or extensive restoration
- Scaling & Root Planing (D4341/D4342) per quadrant rules
- Full mouth debridement (D4355) before initial exam
- Fluoride treatment age restrictions
```

#### 2. **Frequency Limitations** 
```
Common dental frequencies to validate:
- Preventive cleanings: 2x per year
- Bitewing X-rays: 1x per year  
- Full mouth X-rays: 1x per 3-5 years
- Fluoride treatments: 2x per year (pediatric)
```

#### 3. **Age-Based Restrictions**
```
Validation rules needed:
- Sealants typically under age 16
- Fluoride treatments for children
- Orthodontic coverage age limits
- Denture vs. pediatric partial restrictions
```

## 🔧 **Technical Enhancements Needed**

### Data Model Specifications
```
Current: "Store raw and parsed claim data in a normalized schema"
Enhancement Needed:
- Define key entities (Claim, Patient, Provider, Service Line)
- Specify relationships and foreign keys
- Include audit fields (created_at, modified_by, etc.)
- Define data retention policies
```

### API Improvements
**Current APIs are basic. Consider adding:**
- `POST /claims/batch` - Bulk claim submission
- `GET /claims/validate` - Pre-submission validation
- `POST /claims/{id}/resubmit` - Claim correction workflow
- `GET /payers/{id}/rules` - Payer-specific validation rules
- `GET /reports/reconciliation` - Financial reconciliation endpoint

**Dental-Specific API Enhancements:**
- `GET /procedures/cdt/{code}` - CDT code validation and details
- `POST /claims/dental/validate` - Dental-specific validation (tooth numbers, frequencies)
- `GET /providers/{npi}/dental-networks` - Provider network validation
- `POST /predetermination` - Dental treatment plan pre-authorization

### Performance Specifications
**Current:** "Parse and validate one claim in <500ms"
**Issues:**
- No specification for batch processing performance
- Missing memory usage constraints
- No concurrent processing limits defined
- Missing file size limits (max claims per file)

## 📊 **Business Logic Gaps**

### 1. **Claim Correction Workflow**
**Missing:** Process for handling rejected claims
- Correction and resubmission workflow
- Claim frequency limitations (some payers limit resubmissions)
- Original vs. replacement claim handling

### 2. **Financial Reconciliation**
**Current 835 processing is basic. Need:**
- Payment posting workflow
- Adjustment reason code mapping
- Patient balance calculations
- Write-off and appeal processes

### 3. **Duplicate Detection**
**Missing:** Logic to prevent duplicate claim submissions
- Internal claim number generation
- Cross-reference with submitted claims
- Payer duplicate detection handling

## 🔒 **Security & Compliance Enhancements**

### HIPAA Specifics
**Current:** General mention of HIPAA compliance
**Need to specify:**
- BAA requirements with clearinghouses
- PHI handling procedures
- Audit log requirements (who, what, when, where)
- Data breach notification procedures

### Access Control
**Missing:**
- Role definitions (Claims Processor, Supervisor, Admin)
- Permission matrices
- Multi-factor authentication requirements
- Session timeout specifications

## 🎯 **Operational Requirements**

### Monitoring & Alerting
**Current monitoring is vague. Need:**
- Failed transmission alerts
- High rejection rate thresholds
- File processing delays
- System capacity warnings

### Error Handling Details
**Need to specify:**
- Retry logic (exponential backoff, max attempts)
- Dead letter queue handling
- Manual intervention workflows
- Error escalation procedures

## 📋 **Additional Recommendations**

### 1. **Testing Strategy**
Add section covering:
- Unit test requirements for validation engine
- Integration testing with sandbox payers
- End-to-end testing scenarios
- Performance testing criteria

**Dental-Specific Testing Scenarios:**
- Multi-surface fillings with proper tooth numbering
- Orthodontic treatment sequences over multiple visits
- Frequency limitation violations (multiple cleanings)
- Delta Dental network validation across different states
- CDT code validation for 2024 updates

### 2. **Configuration Management**
**Need to address:**
- Payer onboarding process
- Rule configuration UI
- Version control for business rules
- Environment-specific configurations

### 3. **Reporting Requirements**
**Expand beyond basic tracking:**
- Daily submission reports
- Rejection rate analytics
- Financial reconciliation reports
- SLA compliance metrics

### 4. **Migration Strategy**
**If replacing existing system:**
- Data migration approach
- Parallel processing period
- Rollback procedures
- User training requirements

## 🚦 **Risk Assessment Updates**

### Additional Risks to Consider:
| Risk | Impact | Mitigation |
|------|--------|------------|
| Payer certification delays | High | Start certification process early, maintain test credentials |
| EDI version updates (5010 to next version) | Medium | Design flexible parsing engine, monitor X12 updates |
| Clearinghouse API changes | Medium | Use multiple clearinghouses, maintain direct payer connections |
| PHI data breach | Critical | Implement encryption, access logging, penetration testing |

## 📅 **Recommended Next Steps (Dental Priority)**

1. **Define dental scope:** Focus on 837D with Delta Dental, MetLife, Cigna for Phase 1
2. **CDT code integration:** Acquire current CDT code database and validation rules
3. **Dental data model:** Design entities for tooth numbers, surfaces, treatment plans
4. **Delta Dental certification:** Begin certification with largest Delta entities first
5. **Create dental test scenarios:** Build comprehensive test suite with common dental procedures
6. **Security review:** Conduct HIPAA compliance assessment with dental PHI considerations

**Dental Industry Considerations:**
- ADA (American Dental Association) standards compliance
- State dental board reporting requirements may vary
- Dental practice management system integrations (Dentrix, Eaglesoft, Open Dental)
- Dental imaging integration for documentation requirements

## 💡 **Quick Wins for Phase 1 (Dental Focus)**

- **Start with 837D (dental claims) as primary focus**
- **Priority payers:** Delta Dental (largest market share), MetLife, Cigna
- Implement CDT code validation library first
- Focus on common procedures: cleanings, fillings, extractions, crowns
- Start with file-based processing before real-time APIs
- Use existing EDI parser library with dental-specific customizations
- Implement basic frequency validation (cleanings, X-rays)
- **Defer complex orthodontic sequences to Phase 2**

This PRD provides a solid foundation but needs these enhancements to guide successful engineering implementation.
