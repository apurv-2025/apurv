#!/usr/bin/env python3
"""
FHIR-Compliant API Router
Provides FHIR REST API endpoints for CodeSystem and ValueSet resources
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from ..database import SessionLocal
from ..fhir_models import FHIRCodeSystem, FHIRConcept, FHIRValueSet, FHIRConceptMap

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/fhir", tags=["FHIR"])

# FHIR CodeSystem endpoints
@router.get("/CodeSystem")
async def get_code_systems(
    url: Optional[str] = Query(None, description="Canonical URL of the code system"),
    name: Optional[str] = Query(None, description="Name of the code system"),
    status: Optional[str] = Query(None, description="Status of the code system"),
    _count: Optional[int] = Query(10, description="Number of results to return"),
    _offset: Optional[int] = Query(0, description="Number of results to skip")
):
    """
    FHIR CodeSystem search endpoint
    Follows FHIR REST API standards
    """
    try:
        db = SessionLocal()
        query = db.query(FHIRCodeSystem)
        
        # Apply filters
        if url:
            query = query.filter(FHIRCodeSystem.url.contains(url))
        if name:
            query = query.filter(FHIRCodeSystem.name.contains(name))
        if status:
            query = query.filter(FHIRCodeSystem.status == status)
        
        # Apply pagination
        total = query.count()
        code_systems = query.offset(_offset).limit(_count).all()
        
        # Convert to FHIR Bundle format
        bundle = {
            "resourceType": "Bundle",
            "type": "searchset",
            "total": total,
            "entry": []
        }
        
        for cs in code_systems:
            entry = {
                "resource": {
                    "resourceType": "CodeSystem",
                    "id": str(cs.id),
                    "url": cs.url,
                    "version": cs.version,
                    "name": cs.name,
                    "title": cs.title,
                    "status": cs.status,
                    "experimental": cs.experimental,
                    "date": cs.date.isoformat() if cs.date else None,
                    "publisher": cs.publisher,
                    "description": cs.description,
                    "purpose": cs.purpose,
                    "copyright": cs.copyright,
                    "caseSensitive": cs.case_sensitive,
                    "compositional": cs.compositional,
                    "versionNeeded": cs.version_needed,
                    "content": cs.content,
                    "supplements": cs.supplements,
                    "count": cs.count,
                    "filter": cs.filter,
                    "property": cs.property,
                    "concept": cs.concept
                }
            }
            bundle["entry"].append(entry)
        
        return bundle
        
    except Exception as e:
        logger.error(f"Error in CodeSystem search: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
    finally:
        db.close()

@router.get("/CodeSystem/{code_system_id}")
async def get_code_system(code_system_id: int = Path(..., description="CodeSystem ID")):
    """
    FHIR CodeSystem read endpoint
    """
    try:
        db = SessionLocal()
        code_system = db.query(FHIRCodeSystem).filter(FHIRCodeSystem.id == code_system_id).first()
        
        if not code_system:
            raise HTTPException(status_code=404, detail="CodeSystem not found")
        
        return {
            "resourceType": "CodeSystem",
            "id": str(code_system.id),
            "url": code_system.url,
            "version": code_system.version,
            "name": code_system.name,
            "title": code_system.title,
            "status": code_system.status,
            "experimental": code_system.experimental,
            "date": code_system.date.isoformat() if code_system.date else None,
            "publisher": code_system.publisher,
            "description": code_system.description,
            "purpose": code_system.purpose,
            "copyright": code_system.copyright,
            "caseSensitive": code_system.case_sensitive,
            "compositional": code_system.compositional,
            "versionNeeded": code_system.version_needed,
            "content": code_system.content,
            "supplements": code_system.supplements,
            "count": code_system.count,
            "filter": code_system.filter,
            "property": code_system.property,
            "concept": code_system.concept
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in CodeSystem read: {e}")
        raise HTTPException(status_code=500, detail=f"Read error: {str(e)}")
    finally:
        db.close()

@router.get("/CodeSystem/{code_system_id}/$lookup")
async def lookup_code(
    code_system_id: int = Path(..., description="CodeSystem ID"),
    code: str = Query(..., description="Code to lookup"),
    property: Optional[List[str]] = Query(None, description="Properties to return")
):
    """
    FHIR CodeSystem $lookup operation
    """
    try:
        db = SessionLocal()
        concept = db.query(FHIRConcept).filter(
            FHIRConcept.code_system_id == code_system_id,
            FHIRConcept.code == code
        ).first()
        
        if not concept:
            raise HTTPException(status_code=404, detail="Code not found")
        
        result = {
            "resourceType": "Parameters",
            "parameter": [
                {
                    "name": "name",
                    "valueString": concept.code_system.name
                },
                {
                    "name": "version",
                    "valueString": concept.code_system.version
                },
                {
                    "name": "display",
                    "valueString": concept.display
                },
                {
                    "name": "definition",
                    "valueString": concept.definition
                }
            ]
        }
        
        # Add properties if requested
        if property and concept.property:
            for prop_name in property:
                if prop_name in concept.property:
                    result["parameter"].append({
                        "name": prop_name,
                        "valueString": str(concept.property[prop_name])
                    })
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in CodeSystem lookup: {e}")
        raise HTTPException(status_code=500, detail=f"Lookup error: {str(e)}")
    finally:
        db.close()

# FHIR ValueSet endpoints
@router.get("/ValueSet")
async def get_value_sets(
    url: Optional[str] = Query(None, description="Canonical URL of the value set"),
    name: Optional[str] = Query(None, description="Name of the value set"),
    status: Optional[str] = Query(None, description="Status of the value set"),
    _count: Optional[int] = Query(10, description="Number of results to return"),
    _offset: Optional[int] = Query(0, description="Number of results to skip")
):
    """
    FHIR ValueSet search endpoint
    """
    try:
        db = SessionLocal()
        query = db.query(FHIRValueSet)
        
        # Apply filters
        if url:
            query = query.filter(FHIRValueSet.url.contains(url))
        if name:
            query = query.filter(FHIRValueSet.name.contains(name))
        if status:
            query = query.filter(FHIRValueSet.status == status)
        
        # Apply pagination
        total = query.count()
        value_sets = query.offset(_offset).limit(_count).all()
        
        # Convert to FHIR Bundle format
        bundle = {
            "resourceType": "Bundle",
            "type": "searchset",
            "total": total,
            "entry": []
        }
        
        for vs in value_sets:
            entry = {
                "resource": {
                    "resourceType": "ValueSet",
                    "id": str(vs.id),
                    "url": vs.url,
                    "version": vs.version,
                    "name": vs.name,
                    "title": vs.title,
                    "status": vs.status,
                    "experimental": vs.experimental,
                    "date": vs.date.isoformat() if vs.date else None,
                    "publisher": vs.publisher,
                    "description": vs.description,
                    "purpose": vs.purpose,
                    "copyright": vs.copyright,
                    "immutable": vs.immutable,
                    "compose": vs.compose,
                    "expansion": vs.expansion,
                    "scope": vs.scope
                }
            }
            bundle["entry"].append(entry)
        
        return bundle
        
    except Exception as e:
        logger.error(f"Error in ValueSet search: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
    finally:
        db.close()

@router.get("/ValueSet/{value_set_id}")
async def get_value_set(value_set_id: int = Path(..., description="ValueSet ID")):
    """
    FHIR ValueSet read endpoint
    """
    try:
        db = SessionLocal()
        value_set = db.query(FHIRValueSet).filter(FHIRValueSet.id == value_set_id).first()
        
        if not value_set:
            raise HTTPException(status_code=404, detail="ValueSet not found")
        
        return {
            "resourceType": "ValueSet",
            "id": str(value_set.id),
            "url": value_set.url,
            "version": value_set.version,
            "name": value_set.name,
            "title": value_set.title,
            "status": value_set.status,
            "experimental": value_set.experimental,
            "date": value_set.date.isoformat() if value_set.date else None,
            "publisher": value_set.publisher,
            "description": value_set.description,
            "purpose": value_set.purpose,
            "copyright": value_set.copyright,
            "immutable": value_set.immutable,
            "compose": value_set.compose,
            "expansion": value_set.expansion,
            "scope": value_set.scope
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in ValueSet read: {e}")
        raise HTTPException(status_code=500, detail=f"Read error: {str(e)}")
    finally:
        db.close()

@router.get("/ValueSet/{value_set_id}/$expand")
async def expand_value_set(
    value_set_id: int = Path(..., description="ValueSet ID"),
    count: Optional[int] = Query(10, description="Number of results to return"),
    offset: Optional[int] = Query(0, description="Number of results to skip")
):
    """
    FHIR ValueSet $expand operation
    """
    try:
        db = SessionLocal()
        value_set = db.query(FHIRValueSet).filter(FHIRValueSet.id == value_set_id).first()
        
        if not value_set:
            raise HTTPException(status_code=404, detail="ValueSet not found")
        
        # For now, return a simple expansion
        # In a full implementation, this would evaluate the compose criteria
        expansion = {
            "resourceType": "ValueSet",
            "id": str(value_set.id),
            "url": value_set.url,
            "version": value_set.version,
            "name": value_set.name,
            "title": value_set.title,
            "status": value_set.status,
            "expansion": {
                "identifier": f"expand-{value_set.id}",
                "timestamp": datetime.utcnow().isoformat(),
                "total": 0,
                "offset": offset,
                "parameter": [
                    {
                        "name": "count",
                        "valueInteger": count
                    },
                    {
                        "name": "offset",
                        "valueInteger": offset
                    }
                ],
                "contains": []
            }
        }
        
        return expansion
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in ValueSet expand: {e}")
        raise HTTPException(status_code=500, detail=f"Expand error: {str(e)}")
    finally:
        db.close()

# FHIR ConceptMap endpoints
@router.get("/ConceptMap")
async def get_concept_maps(
    url: Optional[str] = Query(None, description="Canonical URL of the concept map"),
    name: Optional[str] = Query(None, description="Name of the concept map"),
    status: Optional[str] = Query(None, description="Status of the concept map"),
    _count: Optional[int] = Query(10, description="Number of results to return"),
    _offset: Optional[int] = Query(0, description="Number of results to skip")
):
    """
    FHIR ConceptMap search endpoint
    """
    try:
        db = SessionLocal()
        query = db.query(FHIRConceptMap)
        
        # Apply filters
        if url:
            query = query.filter(FHIRConceptMap.url.contains(url))
        if name:
            query = query.filter(FHIRConceptMap.name.contains(name))
        if status:
            query = query.filter(FHIRConceptMap.status == status)
        
        # Apply pagination
        total = query.count()
        concept_maps = query.offset(_offset).limit(_count).all()
        
        # Convert to FHIR Bundle format
        bundle = {
            "resourceType": "Bundle",
            "type": "searchset",
            "total": total,
            "entry": []
        }
        
        for cm in concept_maps:
            entry = {
                "resource": {
                    "resourceType": "ConceptMap",
                    "id": str(cm.id),
                    "url": cm.url,
                    "version": cm.version,
                    "name": cm.name,
                    "title": cm.title,
                    "status": cm.status,
                    "experimental": cm.experimental,
                    "date": cm.date.isoformat() if cm.date else None,
                    "publisher": cm.publisher,
                    "description": cm.description,
                    "purpose": cm.purpose,
                    "copyright": cm.copyright,
                    "sourceUri": cm.source_uri,
                    "sourceCanonical": cm.source_canonical,
                    "targetUri": cm.target_uri,
                    "targetCanonical": cm.target_canonical,
                    "group": cm.group
                }
            }
            bundle["entry"].append(entry)
        
        return bundle
        
    except Exception as e:
        logger.error(f"Error in ConceptMap search: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")
    finally:
        db.close()

# FHIR metadata endpoint
@router.get("/metadata")
async def get_fhir_metadata():
    """
    FHIR CapabilityStatement endpoint
    """
    return {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": datetime.utcnow().isoformat(),
        "publisher": "Medical Codes System",
        "kind": "instance",
        "software": {
            "name": "Medical Codes FHIR Server",
            "version": "1.0.0"
        },
        "implementation": {
            "url": "http://localhost:8003/fhir",
            "description": "Medical Codes FHIR Server"
        },
        "fhirVersion": "4.0.1",
        "format": ["json"],
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "CodeSystem",
                        "profile": "http://hl7.org/fhir/StructureDefinition/CodeSystem",
                        "interaction": [
                            {"code": "read"},
                            {"code": "search-type"}
                        ],
                        "searchParam": [
                            {"name": "url", "type": "uri"},
                            {"name": "name", "type": "string"},
                            {"name": "status", "type": "token"}
                        ]
                    },
                    {
                        "type": "ValueSet",
                        "profile": "http://hl7.org/fhir/StructureDefinition/ValueSet",
                        "interaction": [
                            {"code": "read"},
                            {"code": "search-type"}
                        ],
                        "searchParam": [
                            {"name": "url", "type": "uri"},
                            {"name": "name", "type": "string"},
                            {"name": "status", "type": "token"}
                        ]
                    },
                    {
                        "type": "ConceptMap",
                        "profile": "http://hl7.org/fhir/StructureDefinition/ConceptMap",
                        "interaction": [
                            {"code": "read"},
                            {"code": "search-type"}
                        ],
                        "searchParam": [
                            {"name": "url", "type": "uri"},
                            {"name": "name", "type": "string"},
                            {"name": "status", "type": "token"}
                        ]
                    }
                ]
            }
        ]
    } 