# backend/seed_data.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import CPTCode, ICD10Code, HCPCSCode, ModifierCode
from app.database import Base
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://medicalcodes:secure_password_123@localhost:15432/medical_codes")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_database():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_cpt = db.query(CPTCode).first()
        if existing_cpt:
            print("Database already seeded. Skipping...")
            return
        
        print("Seeding database with sample data...")
        
        # Sample CPT Codes (including Category III codes from your reference)
        cpt_codes = [
            # Category I - Evaluation and Management
            CPTCode(code="99201", description="Office or other outpatient visit for the evaluation and management of a new patient", category="Category I", section="Evaluation and Management", subsection="Office or Other Outpatient Services"),
            CPTCode(code="99211", description="Office or other outpatient visit for the evaluation and management of an established patient", category="Category I", section="Evaluation and Management", subsection="Office or Other Outpatient Services"),
            CPTCode(code="99213", description="Office or other outpatient visit for the evaluation and management of an established patient, expanded problem focused", category="Category I", section="Evaluation and Management", subsection="Office or Other Outpatient Services"),
            CPTCode(code="99215", description="Office or other outpatient visit for the evaluation and management of an established patient, comprehensive", category="Category I", section="Evaluation and Management", subsection="Office or Other Outpatient Services"),
            
            # Category I - Psychiatry and Mental Health Services
            CPTCode(code="90791", description="Psychiatric diagnostic evaluation", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90792", description="Psychiatric diagnostic evaluation with medical services", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90832", description="Psychotherapy, 30 minutes with patient", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90834", description="Psychotherapy, 45 minutes with patient", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90837", description="Psychotherapy, 60 minutes with patient", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90853", description="Group psychotherapy (other than of a multiple-family group)", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90863", description="Pharmacologic management, including prescription and review of medication, when performed with psychotherapy services", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90875", description="Individual psychophysiological therapy incorporating biofeedback training by any modality (face-to-face with the patient), with psychotherapy", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90880", description="Hypnotherapy", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90882", description="Environmental intervention for medical management purposes on a psychiatric patient's behalf with agencies, employers, or institutions", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90885", description="Psychiatric evaluation of hospital records, other psychiatric reports, psychometric and/or projective tests, and other accumulated data for medical diagnostic purposes", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90887", description="Interpretation or explanation of results of psychiatric, other medical examinations and procedures, or other accumulated data to family or other responsible persons, or advising them how to assist patient", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90889", description="Preparation of report of patient's psychiatric status, history, treatment, or progress (other than for legal or consultative purposes) for other physicians, agencies, or insurance carriers", category="Category I", section="Medicine", subsection="Psychiatry"),
            CPTCode(code="90899", description="Unlisted psychiatric service or procedure", category="Category I", section="Medicine", subsection="Psychiatry"),
            
            # Category I - Surgery
            CPTCode(code="10021", description="Fine needle aspiration; without imaging guidance", category="Category I", section="Surgery", subsection="Integumentary System"),
            CPTCode(code="27447", description="Arthroplasty, knee, condyle and plateau; medial OR lateral compartment", category="Category I", section="Surgery", subsection="Musculoskeletal System"),
            CPTCode(code="36415", description="Collection of venous blood by venipuncture", category="Category I", section="Surgery", subsection="Cardiovascular System"),
            CPTCode(code="43239", description="Esophagogastroduodenoscopy, flexible, transoral; with biopsy, single or multiple", category="Category I", section="Surgery", subsection="Digestive System"),
            
            # Category I - Radiology
            CPTCode(code="70450", description="Computed tomography, head or brain; without contrast material", category="Category I", section="Radiology", subsection="Diagnostic Radiology"),
            CPTCode(code="71020", description="Radiologic examination, chest, 2 views, frontal and lateral", category="Category I", section="Radiology", subsection="Diagnostic Radiology"),
            CPTCode(code="73721", description="Magnetic resonance (eg, proton) imaging, any joint of lower extremity; without contrast material", category="Category I", section="Radiology", subsection="Diagnostic Radiology"),
            
            # Category I - Pathology and Laboratory
            CPTCode(code="80053", description="Comprehensive metabolic panel", category="Category I", section="Pathology and Laboratory", subsection="Chemistry"),
            CPTCode(code="85025", description="Blood count; complete (CBC), automated (Hgb, Hct, RBC, WBC and platelet count) and automated differential WBC count", category="Category I", section="Pathology and Laboratory", subsection="Hematology and Coagulation"),
            CPTCode(code="87804", description="Infectious agent antigen detection by immunoassay with direct optical observation; influenza", category="Category I", section="Pathology and Laboratory", subsection="Microbiology"),
            
            # Category I - Medicine
            CPTCode(code="90471", description="Immunization administration (includes percutaneous, intradermal, subcutaneous, or intramuscular injections); 1 vaccine (single or combination vaccine/toxoid)", category="Category I", section="Medicine", subsection="Immune Globulins, Serum or Recombinant Products"),
            CPTCode(code="93000", description="Electrocardiogram, routine ECG with at least 12 leads; with interpretation and report", category="Category I", section="Medicine", subsection="Cardiovascular"),
            CPTCode(code="94760", description="Noninvasive ear or pulse oximetry for oxygen saturation; single determination", category="Category I", section="Medicine", subsection="Pulmonary"),
            
            # Category III Codes (Emerging Technology)
            CPTCode(code="0001T", description="Extracorporeal shock wave involving musculoskeletal system, not otherwise specified, low energy", category="Category III", section="Medicine", subsection="Emerging Technology"),
            CPTCode(code="0042T", description="Cerebral perfusion analysis using computed tomography with contrast administration, including post-processing of parametric maps with quantification of cerebral blood flow, cerebral blood volume, and mean transit time", category="Category III", section="Radiology", subsection="Emerging Technology"),
            CPTCode(code="0075T", description="Transcatheter placement of extracranial vertebral or intrathoracic carotid artery stent(s), including radiologic supervision and interpretation, percutaneous; initial vessel", category="Category III", section="Surgery", subsection="Emerging Technology"),
            CPTCode(code="0095T", description="Removal of total disc arthroplasty (artificial disc), anterior approach, single interspace, cervical", category="Category III", section="Surgery", subsection="Emerging Technology"),
            CPTCode(code="0196T", description="Noninvasive testing of coronary endothelial function, using peripheral vascular function to predict coronary artery calcification", category="Category III", section="Medicine", subsection="Emerging Technology"),
            CPTCode(code="0329T", description="Monitoring of intraocular pressure for 24 hours or longer, unilateral or bilateral, with interpretation and report", category="Category III", section="Medicine", subsection="Emerging Technology"),
            CPTCode(code="0394T", description="High dose rate electronic brachytherapy, skin surface application, per fraction, includes basic dosimetry, when performed", category="Category III", section="Radiology", subsection="Emerging Technology"),
            CPTCode(code="0483T", description="Transcatheter mitral valve implantation/replacement (TMVI) with prosthetic valve; percutaneous approach, including transseptal puncture, when performed", category="Category III", section="Surgery", subsection="Emerging Technology"),
            CPTCode(code="0515T", description="Insertion or replacement of implantable cardioverter-defibrillator system with substernal electrode(s), including all imaging guidance and electrophysiological evaluation", category="Category III", section="Surgery", subsection="Emerging Technology"),
            CPTCode(code="0671T", description="Insertion of ocular telescope prosthesis including removal of crystalline lens or intraocular lens prosthesis", category="Category III", section="Surgery", subsection="Emerging Technology"),
        ]
        
        # Sample ICD-10 Codes
        icd10_codes = [
            # Mental Health Diagnosis codes
            ICD10Code(code="F32.0", description="Major depressive disorder, single episode, mild", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F32.1", description="Major depressive disorder, single episode, moderate", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F32.2", description="Major depressive disorder, single episode, severe without psychotic features", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F32.9", description="Major depressive disorder, single episode, unspecified", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F33.0", description="Major depressive disorder, recurrent, mild", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F33.1", description="Major depressive disorder, recurrent, moderate", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F33.2", description="Major depressive disorder, recurrent, severe without psychotic features", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F41.0", description="Panic disorder [episodic paroxysmal anxiety] without agoraphobia", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F41.1", description="Generalized anxiety disorder", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F41.9", description="Anxiety disorder, unspecified", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F43.10", description="Post-traumatic stress disorder, unspecified", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F43.11", description="Post-traumatic stress disorder, acute", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F43.12", description="Post-traumatic stress disorder, chronic", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F60.3", description="Emotionally unstable personality disorder", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F60.9", description="Personality disorder, unspecified", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F90.0", description="Attention-deficit hyperactivity disorder, predominantly inattentive type", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F90.1", description="Attention-deficit hyperactivity disorder, predominantly hyperactive type", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="F90.9", description="Attention-deficit hyperactivity disorder, unspecified type", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
            ICD10Code(code="Z63.0", description="Problems in relationship with spouse or partner", code_type="Diagnosis", chapter="Factors influencing health status and contact with health services", is_billable="Y"),
            ICD10Code(code="Z63.8", description="Other specified problems related to primary support group", code_type="Diagnosis", chapter="Factors influencing health status and contact with health services", is_billable="Y"),
            
            # Other Diagnosis codes
            ICD10Code(code="A09", description="Infectious gastroenteritis and colitis, unspecified", code_type="Diagnosis", chapter="Certain infectious and parasitic diseases", is_billable="Y"),
            ICD10Code(code="B99.9", description="Unspecified infectious disease", code_type="Diagnosis", chapter="Certain infectious and parasitic diseases", is_billable="Y"),
            ICD10Code(code="C78.1", description="Secondary malignant neoplasm of mediastinum", code_type="Diagnosis", chapter="Neoplasms", is_billable="Y"),
            ICD10Code(code="D50.9", description="Iron deficiency anemia, unspecified", code_type="Diagnosis", chapter="Diseases of the blood and blood-forming organs", is_billable="Y"),
            ICD10Code(code="E11.9", description="Type 2 diabetes mellitus without complications", code_type="Diagnosis", chapter="Endocrine, nutritional and metabolic diseases", is_billable="Y"),
            ICD10Code(code="G93.1", description="Anoxic brain damage, not elsewhere classified", code_type="Diagnosis", chapter="Diseases of the nervous system", is_billable="Y"),
            ICD10Code(code="H10.9", description="Unspecified conjunctivitis", code_type="Diagnosis", chapter="Diseases of the eye and adnexa", is_billable="Y"),
            ICD10Code(code="I10", description="Essential (primary) hypertension", code_type="Diagnosis", chapter="Diseases of the circulatory system", is_billable="Y"),
            ICD10Code(code="J44.1", description="Chronic obstructive pulmonary disease with acute exacerbation", code_type="Diagnosis", chapter="Diseases of the respiratory system", is_billable="Y"),
            ICD10Code(code="K59.00", description="Constipation, unspecified", code_type="Diagnosis", chapter="Diseases of the digestive system", is_billable="Y"),
            ICD10Code(code="L30.9", description="Dermatitis, unspecified", code_type="Diagnosis", chapter="Diseases of the skin and subcutaneous tissue", is_billable="Y"),
            ICD10Code(code="M79.3", description="Panniculitis, unspecified", code_type="Diagnosis", chapter="Diseases of the musculoskeletal system", is_billable="Y"),
            ICD10Code(code="N39.0", description="Urinary tract infection, site not specified", code_type="Diagnosis", chapter="Diseases of the genitourinary system", is_billable="Y"),
            ICD10Code(code="O80", description="Encounter for full-term uncomplicated delivery", code_type="Diagnosis", chapter="Pregnancy, childbirth and the puerperium", is_billable="Y"),
            ICD10Code(code="P07.37", description="Other preterm newborn, gestational age 36 completed weeks", code_type="Diagnosis", chapter="Certain conditions originating in the perinatal period", is_billable="Y"),
            ICD10Code(code="Q21.0", description="Ventricular septal defect", code_type="Diagnosis", chapter="Congenital malformations, deformations and chromosomal abnormalities", is_billable="Y"),
            ICD10Code(code="R06.02", description="Shortness of breath", code_type="Diagnosis", chapter="Symptoms, signs and abnormal clinical and laboratory findings", is_billable="Y"),
            ICD10Code(code="S72.001A", description="Fracture of unspecified part of neck of right femur, initial encounter for closed fracture", code_type="Diagnosis", chapter="Injury, poisoning and certain other consequences of external causes", is_billable="Y"),
            ICD10Code(code="Z51.11", description="Encounter for antineoplastic chemotherapy", code_type="Diagnosis", chapter="Factors influencing health status and contact with health services", is_billable="Y"),
        ]
        
        # Sample HCPCS Codes
        hcpcs_codes = [
            # Mental Health Services
            HCPCSCode(code="H0001", description="Behavioral health screening to determine eligibility for admission to treatment program", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0002", description="Behavioral health counseling and therapy, per 15 minutes", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0004", description="Behavioral health prevention program, non-physician provider, per 15 minutes", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0005", description="Behavioral health day treatment, partial hospitalization, per diem", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0006", description="Behavioral health short-term residential, non-hospital residential treatment program, per diem", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0007", description="Behavioral health long-term residential, non-hospital residential treatment program, per diem", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0008", description="Behavioral health clinic visit, per 15 minutes", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0009", description="Behavioral health case management, per 15 minutes", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0010", description="Behavioral health peer support services, per 15 minutes", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0011", description="Behavioral health crisis intervention, per 15 minutes", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0012", description="Behavioral health family psychoeducation, per 15 minutes", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0013", description="Behavioral health medication training and support, per 15 minutes", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0014", description="Behavioral health supported employment, per 15 minutes", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0015", description="Behavioral health supported housing, per 15 minutes", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0016", description="Behavioral health intensive outpatient treatment, per diem", level="Level II", category="Mental Health Services"),
            HCPCSCode(code="H0017", description="Behavioral health assertive community treatment, per diem", level="Level II", category="Mental Health Services"),
            
            # Durable Medical Equipment
            HCPCSCode(code="E0424", description="Stationary compressed gaseous oxygen system, rental; includes container, contents, regulator, flowmeter, humidifier, nebulizer, cannula or mask, and tubing", level="Level II", category="Durable Medical Equipment"),
            HCPCSCode(code="E0470", description="Respiratory assist device, bi-level pressure capability, without backup rate feature, used with noninvasive interface", level="Level II", category="Durable Medical Equipment"),
            HCPCSCode(code="E0601", description="Continuous positive airway pressure (CPAP) device", level="Level II", category="Durable Medical Equipment"),
            HCPCSCode(code="E1390", description="Oxygen concentrator, single delivery port, capable of delivering 85 percent or greater oxygen concentration at the prescribed flow rate", level="Level II", category="Durable Medical Equipment"),
            
            # Prosthetics and Orthotics
            HCPCSCode(code="L0112", description="Cranial cervical orthosis, congenital torticollis type, with or without soft interface material, adjustable range of motion joint, custom fabricated", level="Level II", category="Prosthetics and Orthotics"),
            HCPCSCode(code="L3806", description="Wrist hand finger orthosis, includes one or more nontorsion joints, turnbuckles, elastic bands/springs, may include soft interface material", level="Level II", category="Prosthetics and Orthotics"),
            HCPCSCode(code="L5856", description="Addition to lower extremity prosthesis, endoskeletal knee-shin system, microprocessor control feature, swing and stance phase", level="Level II", category="Prosthetics and Orthotics"),
            
            # Ambulance Services
            HCPCSCode(code="A0425", description="Ground mileage, per statute mile", level="Level II", category="Ambulance Services"),
            HCPCSCode(code="A0427", description="Ambulance service, advanced life support, emergency transport, level 1 (ALS 1)", level="Level II", category="Ambulance Services"),
            
            # Drugs
            HCPCSCode(code="J0135", description="Injection, adalimumab, 20 mg", level="Level II", category="Drugs Administered Other Than Oral Method"),
            HCPCSCode(code="J0171", description="Injection, adalimumab-atto, biosimilar product (Amjevita), 20 mg", level="Level II", category="Drugs Administered Other Than Oral Method"),
            HCPCSCode(code="J1745", description="Injection, infliximab, excludes biosimilar, 10 mg", level="Level II", category="Drugs Administered Other Than Oral Method"),
            HCPCSCode(code="J3357", description="Injection, ustekinumab, 1 mg", level="Level II", category="Drugs Administered Other Than Oral Method"),
        ]
        
        # Sample Modifier Codes
        modifier_codes = [
            ModifierCode(modifier="25", description="Separate E/M service on the same day as another procedure", category="Evaluation and Management", applies_to="E/M services"),
            ModifierCode(modifier="59", description="Distinct procedural service", category="Surgery", applies_to="All procedures"),
            ModifierCode(modifier="76", description="Repeat procedure by same physician", category="Surgery", applies_to="All procedures"),
            ModifierCode(modifier="77", description="Repeat procedure by another physician", category="Surgery", applies_to="All procedures"),
            ModifierCode(modifier="78", description="Unplanned return to operating room for related procedure", category="Surgery", applies_to="Surgical procedures"),
            ModifierCode(modifier="79", description="Unrelated procedure during postoperative period", category="Surgery", applies_to="Surgical procedures"),
            ModifierCode(modifier="80", description="Assistant surgeon", category="Surgery", applies_to="Surgical procedures"),
            ModifierCode(modifier="81", description="Minimum assistant surgeon", category="Surgery", applies_to="Surgical procedures"),
            ModifierCode(modifier="82", description="Assistant surgeon (when qualified resident surgeon not available)", category="Surgery", applies_to="Surgical procedures"),
            ModifierCode(modifier="95", description="Synchronous telemedicine service rendered via real-time interactive audio and video telecommunications system", category="Telemedicine", applies_to="E/M services"),
            ModifierCode(modifier="GT", description="Via interactive audio and video telecommunication systems", category="Telemedicine", applies_to="Mental health services"),
            ModifierCode(modifier="GQ", description="Via asynchronous telecommunications system", category="Telemedicine", applies_to="Mental health services"),
            ModifierCode(modifier="GZ", description="Item or service expected to be denied as not reasonable and necessary", category="Medical Necessity", applies_to="All services"),
            ModifierCode(modifier="GY", description="Item or service statutorily excluded or does not meet the definition of any Medicare benefit", category="Medical Necessity", applies_to="All services"),
            ModifierCode(modifier="GA", description="Waiver of liability statement issued as required by payer policy, individual case", category="Medical Necessity", applies_to="All services"),
            ModifierCode(modifier="GX", description="Notice of liability issued, voluntary under payer policy", category="Medical Necessity", applies_to="All services"),
            ModifierCode(modifier="GZ", description="Item or service expected to be denied as not reasonable and necessary", category="Medical Necessity", applies_to="All services"),
            ModifierCode(modifier="HA", description="Child/adolescent program", category="Mental Health", applies_to="Mental health services"),
            ModifierCode(modifier="HB", description="Adult program, non-geriatric", category="Mental Health", applies_to="Mental health services"),
            ModifierCode(modifier="HC", description="Adult program, geriatric", category="Mental Health", applies_to="Mental health services"),
        ]
        
        # Add all codes to database
        db.add_all(cpt_codes)
        db.add_all(icd10_codes)
        db.add_all(hcpcs_codes)
        db.add_all(modifier_codes)
        
        # Commit the transaction
        db.commit()
        
        print(f"✅ Seeded {len(cpt_codes)} CPT codes")
        print(f"✅ Seeded {len(icd10_codes)} ICD-10 codes")
        print(f"✅ Seeded {len(hcpcs_codes)} HCPCS codes")
        print(f"✅ Seeded {len(modifier_codes)} Modifier codes")
        print("✅ Database seeding completed successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
