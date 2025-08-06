# backend/seed_data.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import CPTCode, ICD10Code, HCPCSCode, ModifierCode, Base
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://medicalcodes:secure_password_123@localhost:15432/medical_codes")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_database():
    db = SessionLocal()
    
    # Sample CPT Codes (including Category III codes from your reference)
    cpt_codes = [
        # Category I - Evaluation and Management
        CPTCode(code="99201", description="Office or other outpatient visit for the evaluation and management of a new patient", category="Category I", section="Evaluation and Management", subsection="Office or Other Outpatient Services"),
        CPTCode(code="99211", description="Office or other outpatient visit for the evaluation and management of an established patient", category="Category I", section="Evaluation and Management", subsection="Office or Other Outpatient Services"),
        CPTCode(code="99213", description="Office or other outpatient visit for the evaluation and management of an established patient, expanded problem focused", category="Category I", section="Evaluation and Management", subsection="Office or Other Outpatient Services"),
        CPTCode(code="99215", description="Office or other outpatient visit for the evaluation and management of an established patient, comprehensive", category="Category I", section="Evaluation and Management", subsection="Office or Other Outpatient Services"),
        
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
        # Diagnosis codes
        ICD10Code(code="A09", description="Infectious gastroenteritis and colitis, unspecified", code_type="Diagnosis", chapter="Certain infectious and parasitic diseases", is_billable="Y"),
        ICD10Code(code="B99.9", description="Unspecified infectious disease", code_type="Diagnosis", chapter="Certain infectious and parasitic diseases", is_billable="Y"),
        ICD10Code(code="C78.1", description="Secondary malignant neoplasm of mediastinum", code_type="Diagnosis", chapter="Neoplasms", is_billable="Y"),
        ICD10Code(code="D50.9", description="Iron deficiency anemia, unspecified", code_type="Diagnosis", chapter="Diseases of the blood and blood-forming organs", is_billable="Y"),
        ICD10Code(code="E11.9", description="Type 2 diabetes mellitus without complications", code_type="Diagnosis", chapter="Endocrine, nutritional and metabolic diseases", is_billable="Y"),
        ICD10Code(code="F32.9", description="Major depressive disorder, single episode, unspecified", code_type="Diagnosis", chapter="Mental, Behavioral and Neurodevelopmental disorders", is_billable="Y"),
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
        HCPCSCode(code="J1100", description="Injection, dexamethasone sodium phosphate, 1 mg", level="Level II", category="Drugs Administered Other Than Oral Method"),
        HCPCSCode(code="J7030", description="Infusion, normal saline solution, 1000 cc", level="Level II", category="Drugs Administered Other Than Oral Method"),
        
        # Temporary Procedures
        HCPCSCode(code="G0121", description="Colorectal cancer screening; colonoscopy on individual not meeting criteria for high risk", level="Level II", category="Temporary Procedures"),
        HCPCSCode(code="G0463", description="Hospital outpatient clinic visit for assessment and management of a patient", level="Level II", category="Temporary Procedures"),
        
        # Supplies
        HCPCSCode(code="A4206", description="Syringe with needle, sterile, 1 cc or less, each", level="Level II", category="Medical and Surgical Supplies"),
        HCPCSCode(code="A4253", description="Blood glucose test or reagent strips for home blood glucose monitor, per 50 strips", level="Level II", category="Medical and Surgical Supplies"),
    ]
    
    # Sample Modifier Codes
    modifier_codes = [
        ModifierCode(modifier="22", description="Increased Procedural Services", category="Procedural", applies_to="Surgical and some medical procedures"),
        ModifierCode(modifier="25", description="Significant, Separately Identifiable Evaluation and Management Service by the Same Physician or Other Qualified Health Care Professional on the Same Day of the Procedure or Other Service", category="E&M", applies_to="Evaluation and Management codes"),
        ModifierCode(modifier="26", description="Professional Component", category="Radiology", applies_to="Radiology and pathology procedures"),
        ModifierCode(modifier="50", description="Bilateral Procedure", category="Procedural", applies_to="Surgical procedures performed bilaterally"),
        ModifierCode(modifier="51", description="Multiple Procedures", category="Procedural", applies_to="Multiple procedures performed during same session"),
        ModifierCode(modifier="52", description="Reduced Services", category="Procedural", applies_to="Services that are reduced or eliminated at physician discretion"),
        ModifierCode(modifier="53", description="Discontinued Procedure", category="Procedural", applies_to="Procedures discontinued due to extenuating circumstances"),
        ModifierCode(modifier="59", description="Distinct Procedural Service", category="Procedural", applies_to="Procedures not normally reported together"),
        ModifierCode(modifier="62", description="Two Surgeons", category="Surgical", applies_to="Surgical procedures requiring two surgeons"),
        ModifierCode(modifier="76", description="Repeat Procedure or Service by Same Physician or Other Qualified Health Care Professional", category="Procedural", applies_to="Repeated procedures"),
        ModifierCode(modifier="77", description="Repeat Procedure by Another Physician or Other Qualified Health Care Professional", category="Procedural", applies_to="Repeated procedures by different provider"),
        ModifierCode(modifier="78", description="Unplanned Return to the Operating/Procedure Room by the Same Physician or Other Qualified Health Care Professional Following Initial Procedure for a Related Procedure During the Postoperative Period", category="Surgical", applies_to="Return to OR procedures"),
        ModifierCode(modifier="79", description="Unrelated Procedure or Service by the Same Physician or Other Qualified Health Care Professional During the Postoperative Period", category="Surgical", applies_to="Unrelated procedures during postoperative period"),
        ModifierCode(modifier="80", description="Assistant Surgeon", category="Surgical", applies_to="Assistant surgeon services"),
        ModifierCode(modifier="81", description="Minimum Assistant Surgeon", category="Surgical", applies_to="Minimum assistant surgeon services"),
        ModifierCode(modifier="82", description="Assistant Surgeon (when qualified resident surgeon not available)", category="Surgical", applies_to="Assistant surgeon when resident not available"),
        ModifierCode(modifier="90", description="Reference (Outside) Laboratory", category="Laboratory", applies_to="Laboratory procedures performed by outside lab"),
        ModifierCode(modifier="91", description="Repeat Clinical Diagnostic Laboratory Test", category="Laboratory", applies_to="Repeated lab tests"),
        ModifierCode(modifier="95", description="Synchronous Telemedicine Service", category="Telemedicine", applies_to="Real-time telemedicine services"),
        ModifierCode(modifier="TC", description="Technical Component", category="Radiology", applies_to="Technical component of radiology procedures"),
    ]
    
    try:
        # Add all sample data
        for cpt in cpt_codes:
            db.merge(cpt)
        
        for icd10 in icd10_codes:
            db.merge(icd10)
        
        for hcpcs in hcpcs_codes:
            db.merge(hcpcs)
        
        for modifier in modifier_codes:
            db.merge(modifier)
        
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
