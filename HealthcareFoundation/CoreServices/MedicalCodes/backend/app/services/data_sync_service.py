#!/usr/bin/env python3
"""
Data Synchronization Service for Medical Codes
Fetches and integrates data from official sources:
- AMA CPT: https://www.ama-assn.org/practice-management/cpt
- CMS ICD-10: https://www.cms.gov/medicare/coding-billing/icd-10-codes
- CMS HCPCS: https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system
"""

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import re
from dataclasses import dataclass
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import CPTCode, ICD10Code, HCPCSCode, ModifierCode
import time
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CodeUpdate:
    """Represents a code update from external sources"""
    code: str
    description: str
    category: Optional[str] = None
    section: Optional[str] = None
    subsection: Optional[str] = None
    effective_date: Optional[datetime] = None
    source: str = ""
    is_active: str = "Y"
    additional_data: Dict[str, Any] = None

class DataSyncService:
    """Service for synchronizing medical codes from official sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Official source URLs
        self.sources = {
            'cpt': {
                'url': 'https://www.ama-assn.org/practice-management/cpt',
                'name': 'AMA CPT',
                'description': 'Current Procedural Terminology codes maintained by American Medical Association'
            },
            'icd10': {
                'url': 'https://www.cms.gov/medicare/coding-billing/icd-10-codes',
                'name': 'CMS ICD-10',
                'description': 'International Classification of Diseases, 10th Revision codes'
            },
            'hcpcs': {
                'url': 'https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system',
                'name': 'CMS HCPCS',
                'description': 'Healthcare Common Procedure Coding System Level II codes'
            }
        }
        
        # API endpoints for structured data (if available)
        self.api_endpoints = {
            'cpt': 'https://www.ama-assn.org/api/cpt-codes',
            'icd10': 'https://www.cms.gov/api/icd10-codes',
            'hcpcs': 'https://www.cms.gov/api/hcpcs-codes'
        }

    async def fetch_cpt_data(self) -> List[CodeUpdate]:
        """Fetch CPT codes from AMA website"""
        logger.info("Fetching CPT data from AMA...")
        
        try:
            # Try to fetch from AMA's structured API first
            cpt_data = await self._fetch_structured_cpt_data()
            if cpt_data:
                return cpt_data
            
            # Fallback to web scraping
            return await self._scrape_cpt_data()
            
        except Exception as e:
            logger.error(f"Error fetching CPT data: {e}")
            return []

    async def fetch_icd10_data(self) -> List[CodeUpdate]:
        """Fetch ICD-10 codes from CMS website"""
        logger.info("Fetching ICD-10 data from CMS...")
        
        try:
            # Try to fetch from CMS's structured API first
            icd10_data = await self._fetch_structured_icd10_data()
            if icd10_data:
                return icd10_data
            
            # Fallback to web scraping
            return await self._scrape_icd10_data()
            
        except Exception as e:
            logger.error(f"Error fetching ICD-10 data: {e}")
            return []

    async def fetch_hcpcs_data(self) -> List[CodeUpdate]:
        """Fetch HCPCS codes from CMS website"""
        logger.info("Fetching HCPCS data from CMS...")
        
        try:
            # Try to fetch from CMS's structured API first
            hcpcs_data = await self._fetch_structured_hcpcs_data()
            if hcpcs_data:
                return hcpcs_data
            
            # Fallback to web scraping
            return await self._scrape_hcpcs_data()
            
        except Exception as e:
            logger.error(f"Error fetching HCPCS data: {e}")
            return []

    async def _fetch_structured_cpt_data(self) -> List[CodeUpdate]:
        """Attempt to fetch structured CPT data from AMA API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_endpoints['cpt']) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_structured_cpt_data(data)
        except Exception as e:
            logger.warning(f"Structured CPT API not available: {e}")
        return []

    async def _fetch_structured_icd10_data(self) -> List[CodeUpdate]:
        """Attempt to fetch structured ICD-10 data from CMS API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_endpoints['icd10']) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_structured_icd10_data(data)
        except Exception as e:
            logger.warning(f"Structured ICD-10 API not available: {e}")
        return []

    async def _fetch_structured_hcpcs_data(self) -> List[CodeUpdate]:
        """Attempt to fetch structured HCPCS data from CMS API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_endpoints['hcpcs']) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_structured_hcpcs_data(data)
        except Exception as e:
            logger.warning(f"Structured HCPCS API not available: {e}")
        return []

    async def _scrape_cpt_data(self) -> List[CodeUpdate]:
        """Scrape CPT data from AMA website"""
        try:
            response = self.session.get(self.sources['cpt']['url'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            cpt_codes = []
            
            # Look for CPT code tables or lists
            # This is a generic approach - actual implementation would need to be adapted
            # based on the specific structure of the AMA website
            
            # Example patterns to look for:
            code_elements = soup.find_all(['div', 'span', 'td'], 
                                        string=re.compile(r'^\d{5}$'))  # 5-digit CPT codes
            
            for element in code_elements:
                code = element.get_text().strip()
                description_element = element.find_next_sibling(['div', 'span', 'td'])
                description = description_element.get_text().strip() if description_element else ""
                
                if code and description:
                    cpt_codes.append(CodeUpdate(
                        code=code,
                        description=description,
                        category="Category I",  # Default, would need to be determined from context
                        source="AMA CPT"
                    ))
            
            logger.info(f"Scraped {len(cpt_codes)} CPT codes from AMA website")
            return cpt_codes
            
        except Exception as e:
            logger.error(f"Error scraping CPT data: {e}")
            return []

    async def _scrape_icd10_data(self) -> List[CodeUpdate]:
        """Scrape ICD-10 data from CMS website"""
        try:
            response = self.session.get(self.sources['icd10']['url'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            icd10_codes = []
            
            # Look for ICD-10 code patterns (letters followed by numbers)
            code_elements = soup.find_all(['div', 'span', 'td'], 
                                        string=re.compile(r'^[A-Z]\d{2}(\.\d{1,2})?$'))
            
            for element in code_elements:
                code = element.get_text().strip()
                description_element = element.find_next_sibling(['div', 'span', 'td'])
                description = description_element.get_text().strip() if description_element else ""
                
                if code and description:
                    icd10_codes.append(CodeUpdate(
                        code=code,
                        description=description,
                        code_type="Diagnosis",  # Default
                        source="CMS ICD-10"
                    ))
            
            logger.info(f"Scraped {len(icd10_codes)} ICD-10 codes from CMS website")
            return icd10_codes
            
        except Exception as e:
            logger.error(f"Error scraping ICD-10 data: {e}")
            return []

    async def _scrape_hcpcs_data(self) -> List[CodeUpdate]:
        """Scrape HCPCS data from CMS website"""
        try:
            response = self.session.get(self.sources['hcpcs']['url'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            hcpcs_codes = []
            
            # Look for HCPCS code patterns (letter followed by 4 digits)
            code_elements = soup.find_all(['div', 'span', 'td'], 
                                        string=re.compile(r'^[A-Z]\d{4}$'))
            
            for element in code_elements:
                code = element.get_text().strip()
                description_element = element.find_next_sibling(['div', 'span', 'td'])
                description = description_element.get_text().strip() if description_element else ""
                
                if code and description:
                    hcpcs_codes.append(CodeUpdate(
                        code=code,
                        description=description,
                        level="Level II",  # Default for HCPCS
                        source="CMS HCPCS"
                    ))
            
            logger.info(f"Scraped {len(hcpcs_codes)} HCPCS codes from CMS website")
            return hcpcs_codes
            
        except Exception as e:
            logger.error(f"Error scraping HCPCS data: {e}")
            return []

    def _parse_structured_cpt_data(self, data: Dict) -> List[CodeUpdate]:
        """Parse structured CPT data from API response"""
        cpt_codes = []
        try:
            for item in data.get('codes', []):
                cpt_codes.append(CodeUpdate(
                    code=item.get('code', ''),
                    description=item.get('description', ''),
                    category=item.get('category', 'Category I'),
                    section=item.get('section', ''),
                    subsection=item.get('subsection', ''),
                    effective_date=item.get('effective_date'),
                    source="AMA CPT API"
                ))
        except Exception as e:
            logger.error(f"Error parsing structured CPT data: {e}")
        return cpt_codes

    def _parse_structured_icd10_data(self, data: Dict) -> List[CodeUpdate]:
        """Parse structured ICD-10 data from API response"""
        icd10_codes = []
        try:
            for item in data.get('codes', []):
                icd10_codes.append(CodeUpdate(
                    code=item.get('code', ''),
                    description=item.get('description', ''),
                    code_type=item.get('code_type', 'Diagnosis'),
                    chapter=item.get('chapter', ''),
                    block=item.get('block', ''),
                    is_billable=item.get('is_billable', 'Y'),
                    source="CMS ICD-10 API"
                ))
        except Exception as e:
            logger.error(f"Error parsing structured ICD-10 data: {e}")
        return icd10_codes

    def _parse_structured_hcpcs_data(self, data: Dict) -> List[CodeUpdate]:
        """Parse structured HCPCS data from API response"""
        hcpcs_codes = []
        try:
            for item in data.get('codes', []):
                hcpcs_codes.append(CodeUpdate(
                    code=item.get('code', ''),
                    description=item.get('description', ''),
                    level=item.get('level', 'Level II'),
                    category=item.get('category', ''),
                    coverage_status=item.get('coverage_status', ''),
                    source="CMS HCPCS API"
                ))
        except Exception as e:
            logger.error(f"Error parsing structured HCPCS data: {e}")
        return hcpcs_codes

    async def sync_all_data(self) -> Dict[str, int]:
        """Synchronize all medical codes from official sources"""
        logger.info("Starting full data synchronization...")
        
        results = {
            'cpt_codes': 0,
            'icd10_codes': 0,
            'hcpcs_codes': 0,
            'errors': 0
        }
        
        try:
            # Fetch data from all sources concurrently
            cpt_task = self.fetch_cpt_data()
            icd10_task = self.fetch_icd10_data()
            hcpcs_task = self.fetch_hcpcs_data()
            
            cpt_codes, icd10_codes, hcpcs_codes = await asyncio.gather(
                cpt_task, icd10_task, hcpcs_task, return_exceptions=True
            )
            
            # Process CPT codes
            if isinstance(cpt_codes, list):
                results['cpt_codes'] = await self._update_cpt_codes(cpt_codes)
            else:
                logger.error(f"CPT data fetch failed: {cpt_codes}")
                results['errors'] += 1
            
            # Process ICD-10 codes
            if isinstance(icd10_codes, list):
                results['icd10_codes'] = await self._update_icd10_codes(icd10_codes)
            else:
                logger.error(f"ICD-10 data fetch failed: {icd10_codes}")
                results['errors'] += 1
            
            # Process HCPCS codes
            if isinstance(hcpcs_codes, list):
                results['hcpcs_codes'] = await self._update_hcpcs_codes(hcpcs_codes)
            else:
                logger.error(f"HCPCS data fetch failed: {hcpcs_codes}")
                results['errors'] += 1
            
            logger.info(f"Data synchronization completed: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error during data synchronization: {e}")
            results['errors'] += 1
            return results

    async def _update_cpt_codes(self, code_updates: List[CodeUpdate]) -> int:
        """Update CPT codes in database"""
        db = SessionLocal()
        try:
            updated_count = 0
            for update in code_updates:
                existing = db.query(CPTCode).filter(CPTCode.code == update.code).first()
                
                if existing:
                    # Update existing code
                    existing.description = update.description
                    existing.category = update.category or existing.category
                    existing.section = update.section or existing.section
                    existing.subsection = update.subsection or existing.subsection
                    if update.effective_date:
                        existing.effective_date = update.effective_date
                else:
                    # Create new code
                    new_code = CPTCode(
                        code=update.code,
                        description=update.description,
                        category=update.category or "Category I",
                        section=update.section or "",
                        subsection=update.subsection or "",
                        effective_date=update.effective_date,
                        is_active=update.is_active
                    )
                    db.add(new_code)
                
                updated_count += 1
            
            db.commit()
            logger.info(f"Updated {updated_count} CPT codes")
            return updated_count
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating CPT codes: {e}")
            return 0
        finally:
            db.close()

    async def _update_icd10_codes(self, code_updates: List[CodeUpdate]) -> int:
        """Update ICD-10 codes in database"""
        db = SessionLocal()
        try:
            updated_count = 0
            for update in code_updates:
                existing = db.query(ICD10Code).filter(ICD10Code.code == update.code).first()
                
                if existing:
                    # Update existing code
                    existing.description = update.description
                    existing.code_type = update.code_type or existing.code_type
                    existing.chapter = update.chapter or existing.chapter
                    existing.block = update.block or existing.block
                    existing.is_billable = update.is_billable or existing.is_billable
                else:
                    # Create new code
                    new_code = ICD10Code(
                        code=update.code,
                        description=update.description,
                        code_type=update.code_type or "Diagnosis",
                        chapter=update.chapter or "",
                        block=update.block or "",
                        is_billable=update.is_billable or "Y",
                        is_active=update.is_active
                    )
                    db.add(new_code)
                
                updated_count += 1
            
            db.commit()
            logger.info(f"Updated {updated_count} ICD-10 codes")
            return updated_count
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating ICD-10 codes: {e}")
            return 0
        finally:
            db.close()

    async def _update_hcpcs_codes(self, code_updates: List[CodeUpdate]) -> int:
        """Update HCPCS codes in database"""
        db = SessionLocal()
        try:
            updated_count = 0
            for update in code_updates:
                existing = db.query(HCPCSCode).filter(HCPCSCode.code == update.code).first()
                
                if existing:
                    # Update existing code
                    existing.description = update.description
                    existing.level = update.level or existing.level
                    existing.category = update.category or existing.category
                    existing.coverage_status = update.coverage_status or existing.coverage_status
                else:
                    # Create new code
                    new_code = HCPCSCode(
                        code=update.code,
                        description=update.description,
                        level=update.level or "Level II",
                        category=update.category or "",
                        coverage_status=update.coverage_status or "",
                        is_active=update.is_active
                    )
                    db.add(new_code)
                
                updated_count += 1
            
            db.commit()
            logger.info(f"Updated {updated_count} HCPCS codes")
            return updated_count
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating HCPCS codes: {e}")
            return 0
        finally:
            db.close()

    def get_sync_status(self) -> Dict[str, Any]:
        """Get the status of the last synchronization"""
        return {
            'last_sync': datetime.now().isoformat(),
            'sources': self.sources,
            'status': 'ready'
        }

# Global instance
data_sync_service = DataSyncService() 