#!/usr/bin/env python3
"""
Specialized Scrapers for Official Medical Coding Sources
Handles the specific structure and content of:
- AMA CPT: https://www.ama-assn.org/practice-management/cpt
- CMS ICD-10: https://www.cms.gov/medicare/coding-billing/icd-10-codes
- CMS HCPCS: https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import time
import random

logger = logging.getLogger(__name__)

@dataclass
class ScrapedCode:
    """Represents a scraped medical code"""
    code: str
    description: str
    category: Optional[str] = None
    section: Optional[str] = None
    subsection: Optional[str] = None
    chapter: Optional[str] = None
    block: Optional[str] = None
    level: Optional[str] = None
    coverage_status: Optional[str] = None
    is_billable: str = "Y"
    is_active: str = "Y"
    effective_date: Optional[datetime] = None
    source: str = ""
    additional_data: Dict[str, Any] = None

class AMACPTScraper:
    """Specialized scraper for AMA CPT codes"""
    
    def __init__(self):
        self.base_url = "https://www.ama-assn.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def scrape_cpt_codes(self) -> List[ScrapedCode]:
        """Scrape CPT codes from AMA website"""
        logger.info("Scraping CPT codes from AMA website...")
        
        try:
            # Main CPT page
            response = self.session.get(f"{self.base_url}/practice-management/cpt")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            cpt_codes = []
            
            # Look for CPT code sections
            # AMA typically organizes CPT codes in sections
            sections = soup.find_all(['div', 'section'], class_=re.compile(r'cpt|code|section', re.I))
            
            for section in sections:
                # Look for code patterns (5-digit numbers)
                code_elements = section.find_all(['span', 'div', 'td'], 
                                               string=re.compile(r'^\d{5}$'))
                
                for code_elem in code_elements:
                    code = code_elem.get_text().strip()
                    
                    # Find description (usually in nearby elements)
                    description = self._find_description(code_elem)
                    
                    # Determine category and section
                    category, section_name = self._determine_category_section(code_elem)
                    
                    if code and description:
                        cpt_codes.append(ScrapedCode(
                            code=code,
                            description=description,
                            category=category,
                            section=section_name,
                            source="AMA CPT"
                        ))
            
            # Also try to find CPT codes in tables
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        code_cell = cells[0]
                        desc_cell = cells[1] if len(cells) > 1 else None
                        
                        code_text = code_cell.get_text().strip()
                        if re.match(r'^\d{5}$', code_text):
                            description = desc_cell.get_text().strip() if desc_cell else ""
                            
                            if description:
                                cpt_codes.append(ScrapedCode(
                                    code=code_text,
                                    description=description,
                                    category="Category I",
                                    source="AMA CPT"
                                ))
            
            logger.info(f"Scraped {len(cpt_codes)} CPT codes from AMA")
            return cpt_codes
            
        except Exception as e:
            logger.error(f"Error scraping AMA CPT codes: {e}")
            return []
    
    def _find_description(self, code_element) -> str:
        """Find description for a CPT code"""
        # Look in parent element
        parent = code_element.parent
        if parent:
            # Find text elements that might contain description
            text_elements = parent.find_all(['span', 'div', 'p'], 
                                          string=lambda text: text and len(text) > 20)
            for elem in text_elements:
                text = elem.get_text().strip()
                if text and not re.match(r'^\d{5}$', text):
                    return text
        
        # Look in next sibling
        next_sibling = code_element.find_next_sibling()
        if next_sibling:
            return next_sibling.get_text().strip()
        
        return ""
    
    def _determine_category_section(self, code_element) -> tuple:
        """Determine category and section for a CPT code"""
        # Look for category indicators in parent elements
        parent = code_element.parent
        while parent:
            parent_text = parent.get_text().lower()
            
            # Check for category indicators
            if 'category i' in parent_text:
                category = "Category I"
            elif 'category ii' in parent_text:
                category = "Category II"
            elif 'category iii' in parent_text:
                category = "Category III"
            else:
                category = "Category I"  # Default
            
            # Check for section indicators
            if 'evaluation and management' in parent_text:
                section = "Evaluation and Management"
            elif 'surgery' in parent_text:
                section = "Surgery"
            elif 'radiology' in parent_text:
                section = "Radiology"
            elif 'pathology' in parent_text:
                section = "Pathology and Laboratory"
            elif 'medicine' in parent_text:
                section = "Medicine"
            else:
                section = ""
            
            if category and section:
                break
            
            parent = parent.parent
        
        return category, section

class CMSICD10Scraper:
    """Specialized scraper for CMS ICD-10 codes"""
    
    def __init__(self):
        self.base_url = "https://www.cms.gov"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def scrape_icd10_codes(self) -> List[ScrapedCode]:
        """Scrape ICD-10 codes from CMS website"""
        logger.info("Scraping ICD-10 codes from CMS website...")
        
        try:
            # Main ICD-10 page
            response = self.session.get(f"{self.base_url}/medicare/coding-billing/icd-10-codes")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            icd10_codes = []
            
            # Look for ICD-10 code patterns (letters followed by numbers)
            code_elements = soup.find_all(['span', 'div', 'td'], 
                                        string=re.compile(r'^[A-Z]\d{2}(\.\d{1,2})?$'))
            
            for code_elem in code_elements:
                code = code_elem.get_text().strip()
                description = self._find_icd10_description(code_elem)
                chapter = self._find_icd10_chapter(code_elem)
                
                if code and description:
                    icd10_codes.append(ScrapedCode(
                        code=code,
                        description=description,
                        chapter=chapter,
                        code_type="Diagnosis",
                        source="CMS ICD-10"
                    ))
            
            # Also look for codes in tables
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        code_cell = cells[0]
                        desc_cell = cells[1] if len(cells) > 1 else None
                        
                        code_text = code_cell.get_text().strip()
                        if re.match(r'^[A-Z]\d{2}(\.\d{1,2})?$', code_text):
                            description = desc_cell.get_text().strip() if desc_cell else ""
                            
                            if description:
                                icd10_codes.append(ScrapedCode(
                                    code=code_text,
                                    description=description,
                                    code_type="Diagnosis",
                                    source="CMS ICD-10"
                                ))
            
            logger.info(f"Scraped {len(icd10_codes)} ICD-10 codes from CMS")
            return icd10_codes
            
        except Exception as e:
            logger.error(f"Error scraping CMS ICD-10 codes: {e}")
            return []
    
    def _find_icd10_description(self, code_element) -> str:
        """Find description for an ICD-10 code"""
        # Similar logic to CPT but adapted for ICD-10 structure
        parent = code_element.parent
        if parent:
            text_elements = parent.find_all(['span', 'div', 'p'], 
                                          string=lambda text: text and len(text) > 10)
            for elem in text_elements:
                text = elem.get_text().strip()
                if text and not re.match(r'^[A-Z]\d{2}(\.\d{1,2})?$', text):
                    return text
        
        next_sibling = code_element.find_next_sibling()
        if next_sibling:
            return next_sibling.get_text().strip()
        
        return ""
    
    def _find_icd10_chapter(self, code_element) -> str:
        """Find chapter for an ICD-10 code"""
        # Look for chapter information in parent elements
        parent = code_element.parent
        while parent:
            parent_text = parent.get_text().lower()
            
            # Common ICD-10 chapters
            chapters = [
                "certain infectious and parasitic diseases",
                "neoplasms",
                "diseases of the blood and blood-forming organs",
                "endocrine, nutritional and metabolic diseases",
                "mental, behavioral and neurodevelopmental disorders",
                "diseases of the nervous system",
                "diseases of the eye and adnexa",
                "diseases of the ear and mastoid process",
                "diseases of the circulatory system",
                "diseases of the respiratory system",
                "diseases of the digestive system",
                "diseases of the skin and subcutaneous tissue",
                "diseases of the musculoskeletal system",
                "diseases of the genitourinary system",
                "pregnancy, childbirth and the puerperium",
                "certain conditions originating in the perinatal period",
                "congenital malformations, deformations and chromosomal abnormalities",
                "symptoms, signs and abnormal clinical and laboratory findings",
                "injury, poisoning and certain other consequences of external causes",
                "external causes of morbidity",
                "factors influencing health status and contact with health services"
            ]
            
            for chapter in chapters:
                if chapter in parent_text:
                    return chapter.title()
            
            parent = parent.parent
        
        return ""

class CMSHCPCSScraper:
    """Specialized scraper for CMS HCPCS codes"""
    
    def __init__(self):
        self.base_url = "https://www.cms.gov"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def scrape_hcpcs_codes(self) -> List[ScrapedCode]:
        """Scrape HCPCS codes from CMS website"""
        logger.info("Scraping HCPCS codes from CMS website...")
        
        try:
            # Main HCPCS page
            response = self.session.get(f"{self.base_url}/medicare/coding-billing/healthcare-common-procedure-system")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            hcpcs_codes = []
            
            # Look for HCPCS code patterns (letter followed by 4 digits)
            code_elements = soup.find_all(['span', 'div', 'td'], 
                                        string=re.compile(r'^[A-Z]\d{4}$'))
            
            for code_elem in code_elements:
                code = code_elem.get_text().strip()
                description = self._find_hcpcs_description(code_elem)
                category = self._find_hcpcs_category(code_elem)
                
                if code and description:
                    hcpcs_codes.append(ScrapedCode(
                        code=code,
                        description=description,
                        category=category,
                        level="Level II",
                        source="CMS HCPCS"
                    ))
            
            # Also look for codes in tables
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        code_cell = cells[0]
                        desc_cell = cells[1] if len(cells) > 1 else None
                        
                        code_text = code_cell.get_text().strip()
                        if re.match(r'^[A-Z]\d{4}$', code_text):
                            description = desc_cell.get_text().strip() if desc_cell else ""
                            
                            if description:
                                hcpcs_codes.append(ScrapedCode(
                                    code=code_text,
                                    description=description,
                                    level="Level II",
                                    source="CMS HCPCS"
                                ))
            
            logger.info(f"Scraped {len(hcpcs_codes)} HCPCS codes from CMS")
            return hcpcs_codes
            
        except Exception as e:
            logger.error(f"Error scraping CMS HCPCS codes: {e}")
            return []
    
    def _find_hcpcs_description(self, code_element) -> str:
        """Find description for an HCPCS code"""
        # Similar logic to other scrapers
        parent = code_element.parent
        if parent:
            text_elements = parent.find_all(['span', 'div', 'p'], 
                                          string=lambda text: text and len(text) > 10)
            for elem in text_elements:
                text = elem.get_text().strip()
                if text and not re.match(r'^[A-Z]\d{4}$', text):
                    return text
        
        next_sibling = code_element.find_next_sibling()
        if next_sibling:
            return next_sibling.get_text().strip()
        
        return ""
    
    def _find_hcpcs_category(self, code_element) -> str:
        """Find category for an HCPCS code"""
        # Look for category information in parent elements
        parent = code_element.parent
        while parent:
            parent_text = parent.get_text().lower()
            
            # Common HCPCS categories
            categories = [
                "durable medical equipment",
                "prosthetics and orthotics",
                "ambulance services",
                "drugs administered other than oral method",
                "medical and surgical supplies",
                "temporary procedures",
                "vision services",
                "hearing services"
            ]
            
            for category in categories:
                if category in parent_text:
                    return category.title()
            
            parent = parent.parent
        
        return ""

class OfficialDataScraper:
    """Main scraper that coordinates all official data sources"""
    
    def __init__(self):
        self.cpt_scraper = AMACPTScraper()
        self.icd10_scraper = CMSICD10Scraper()
        self.hcpcs_scraper = CMSHCPCSScraper()
    
    def scrape_all_official_data(self) -> Dict[str, List[ScrapedCode]]:
        """Scrape data from all official sources"""
        logger.info("Starting comprehensive scraping of official medical coding sources...")
        
        results = {
            'cpt_codes': [],
            'icd10_codes': [],
            'hcpcs_codes': []
        }
        
        try:
            # Scrape CPT codes from AMA
            logger.info("Scraping CPT codes from AMA...")
            results['cpt_codes'] = self.cpt_scraper.scrape_cpt_codes()
            
            # Add delay to be respectful to servers
            time.sleep(random.uniform(1, 3))
            
            # Scrape ICD-10 codes from CMS
            logger.info("Scraping ICD-10 codes from CMS...")
            results['icd10_codes'] = self.icd10_scraper.scrape_icd10_codes()
            
            # Add delay to be respectful to servers
            time.sleep(random.uniform(1, 3))
            
            # Scrape HCPCS codes from CMS
            logger.info("Scraping HCPCS codes from CMS...")
            results['hcpcs_codes'] = self.hcpcs_scraper.scrape_hcpcs_codes()
            
            # Summary
            total_codes = (len(results['cpt_codes']) + 
                          len(results['icd10_codes']) + 
                          len(results['hcpcs_codes']))
            
            logger.info(f"Scraping completed successfully!")
            logger.info(f"Total codes scraped: {total_codes}")
            logger.info(f"  - CPT codes: {len(results['cpt_codes'])}")
            logger.info(f"  - ICD-10 codes: {len(results['icd10_codes'])}")
            logger.info(f"  - HCPCS codes: {len(results['hcpcs_codes'])}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error during comprehensive scraping: {e}")
            return results
    
    def save_scraped_data(self, data: Dict[str, List[ScrapedCode]], filename: str = None):
        """Save scraped data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_medical_codes_{timestamp}.json"
        
        try:
            # Convert to serializable format
            serializable_data = {}
            for key, codes in data.items():
                serializable_data[key] = []
                for code in codes:
                    serializable_data[key].append({
                        'code': code.code,
                        'description': code.description,
                        'category': code.category,
                        'section': code.section,
                        'subsection': code.subsection,
                        'chapter': code.chapter,
                        'block': code.block,
                        'level': code.level,
                        'coverage_status': code.coverage_status,
                        'is_billable': code.is_billable,
                        'is_active': code.is_active,
                        'source': code.source,
                        'additional_data': code.additional_data
                    })
            
            with open(filename, 'w') as f:
                json.dump(serializable_data, f, indent=2)
            
            logger.info(f"Scraped data saved to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving scraped data: {e}")
            return None

# Global instance
official_data_scraper = OfficialDataScraper() 