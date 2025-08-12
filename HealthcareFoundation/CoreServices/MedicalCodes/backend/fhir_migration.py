#!/usr/bin/env python3
"""
FHIR Schema Migration
Converts custom medical codes schema to FHIR-compliant schema
"""

import sys
import os
import json
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from app.database import engine, SessionLocal
from app.models import CPTCode, ICD10Code, HCPCSCode, ModifierCode
from app.fhir_models import (
    FHIRCodeSystem, FHIRConcept, FHIRValueSet, FHIRConceptMap,
    LegacyCPTCode, LegacyICD10Code, LegacyHCPCSCode, LegacyModifierCode
)
from sqlalchemy import text

def create_fhir_schema():
    """Create FHIR-compliant schema"""
    print("Creating FHIR-compliant schema...")
    
    # Import FHIR models to create tables
    from app.fhir_models import Base
    Base.metadata.create_all(bind=engine)
    
    print("✅ FHIR schema tables created successfully!")

def migrate_existing_data():
    """Migrate existing data to FHIR-compliant format"""
    print("Migrating existing data to FHIR format...")
    
    db = SessionLocal()
    try:
        # Create FHIR CodeSystems for each coding system
        code_systems = {
            'cpt': {
                'url': 'http://www.ama-assn.org/go/cpt',
                'name': 'CPT',
                'title': 'Current Procedural Terminology',
                'description': 'CPT codes are used to report medical, surgical, and diagnostic procedures and services.',
                'publisher': 'American Medical Association',
                'content': 'complete'
            },
            'icd10': {
                'url': 'http://hl7.org/fhir/sid/icd-10',
                'name': 'ICD-10',
                'title': 'International Classification of Diseases, 10th Revision',
                'description': 'ICD-10 codes are used to classify diseases and health problems.',
                'publisher': 'World Health Organization',
                'content': 'complete'
            },
            'hcpcs': {
                'url': 'http://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets',
                'name': 'HCPCS',
                'title': 'Healthcare Common Procedure Coding System',
                'description': 'HCPCS codes are used to report medical procedures and services.',
                'publisher': 'Centers for Medicare & Medicaid Services',
                'content': 'complete'
            },
            'modifiers': {
                'url': 'http://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets/Modifiers',
                'name': 'HCPCS_Modifiers',
                'title': 'HCPCS Modifiers',
                'description': 'HCPCS modifiers are used to provide additional information about procedures.',
                'publisher': 'Centers for Medicare & Medicaid Services',
                'content': 'complete'
            }
        }
        
        fhir_code_systems = {}
        
        # Create CodeSystems
        for system_key, system_data in code_systems.items():
            existing = db.query(FHIRCodeSystem).filter(FHIRCodeSystem.url == system_data['url']).first()
            if not existing:
                code_system = FHIRCodeSystem(
                    url=system_data['url'],
                    name=system_data['name'],
                    title=system_data['title'],
                    description=system_data['description'],
                    publisher=system_data['publisher'],
                    content=system_data['content'],
                    status='active',
                    date=datetime.utcnow()
                )
                db.add(code_system)
                db.commit()
                db.refresh(code_system)
                fhir_code_systems[system_key] = code_system
                print(f"✅ Created CodeSystem: {system_data['name']}")
            else:
                fhir_code_systems[system_key] = existing
                print(f"✅ Found existing CodeSystem: {system_data['name']}")
        
        # Migrate CPT codes
        print("Migrating CPT codes...")
        cpt_codes = db.query(CPTCode).all()
        for cpt in cpt_codes:
            # Create FHIR Concept
            concept = FHIRConcept(
                code_system_id=fhir_code_systems['cpt'].id,
                code=cpt.code,
                display=cpt.description,
                definition=cpt.description,
                property={
                    'category': cpt.category,
                    'section': cpt.section,
                    'subsection': cpt.subsection,
                    'is_active': cpt.is_active,
                    'effective_date': cpt.effective_date.isoformat() if cpt.effective_date else None
                }
            )
            db.add(concept)
            
            # Create legacy record for backward compatibility
            legacy_cpt = LegacyCPTCode(
                code=cpt.code,
                description=cpt.description,
                category=cpt.category,
                section=cpt.section,
                subsection=cpt.subsection,
                is_active=cpt.is_active,
                effective_date=cpt.effective_date,
                created_at=cpt.created_at
            )
            db.add(legacy_cpt)
        
        # Migrate ICD-10 codes
        print("Migrating ICD-10 codes...")
        icd10_codes = db.query(ICD10Code).all()
        for icd10 in icd10_codes:
            # Create FHIR Concept
            concept = FHIRConcept(
                code_system_id=fhir_code_systems['icd10'].id,
                code=icd10.code,
                display=icd10.description,
                definition=icd10.description,
                property={
                    'code_type': icd10.code_type,
                    'chapter': icd10.chapter,
                    'block': icd10.block,
                    'is_billable': icd10.is_billable,
                    'is_active': icd10.is_active,
                    'effective_date': icd10.effective_date.isoformat() if icd10.effective_date else None
                }
            )
            db.add(concept)
            
            # Create legacy record for backward compatibility
            legacy_icd10 = LegacyICD10Code(
                code=icd10.code,
                description=icd10.description,
                code_type=icd10.code_type,
                chapter=icd10.chapter,
                block=icd10.block,
                is_billable=icd10.is_billable,
                is_active=icd10.is_active,
                effective_date=icd10.effective_date,
                created_at=icd10.created_at
            )
            db.add(legacy_icd10)
        
        # Migrate HCPCS codes
        print("Migrating HCPCS codes...")
        hcpcs_codes = db.query(HCPCSCode).all()
        for hcpcs in hcpcs_codes:
            # Create FHIR Concept
            concept = FHIRConcept(
                code_system_id=fhir_code_systems['hcpcs'].id,
                code=hcpcs.code,
                display=hcpcs.description,
                definition=hcpcs.description,
                property={
                    'level': hcpcs.level,
                    'category': hcpcs.category,
                    'coverage_status': hcpcs.coverage_status,
                    'is_active': hcpcs.is_active,
                    'effective_date': hcpcs.effective_date.isoformat() if hcpcs.effective_date else None
                }
            )
            db.add(concept)
            
            # Create legacy record for backward compatibility
            legacy_hcpcs = LegacyHCPCSCode(
                code=hcpcs.code,
                description=hcpcs.description,
                level=hcpcs.level,
                category=hcpcs.category,
                coverage_status=hcpcs.coverage_status,
                is_active=hcpcs.is_active,
                effective_date=hcpcs.effective_date,
                created_at=hcpcs.created_at
            )
            db.add(legacy_hcpcs)
        
        # Migrate Modifier codes
        print("Migrating Modifier codes...")
        modifier_codes = db.query(ModifierCode).all()
        for modifier in modifier_codes:
            # Create FHIR Concept
            concept = FHIRConcept(
                code_system_id=fhir_code_systems['modifiers'].id,
                code=modifier.modifier,
                display=modifier.description,
                definition=modifier.description,
                property={
                    'category': modifier.category,
                    'applies_to': modifier.applies_to,
                    'is_active': modifier.is_active
                }
            )
            db.add(concept)
            
            # Create legacy record for backward compatibility
            legacy_modifier = LegacyModifierCode(
                modifier=modifier.modifier,
                description=modifier.description,
                category=modifier.category,
                applies_to=modifier.applies_to,
                is_active=modifier.is_active,
                created_at=modifier.created_at
            )
            db.add(legacy_modifier)
        
        # Update CodeSystem counts
        for system_key, code_system in fhir_code_systems.items():
            count = db.query(FHIRConcept).filter(FHIRConcept.code_system_id == code_system.id).count()
            code_system.count = count
        
        db.commit()
        print("✅ Data migration completed successfully!")
        
        # Print migration summary
        print("\n📊 Migration Summary:")
        for system_key, code_system in fhir_code_systems.items():
            count = db.query(FHIRConcept).filter(FHIRConcept.code_system_id == code_system.id).count()
            print(f"  {code_system.name}: {count} concepts")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error during migration: {e}")
        raise
    finally:
        db.close()

