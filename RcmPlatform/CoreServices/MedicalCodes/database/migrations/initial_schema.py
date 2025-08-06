"""
Initial database schema migration
Creates all tables for medical codes
"""

from sqlalchemy import create_engine, text
import os

def run_migration():
    """Run the initial migration to create all tables"""
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://medicalcodes:secure_password_123@localhost:15432/medical_codes")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Create CPT codes table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS cpt_codes (
                id SERIAL PRIMARY KEY,
                code VARCHAR(10) UNIQUE NOT NULL,
                description TEXT NOT NULL,
                category VARCHAR(50),
                section VARCHAR(100),
                subsection VARCHAR(200),
                is_active VARCHAR(1) DEFAULT 'Y',
                effective_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create ICD-10 codes table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS icd10_codes (
                id SERIAL PRIMARY KEY,
                code VARCHAR(10) UNIQUE NOT NULL,
                description TEXT NOT NULL,
                code_type VARCHAR(20),
                chapter VARCHAR(200),
                block VARCHAR(200),
                is_billable VARCHAR(1) DEFAULT 'Y',
                is_active VARCHAR(1) DEFAULT 'Y',
                effective_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create HCPCS codes table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS hcpcs_codes (
                id SERIAL PRIMARY KEY,
                code VARCHAR(10) UNIQUE NOT NULL,
                description TEXT NOT NULL,
                level VARCHAR(10),
                category VARCHAR(100),
                coverage_status VARCHAR(50),
                is_active VARCHAR(1) DEFAULT 'Y',
                effective_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create Modifier codes table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS modifier_codes (
                id SERIAL PRIMARY KEY,
                modifier VARCHAR(5) UNIQUE NOT NULL,
                description TEXT NOT NULL,
                category VARCHAR(50),
                applies_to VARCHAR(200),
                is_active VARCHAR(1) DEFAULT 'Y',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create indexes for better performance
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_cpt_code ON cpt_codes(code)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_cpt_description ON cpt_codes(description)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_cpt_category ON cpt_codes(category)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_cpt_section ON cpt_codes(section)"))
        
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_icd10_code ON icd10_codes(code)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_icd10_description ON icd10_codes(description)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_icd10_chapter ON icd10_codes(chapter)"))
        
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_hcpcs_code ON hcpcs_codes(code)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_hcpcs_description ON hcpcs_codes(description)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_hcpcs_category ON hcpcs_codes(category)"))
        
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_modifier_code ON modifier_codes(modifier)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_modifier_description ON modifier_codes(description)"))
        
        conn.commit()
        print("Initial migration completed successfully!")

if __name__ == "__main__":
    run_migration() 