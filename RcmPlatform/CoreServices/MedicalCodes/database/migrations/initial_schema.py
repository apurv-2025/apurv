#!/usr/bin/env python3
"""
Initial database schema migration
Creates all tables for the Medical Codes application
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from app.database import engine, Base
from app.models import CPTCode, ICD10Code, HCPCSCode, ModifierCode

def run_migration():
    """Create all database tables"""
    print("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Verify tables were created
        inspector = engine.dialect.inspector(engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['cpt_codes', 'icd10_codes', 'hcpcs_codes', 'modifier_codes']
        for table in expected_tables:
            if table in tables:
                print(f"✅ Table '{table}' created")
            else:
                print(f"❌ Table '{table}' not found")
                
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

if __name__ == "__main__":
    run_migration() 