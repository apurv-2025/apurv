# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from typing import Generator

# Database URL - adjust for your PostgreSQL setup
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://username:password@localhost:5432/charge_capture_db"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Disable connection pooling for development
    echo=True  # Set to False in production
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database tables
def init_db():
    """Create all tables"""
    from app.models.models import Base  # Fixed import path
    Base.metadata.create_all(bind=engine)

# Sample data seeder
def seed_database():
    """Seed the database with sample data"""
    from app.models.models import Provider, Patient, Encounter, ChargeTemplate, ChargeValidationRule
    from datetime import datetime, timedelta
    import uuid
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Provider).first():
            print("Database already seeded")
            return
        
        # Create sample providers
        providers = [
            Provider(
                first_name="John",
                last_name="Smith",
                npi="1234567890",
                specialty="Internal Medicine"
            ),
            Provider(
                first_name="Sarah",
                last_name="Johnson",
                npi="0987654321",
                specialty="Cardiology"
            ),
            Provider(
                first_name="Michael",
                last_name="Davis",
                npi="1122334455",
                specialty="Dermatology"
            )
        ]
        
        for provider in providers:
            db.add(provider)
        db.flush()  # Get IDs
        
        # Create sample patients
        patients = [
            Patient(
                first_name="John",
                last_name="Doe",
                date_of_birth=datetime(1985, 3, 15),
                mrn="MRN-001",
                insurance_info={
                    "primary": "Blue Cross Blue Shield",
                    "member_id": "BC123456789",
                    "group_id": "GRP001"
                }
            ),
            Patient(
                first_name="Jane",
                last_name="Smith",
                date_of_birth=datetime(1990, 7, 22),
                mrn="MRN-002",
                insurance_info={
                    "primary": "Aetna",
                    "member_id": "AET987654321",
                    "group_id": "GRP002"
                }
            ),
            Patient(
                first_name="Robert",
                last_name="Wilson",
                date_of_birth=datetime(1978, 12, 3),
                mrn="MRN-003",
                insurance_info={
                    "primary": "UnitedHealthcare",
                    "member_id": "UHC456789123",
                    "group_id": "GRP003"
                }
            )
        ]
        
        for patient in patients:
            db.add(patient)
        db.flush()
        
        # Create sample encounters
        encounters = [
            Encounter(
                patient_id=patients[0].id,
                provider_id=providers[0].id,
                encounter_date=datetime.now() - timedelta(days=1),
                encounter_type="office_visit",
                status="completed",
                notes="Routine follow-up visit"
            ),
            Encounter(
                patient_id=patients[1].id,
                provider_id=providers[1].id,
                encounter_date=datetime.now() - timedelta(days=2),
                encounter_type="consultation",
                status="completed",
                notes="Cardiology consultation for chest pain"
            ),
            Encounter(
                patient_id=patients[2].id,
                provider_id=providers[2].id,
                encounter_date=datetime.now(),
                encounter_type="procedure",
                status="in_progress",
                notes="Skin lesion removal"
            )
        ]
        
        for encounter in encounters:
            db.add(encounter)
        db.flush()
        
        # Create sample charge templates
        templates = [
            ChargeTemplate(
                name="Common Office Visits",
                specialty="Internal Medicine",
                provider_id=providers[0].id,
                template_data={
                    "codes": [
                        {
                            "name": "Level 3 Established Visit",
                            "cpt": "99213",
                            "icd_options": ["Z00.00", "I10", "E11.9"],
                            "default_units": 1
                        },
                        {
                            "name": "Level 4 Established Visit",
                            "cpt": "99214",
                            "icd_options": ["I10", "E11.9", "J06.9"],
                            "default_units": 1
                        }
                    ]
                }
            ),
            ChargeTemplate(
                name="Cardiology Procedures",
                specialty="Cardiology",
                provider_id=providers[1].id,
                template_data={
                    "codes": [
                        {
                            "name": "Echocardiogram",
                            "cpt": "93306",
                            "icd_options": ["I25.9", "I50.9", "R06.02"],
                            "default_units": 1
                        },
                        {
                            "name": "Stress Test",
                            "cpt": "93015",
                            "icd_options": ["Z01.810", "I25.9"],
                            "default_units": 1
                        }
                    ]
                }
            ),
            ChargeTemplate(
                name="System Default - Preventive Care",
                specialty="All",
                is_system_template=True,
                template_data={
                    "codes": [
                        {
                            "name": "Annual Physical",
                            "cpt": "99395",
                            "icd_options": ["Z00.00"],
                            "default_units": 1
                        },
                        {
                            "name": "Preventive Medicine",
                            "cpt": "99396",
                            "icd_options": ["Z00.00", "Z00.01"],
                            "default_units": 1
                        }
                    ]
                }
            )
        ]
        
        for template in templates:
            db.add(template)
        
        # Create validation rules
        validation_rules = [
            ChargeValidationRule(
                rule_name="Prevent High Level Visits for Routine Exams",
                rule_type="code_combination",
                specialty="All",
                rule_config={
                    "cpt_codes": ["99215", "99205"],
                    "prohibited_icd_codes": ["Z00.00", "Z00.01"],
                    "severity": "warning"
                },
                error_message="High complexity visit codes may not be appropriate for routine examinations"
            ),
            ChargeValidationRule(
                rule_name="Diabetes Code Validation",
                rule_type="code_combination",
                specialty="Internal Medicine",
                rule_config={
                    "cpt_codes": ["99213", "99214", "99215"],
                    "required_when_icd": "E11.*",
                    "additional_codes": ["90791", "90792"]
                },
                error_message="Diabetes management may require additional documentation"
            ),
            ChargeValidationRule(
                rule_name="Modifier Required for Bilateral Procedures",
                rule_type="modifier_required",
                specialty="All",
                rule_config={
                    "cpt_codes": ["12001", "12002", "12004"],
                    "required_modifiers": ["50", "LT", "RT"],
                    "when": "bilateral"
                },
                error_message="Bilateral procedures require appropriate modifiers"
            )
        ]
        
        for rule in validation_rules:
            db.add(rule)
        
        # Commit all changes
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Initialize database and seed with sample data
    init_db()
    seed_database()
