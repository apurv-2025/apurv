from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CPTCodeResponse(BaseModel):
    id: int
    code: str
    description: str
    category: Optional[str]
    section: Optional[str]
    subsection: Optional[str]
    is_active: str
    effective_date: Optional[datetime]
    
    class Config:
        from_attributes = True

class ICD10CodeResponse(BaseModel):
    id: int
    code: str
    description: str
    code_type: Optional[str]
    chapter: Optional[str]
    block: Optional[str]
    is_billable: str
    is_active: str
    effective_date: Optional[datetime]
    
    class Config:
        from_attributes = True

class HCPCSCodeResponse(BaseModel):
    id: int
    code: str
    description: str
    level: Optional[str]
    category: Optional[str]
    coverage_status: Optional[str]
    is_active: str
    effective_date: Optional[datetime]
    
    class Config:
        from_attributes = True

class ModifierCodeResponse(BaseModel):
    id: int
    modifier: str
    description: str
    category: Optional[str]
    applies_to: Optional[str]
    is_active: str
    
    class Config:
        from_attributes = True

class SearchResults(BaseModel):
    cpt_codes: List[CPTCodeResponse]
    icd10_codes: List[ICD10CodeResponse]
    hcpcs_codes: List[HCPCSCodeResponse]
    modifier_codes: List[ModifierCodeResponse]
    total_results: int

class CategoriesResponse(BaseModel):
    cpt_categories: List[str]
    icd10_chapters: List[str]
    hcpcs_categories: List[str]

class StatsResponse(BaseModel):
    total_cpt_codes: int
    total_icd10_codes: int
    total_hcpcs_codes: int
    total_modifier_codes: int
    active_cpt_codes: int
    active_icd10_codes: int
    active_hcpcs_codes: int 