def create_fhir_valuesets():
    """Create FHIR ValueSets for common code groupings"""
    print("Creating FHIR ValueSets...")
    
    db = SessionLocal()
    try:
        # Create ValueSets for different specialties
        valuesets = [
            {
                'url': 'http://medicalcodes.example.com/valueset/psychiatry-codes',
                'name': 'PsychiatryCodes',
                'title': 'Psychiatry Medical Codes',
                'description': 'Medical codes commonly used in psychiatry practice',
                'publisher': 'Medical Codes System',
                'compose': {
                    'include': [
                        {
                            'system': 'http://www.ama-assn.org/go/cpt',
                            'filter': [
                                {
                                    'property': 'section',
                                    'op': '=',
                                    'value': 'Medicine'
                                }
                            ]
                        }
                    ]
                }
            },
            {
                'url': 'http://medicalcodes.example.com/valueset/primary-care-codes',
                'name': 'PrimaryCareCodes',
                'title': 'Primary Care Medical Codes',
                'description': 'Medical codes commonly used in primary care practice',
                'publisher': 'Medical Codes System',
                'compose': {
                    'include': [
                        {
                            'system': 'http://www.ama-assn.org/go/cpt',
                            'filter': [
                                {
                                    'property': 'section',
                                    'op': '=',
                                    'value': 'Evaluation and Management'
                                }
                            ]
                        }
                    ]
                }
            }
        ]
        
        for vs_data in valuesets:
            existing = db.query(FHIRValueSet).filter(FHIRValueSet.url == vs_data['url']).first()
            if not existing:
                valueset = FHIRValueSet(
                    url=vs_data['url'],
                    name=vs_data['name'],
                    title=vs_data['title'],
                    description=vs_data['description'],
                    publisher=vs_data['publisher'],
                    compose=vs_data['compose'],
                    status='active',
                    date=datetime.utcnow()
                )
                db.add(valueset)
                print(f"✅ Created ValueSet: {vs_data['name']}")
        
        db.commit()
        print("✅ ValueSets created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating ValueSets: {e}")
        raise
    finally:
        db.close()

def run_fhir_migration():
    """Run complete FHIR migration"""
    print("🚀 Starting FHIR Schema Migration...")
    
    try:
        # Step 1: Create FHIR schema
        create_fhir_schema()
        
        # Step 2: Migrate existing data
        migrate_existing_data()
        
        # Step 3: Create ValueSets
        create_fhir_valuesets()
        
        print("🎉 FHIR migration completed successfully!")
        print("\n📋 Migration Results:")
        print("  ✅ FHIR CodeSystems created")
        print("  ✅ FHIR Concepts migrated")
        print("  ✅ Legacy tables maintained for backward compatibility")
        print("  ✅ FHIR ValueSets created")
        print("  ✅ All data preserved and accessible")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    run_fhir_migration() 