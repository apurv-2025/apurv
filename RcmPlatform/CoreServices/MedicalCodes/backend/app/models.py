from sqlalchemy import Column, String, Text, Integer, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CPTCode(Base):
    __tablename__ = "cpt_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), index=True)  # Category I, II, III
    section = Column(String(100), index=True)  # Surgery, Medicine, etc.
    subsection = Column(String(200))
    is_active = Column(String(1), default='Y')
    effective_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_cpt_code_desc', 'code', 'description'),
        Index('idx_cpt_category_section', 'category', 'section'),
    )

class ICD10Code(Base):
    __tablename__ = "icd10_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    code_type = Column(String(20), index=True)  # Diagnosis, Procedure
    chapter = Column(String(200), index=True)
    block = Column(String(200))
    is_billable = Column(String(1), default='Y')
    is_active = Column(String(1), default='Y')
    effective_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class HCPCSCode(Base):
    __tablename__ = "hcpcs_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    level = Column(String(10), index=True)  # Level I (CPT), Level II
    category = Column(String(100), index=True)
    coverage_status = Column(String(50))
    is_active = Column(String(1), default='Y')
    effective_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class ModifierCode(Base):
    __tablename__ = "modifier_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    modifier = Column(String(5), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), index=True)
    applies_to = Column(String(200))  # What types of codes this applies to
    is_active = Column(String(1), default='Y')
    created_at = Column(DateTime, default=datetime.utcnow) 