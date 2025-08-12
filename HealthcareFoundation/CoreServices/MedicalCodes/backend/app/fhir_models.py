#!/usr/bin/env python3
"""
FHIR-Compliant Models for Medical Codes
Uses FHIR CodeSystem and ValueSet resources for interoperability
"""

from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class FHIRCodeSystem(Base):
    """FHIR CodeSystem resource for medical coding systems"""
    __tablename__ = "fhir_code_systems"
    
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(50), default="CodeSystem", nullable=False)
    url = Column(String(500), unique=True, nullable=False)  # Canonical URL
    version = Column(String(50))
    name = Column(String(200), nullable=False)
    title = Column(String(200))
    status = Column(String(20), default="active")  # draft, active, retired, unknown
    experimental = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.utcnow)
    publisher = Column(String(200))
    description = Column(Text)
    purpose = Column(Text)
    copyright = Column(Text)
    case_sensitive = Column(Boolean, default=True)
    compositional = Column(Boolean, default=False)
    version_needed = Column(Boolean, default=False)
    content = Column(String(20), default="complete")  # not-present, example, fragment, complete, supplement
    supplements = Column(String(500))  # Canonical URL of CodeSystem this supplements
    count = Column(Integer, default=0)  # Total number of concepts
    filter = Column(JSON)  # Filter properties
    property = Column(JSON)  # Additional properties
    concept = Column(JSON)  # Concepts in the code system
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    concepts = relationship("FHIRConcept", back_populates="code_system")
    
    __table_args__ = (
        Index('idx_codesystem_url', 'url'),
        Index('idx_codesystem_name', 'name'),
        Index('idx_codesystem_status', 'status'),
    )

class FHIRConcept(Base):
    """FHIR Concept within a CodeSystem"""
    __tablename__ = "fhir_concepts"
    
    id = Column(Integer, primary_key=True, index=True)
    code_system_id = Column(Integer, ForeignKey("fhir_code_systems.id"), nullable=False)
    code = Column(String(50), nullable=False)  # Code that identifies the concept
    display = Column(String(500), nullable=False)  # Human readable name
    definition = Column(Text)  # Formal definition
    designation = Column(JSON)  # Additional representations
    property = Column(JSON)  # Property values for the concept
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    code_system = relationship("FHIRCodeSystem", back_populates="concepts")
    
    __table_args__ = (
        Index('idx_concept_code', 'code'),
        Index('idx_concept_display', 'display'),
        Index('idx_concept_codesystem', 'code_system_id'),
        Index('idx_concept_code_display', 'code', 'display'),
    )

class FHIRValueSet(Base):
    """FHIR ValueSet resource for medical code sets"""
    __tablename__ = "fhir_value_sets"
    
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(50), default="ValueSet", nullable=False)
    url = Column(String(500), unique=True, nullable=False)  # Canonical URL
    version = Column(String(50))
    name = Column(String(200), nullable=False)
    title = Column(String(200))
    status = Column(String(20), default="active")  # draft, active, retired, unknown
    experimental = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.utcnow)
    publisher = Column(String(200))
    description = Column(Text)
    purpose = Column(Text)
    copyright = Column(Text)
    immutable = Column(Boolean, default=False)
    compose = Column(JSON)  # Content logical definition
    expansion = Column(JSON)  # Used when the value set is "expanded"
    scope = Column(JSON)  # Description of the scope and usage
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_valueset_url', 'url'),
        Index('idx_valueset_name', 'name'),
        Index('idx_valueset_status', 'status'),
    )

class FHIRConceptMap(Base):
    """FHIR ConceptMap for mapping between code systems"""
    __tablename__ = "fhir_concept_maps"
    
    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(50), default="ConceptMap", nullable=False)
    url = Column(String(500), unique=True, nullable=False)  # Canonical URL
    version = Column(String(50))
    name = Column(String(200), nullable=False)
    title = Column(String(200))
    status = Column(String(20), default="active")  # draft, active, retired, unknown
    experimental = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.utcnow)
    publisher = Column(String(200))
    description = Column(Text)
    purpose = Column(Text)
    copyright = Column(Text)
    source_uri = Column(String(500))  # Source value set
    source_canonical = Column(String(500))  # Source value set (canonical)
    target_uri = Column(String(500))  # Target value set
    target_canonical = Column(String(500))  # Target value set (canonical)
    group = Column(JSON)  # Mappings for a set of concepts
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_conceptmap_url', 'url'),
        Index('idx_conceptmap_name', 'name'),
        Index('idx_conceptmap_status', 'status'),
    )

# Legacy compatibility models (for backward compatibility)
class LegacyCPTCode(Base):
    """Legacy CPT Code model for backward compatibility"""
    __tablename__ = "legacy_cpt_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), index=True)
    section = Column(String(100), index=True)
    subsection = Column(String(200))
    is_active = Column(String(1), default='Y')
    effective_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_legacy_cpt_code_desc', 'code', 'description'),
        Index('idx_legacy_cpt_category_section', 'category', 'section'),
    )

class LegacyICD10Code(Base):
    """Legacy ICD-10 Code model for backward compatibility"""
    __tablename__ = "legacy_icd10_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    code_type = Column(String(20), index=True)
    chapter = Column(String(200), index=True)
    block = Column(String(200))
    is_billable = Column(String(1), default='Y')
    is_active = Column(String(1), default='Y')
    effective_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class LegacyHCPCSCode(Base):
    """Legacy HCPCS Code model for backward compatibility"""
    __tablename__ = "legacy_hcpcs_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    level = Column(String(10), index=True)
    category = Column(String(100), index=True)
    coverage_status = Column(String(50))
    is_active = Column(String(1), default='Y')
    effective_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class LegacyModifierCode(Base):
    """Legacy Modifier Code model for backward compatibility"""
    __tablename__ = "legacy_modifier_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    modifier = Column(String(5), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), index=True)
    applies_to = Column(String(200))
    is_active = Column(String(1), default='Y')
    created_at = Column(DateTime, default=datetime.utcnow) 