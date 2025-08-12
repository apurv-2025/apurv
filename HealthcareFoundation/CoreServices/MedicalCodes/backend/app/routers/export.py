#!/usr/bin/env python3
"""
Export API Router
Provides endpoints for exporting medical codes to PDF and JSON formats
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from typing import List, Optional, Dict, Any
import json
import os
import logging
from datetime import datetime
import tempfile
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from ..services.comprehensive_code_database import comprehensive_db
from ..database import SessionLocal
from ..models import CPTCode, ICD10Code, HCPCSCode, ModifierCode

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/export", tags=["Export"])

def get_all_codes_from_database() -> Dict[str, List[Dict[str, Any]]]:
    """Get all codes from database organized by type and specialty"""
    db = SessionLocal()
    try:
        # Get all codes from database
        cpt_codes = db.query(CPTCode).all()
        icd10_codes = db.query(ICD10Code).all()
        hcpcs_codes = db.query(HCPCSCode).all()
        modifier_codes = db.query(ModifierCode).all()
        
        # If database is empty, try to get from comprehensive cache
        if not cpt_codes and not icd10_codes and not hcpcs_codes and not modifier_codes:
            logger.info("Database is empty, trying to get codes from comprehensive cache")
            try:
                cache_file = os.path.join(comprehensive_db.cache_dir, "comprehensive_codes.json")
                if os.path.exists(cache_file):
                    with open(cache_file, 'r') as f:
                        cache_data = json.load(f)
                    
                    # Convert cache data to the expected format
                    organized_codes = {
                        'cpt_codes': [],
                        'icd10_codes': [],
                        'hcpcs_codes': [],
                        'modifier_codes': []
                    }
                    
                    # Process cached CPT codes
                    for code in cache_data.get('cpt_codes', []):
                        code_dict = {
                            'code': code.get('code'),
                            'description': code.get('description'),
                            'category': code.get('category'),
                            'section': code.get('section'),
                            'subsection': code.get('subsection'),
                            'is_active': 'Y',
                            'effective_date': None,
                            'specialty': code.get('specialty', get_cpt_specialty(code.get('section', ''), code.get('subsection', ''))),
                            'type': 'CPT'
                        }
                        organized_codes['cpt_codes'].append(code_dict)
                    
                    # Process cached ICD-10 codes
                    for code in cache_data.get('icd10_codes', []):
                        code_dict = {
                            'code': code.get('code'),
                            'description': code.get('description'),
                            'code_type': 'Diagnosis',
                            'chapter': code.get('chapter'),
                            'is_billable': 'Y',
                            'specialty': code.get('specialty', get_icd10_specialty(code.get('chapter', ''))),
                            'type': 'ICD-10'
                        }
                        organized_codes['icd10_codes'].append(code_dict)
                    
                    # Process cached HCPCS codes
                    for code in cache_data.get('hcpcs_codes', []):
                        code_dict = {
                            'code': code.get('code'),
                            'description': code.get('description'),
                            'level': code.get('level'),
                            'category': code.get('category'),
                            'specialty': code.get('specialty', get_hcpcs_specialty(code.get('category', ''))),
                            'type': 'HCPCS'
                        }
                        organized_codes['hcpcs_codes'].append(code_dict)
                    
                    logger.info(f"Loaded {len(organized_codes['cpt_codes'])} CPT, {len(organized_codes['icd10_codes'])} ICD-10, {len(organized_codes['hcpcs_codes'])} HCPCS codes from cache")
                    return organized_codes
                    
            except Exception as e:
                logger.error(f"Error loading from cache: {e}")
        
        # Convert to dictionaries and organize by specialty
        organized_codes = {
            'cpt_codes': [],
            'icd10_codes': [],
            'hcpcs_codes': [],
            'modifier_codes': []
        }
        
        # Process CPT codes
        for code in cpt_codes:
            code_dict = {
                'code': code.code,
                'description': code.description,
                'category': code.category,
                'section': code.section,
                'subsection': code.subsection,
                'is_active': code.is_active,
                'effective_date': code.effective_date.isoformat() if code.effective_date else None,
                'specialty': get_cpt_specialty(code.section, code.subsection),
                'type': 'CPT'
            }
            organized_codes['cpt_codes'].append(code_dict)
        
        # Process ICD-10 codes
        for code in icd10_codes:
            code_dict = {
                'code': code.code,
                'description': code.description,
                'code_type': code.code_type,
                'chapter': code.chapter,
                'is_billable': code.is_billable,
                'specialty': get_icd10_specialty(code.chapter),
                'type': 'ICD-10'
            }
            organized_codes['icd10_codes'].append(code_dict)
        
        # Process HCPCS codes
        for code in hcpcs_codes:
            code_dict = {
                'code': code.code,
                'description': code.description,
                'level': code.level,
                'category': code.category,
                'specialty': get_hcpcs_specialty(code.category),
                'type': 'HCPCS'
            }
            organized_codes['hcpcs_codes'].append(code_dict)
        
        # Process Modifier codes
        for code in modifier_codes:
            code_dict = {
                'modifier': code.modifier,
                'description': code.description,
                'category': code.category,
                'applies_to': code.applies_to,
                'specialty': get_modifier_specialty(code.category),
                'type': 'Modifier'
            }
            organized_codes['modifier_codes'].append(code_dict)
        
        return organized_codes
        
    except Exception as e:
        logger.error(f"Error getting codes from database: {e}")
        return {'cpt_codes': [], 'icd10_codes': [], 'hcpcs_codes': [], 'modifier_codes': []}
    finally:
        db.close()

def get_cpt_specialty(section: str, subsection: str) -> str:
    """Map CPT section/subsection to specialty"""
    specialty_mapping = {
        'Evaluation and Management': 'Primary Care',
        'Surgery': 'Surgery',
        'Radiology': 'Radiology',
        'Pathology and Laboratory': 'Pathology',
        'Medicine': 'Primary Care'
    }
    
    if section == 'Medicine' and subsection == 'Psychiatry':
        return 'Psychiatry'
    
    return specialty_mapping.get(section, 'General')

def get_icd10_specialty(chapter: str) -> str:
    """Map ICD-10 chapter to specialty"""
    specialty_mapping = {
        'Mental, Behavioral and Neurodevelopmental disorders': 'Psychiatry',
        'Diseases of the circulatory system': 'Cardiology',
        'Diseases of the respiratory system': 'Pulmonology',
        'Diseases of the digestive system': 'Gastroenterology',
        'Diseases of the musculoskeletal system': 'Orthopedics',
        'Diseases of the genitourinary system': 'Urology',
        'Diseases of the eye and adnexa': 'Ophthalmology',
        'Diseases of the nervous system': 'Neurology',
        'Endocrine, nutritional and metabolic diseases': 'Endocrinology',
        'Diseases of the skin and subcutaneous tissue': 'Dermatology',
        'Neoplasms': 'Oncology',
        'Diseases of the blood and blood-forming organs': 'Hematology',
        'Certain infectious and parasitic diseases': 'Infectious Disease',
        'Pregnancy, childbirth and the puerperium': 'Obstetrics',
        'Certain conditions originating in the perinatal period': 'Neonatology',
        'Congenital malformations, deformations and chromosomal abnormalities': 'Pediatrics',
        'Injury, poisoning and certain other consequences of external causes': 'Emergency Medicine',
        'Symptoms, signs and abnormal clinical and laboratory findings': 'Primary Care',
        'Factors influencing health status and contact with health services': 'Primary Care'
    }
    
    return specialty_mapping.get(chapter, 'General')

def get_hcpcs_specialty(category: str) -> str:
    """Map HCPCS category to specialty"""
    specialty_mapping = {
        'Mental Health Services': 'Psychiatry',
        'Durable Medical Equipment': 'Pulmonology',
        'Prosthetics and Orthotics': 'Orthopedics',
        'Ambulance Services': 'Emergency Medicine',
        'Drugs Administered Other Than Oral Method': 'Oncology'
    }
    
    return specialty_mapping.get(category, 'General')

def get_modifier_specialty(category: str) -> str:
    """Map Modifier category to specialty"""
    specialty_mapping = {
        'Evaluation and Management': 'Primary Care',
        'Surgery': 'Surgery',
        'Telemedicine': 'Primary Care',
        'Medical Necessity': 'General',
        'Mental Health': 'Psychiatry'
    }
    
    return specialty_mapping.get(category, 'General')

def organize_by_specialty(codes: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """Organize codes by specialty"""
    specialty_organization = {}
    
    for code_type, code_list in codes.items():
        for code in code_list:
            specialty = code.get('specialty', 'General')
            if specialty not in specialty_organization:
                specialty_organization[specialty] = {
                    'cpt_codes': [],
                    'icd10_codes': [],
                    'hcpcs_codes': [],
                    'modifier_codes': []
                }
            
            specialty_organization[specialty][code_type].append(code)
    
    return specialty_organization

@router.get("/json")
async def export_to_json(
    format_type: str = Query("detailed", description="Export format: 'detailed' or 'summary'"),
    specialty_filter: Optional[str] = Query(None, description="Filter by specific specialty")
):
    """
    Export medical codes to JSON format
    
    - format_type: 'detailed' for full information, 'summary' for basic info
    - specialty_filter: Optional specialty filter (e.g., 'Psychiatry', 'Cardiology')
    """
    try:
        # Get all codes from database
        all_codes = get_all_codes_from_database()
        
        # Organize by specialty
        specialty_organized = organize_by_specialty(all_codes)
        
        # Apply specialty filter if specified
        if specialty_filter:
            if specialty_filter in specialty_organized:
                specialty_organized = {specialty_filter: specialty_organized[specialty_filter]}
            else:
                return JSONResponse(
                    content={"error": f"Specialty '{specialty_filter}' not found"},
                    status_code=404
                )
        
        # Create export data
        export_data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "format_type": format_type,
                "specialty_filter": specialty_filter,
                "total_specialties": len(specialty_organized),
                "total_codes": sum(
                    len(codes) for specialty in specialty_organized.values() 
                    for codes in specialty.values()
                )
            },
            "specialties": {}
        }
        
        # Process each specialty
        for specialty, codes in specialty_organized.items():
            specialty_data = {
                "summary": {
                    "cpt_count": len(codes['cpt_codes']),
                    "icd10_count": len(codes['icd10_codes']),
                    "hcpcs_count": len(codes['hcpcs_codes']),
                    "modifier_count": len(codes['modifier_codes']),
                    "total_count": sum(len(code_list) for code_list in codes.values())
                }
            }
            
            if format_type == "detailed":
                specialty_data["codes"] = codes
            else:
                # Summary format - just basic info
                specialty_data["codes"] = {
                    "cpt_codes": [
                        {"code": code["code"], "description": code["description"][:100] + "..." if len(code["description"]) > 100 else code["description"]}
                        for code in codes['cpt_codes']
                    ],
                    "icd10_codes": [
                        {"code": code["code"], "description": code["description"][:100] + "..." if len(code["description"]) > 100 else code["description"]}
                        for code in codes['icd10_codes']
                    ],
                    "hcpcs_codes": [
                        {"code": code["code"], "description": code["description"][:100] + "..." if len(code["description"]) > 100 else code["description"]}
                        for code in codes['hcpcs_codes']
                    ],
                    "modifier_codes": [
                        {"modifier": code["modifier"], "description": code["description"][:100] + "..." if len(code["description"]) > 100 else code["description"]}
                        for code in codes['modifier_codes']
                    ]
                }
            
            export_data["specialties"][specialty] = specialty_data
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        specialty_suffix = f"_{specialty_filter}" if specialty_filter else ""
        filename = f"medical_codes_export_{format_type}{specialty_suffix}_{timestamp}.json"
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(export_data, temp_file, indent=2)
        temp_file.close()
        
        return FileResponse(
            temp_file.name,
            media_type='application/json',
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error exporting to JSON: {e}")
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")

@router.get("/pdf")
async def export_to_pdf(
    specialty_filter: Optional[str] = Query(None, description="Filter by specific specialty"),
    include_summary: bool = Query(True, description="Include summary statistics")
):
    """
    Export medical codes to PDF format
    
    - specialty_filter: Optional specialty filter
    - include_summary: Include summary statistics page
    """
    try:
        # Get all codes from database
        all_codes = get_all_codes_from_database()
        
        # Organize by specialty
        specialty_organized = organize_by_specialty(all_codes)
        
        # Apply specialty filter if specified
        if specialty_filter:
            if specialty_filter in specialty_organized:
                specialty_organized = {specialty_filter: specialty_organized[specialty_filter]}
            else:
                raise HTTPException(status_code=404, detail=f"Specialty '{specialty_filter}' not found")
        
        # Create temporary PDF file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        specialty_suffix = f"_{specialty_filter}" if specialty_filter else ""
        filename = f"medical_codes_export{specialty_suffix}_{timestamp}.pdf"
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_file.close()
        
        # Create PDF document
        doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20
        )
        normal_style = styles['Normal']
        
        # Title page
        story.append(Paragraph("Medical Codes Database Export", title_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", normal_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Specialty Filter: {specialty_filter if specialty_filter else 'All Specialties'}", normal_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Total Specialties: {len(specialty_organized)}", normal_style))
        
        total_codes = sum(
            len(codes) for specialty in specialty_organized.values() 
            for codes in specialty.values()
        )
        story.append(Paragraph(f"Total Codes: {total_codes}", normal_style))
        story.append(PageBreak())
        
        # Summary page
        if include_summary:
            story.append(Paragraph("Summary Statistics", heading_style))
            
            summary_data = [['Specialty', 'CPT', 'ICD-10', 'HCPCS', 'Modifiers', 'Total']]
            for specialty, codes in specialty_organized.items():
                cpt_count = len(codes['cpt_codes'])
                icd10_count = len(codes['icd10_codes'])
                hcpcs_count = len(codes['hcpcs_codes'])
                modifier_count = len(codes['modifier_codes'])
                total = cpt_count + icd10_count + hcpcs_count + modifier_count
                
                summary_data.append([
                    specialty,
                    str(cpt_count),
                    str(icd10_count),
                    str(hcpcs_count),
                    str(modifier_count),
                    str(total)
                ])
            
            summary_table = Table(summary_data, colWidths=[2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(summary_table)
            story.append(PageBreak())
        
        # Process each specialty
        for specialty, codes in specialty_organized.items():
            story.append(Paragraph(f"Specialty: {specialty}", heading_style))
            
            # CPT Codes
            if codes['cpt_codes']:
                story.append(Paragraph("CPT Codes", styles['Heading3']))
                cpt_data = [['Code', 'Description', 'Category', 'Section']]
                for code in codes['cpt_codes']:
                    cpt_data.append([
                        code['code'],
                        code['description'][:60] + "..." if len(code['description']) > 60 else code['description'],
                        code.get('category', ''),
                        code.get('section', '')
                    ])
                
                cpt_table = Table(cpt_data, colWidths=[1*inch, 3*inch, 1.5*inch, 1.5*inch])
                cpt_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8)
                ]))
                story.append(cpt_table)
                story.append(Spacer(1, 12))
            
            # ICD-10 Codes
            if codes['icd10_codes']:
                story.append(Paragraph("ICD-10 Codes", styles['Heading3']))
                icd10_data = [['Code', 'Description', 'Chapter', 'Billable']]
                for code in codes['icd10_codes']:
                    icd10_data.append([
                        code['code'],
                        code['description'][:60] + "..." if len(code['description']) > 60 else code['description'],
                        code.get('chapter', ''),
                        code.get('is_billable', '')
                    ])
                
                icd10_table = Table(icd10_data, colWidths=[1*inch, 3*inch, 2*inch, 0.5*inch])
                icd10_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.green),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8)
                ]))
                story.append(icd10_table)
                story.append(Spacer(1, 12))
            
            # HCPCS Codes
            if codes['hcpcs_codes']:
                story.append(Paragraph("HCPCS Codes", styles['Heading3']))
                hcpcs_data = [['Code', 'Description', 'Category', 'Level']]
                for code in codes['hcpcs_codes']:
                    hcpcs_data.append([
                        code['code'],
                        code['description'][:60] + "..." if len(code['description']) > 60 else code['description'],
                        code.get('category', ''),
                        code.get('level', '')
                    ])
                
                hcpcs_table = Table(hcpcs_data, colWidths=[1*inch, 3*inch, 2*inch, 0.5*inch])
                hcpcs_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8)
                ]))
                story.append(hcpcs_table)
                story.append(Spacer(1, 12))
            
            # Modifier Codes
            if codes['modifier_codes']:
                story.append(Paragraph("Modifier Codes", styles['Heading3']))
                modifier_data = [['Modifier', 'Description', 'Category', 'Applies To']]
                for code in codes['modifier_codes']:
                    modifier_data.append([
                        code['modifier'],
                        code['description'][:60] + "..." if len(code['description']) > 60 else code['description'],
                        code.get('category', ''),
                        code.get('applies_to', '')
                    ])
                
                modifier_table = Table(modifier_data, colWidths=[1*inch, 3*inch, 1.5*inch, 1*inch])
                modifier_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.orange),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8)
                ]))
                story.append(modifier_table)
            
            story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        
        return FileResponse(
            temp_file.name,
            media_type='application/pdf',
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error exporting to PDF: {e}")
        raise HTTPException(status_code=500, detail=f"PDF export error: {str(e)}")

@router.get("/stats")
async def get_export_stats():
    """Get statistics for export functionality"""
    try:
        all_codes = get_all_codes_from_database()
        specialty_organized = organize_by_specialty(all_codes)
        
        stats = {
            "total_specialties": len(specialty_organized),
            "specialties": {},
            "total_codes": 0
        }
        
        for specialty, codes in specialty_organized.items():
            specialty_stats = {
                "cpt_count": len(codes['cpt_codes']),
                "icd10_count": len(codes['icd10_codes']),
                "hcpcs_count": len(codes['hcpcs_codes']),
                "modifier_count": len(codes['modifier_codes']),
                "total_count": sum(len(code_list) for code_list in codes.values())
            }
            stats["specialties"][specialty] = specialty_stats
            stats["total_codes"] += specialty_stats["total_count"]
        
        return {
            "success": True,
            "export_stats": stats,
            "available_formats": ["json", "pdf"],
            "available_specialties": list(specialty_organized.keys())
        }
        
    except Exception as e:
        logger.error(f"Error getting export stats: {e}")
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}") 