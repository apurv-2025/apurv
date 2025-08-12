#!/usr/bin/env python3
"""
Enhanced Scrapers with Database Integration
Provides options to save scraped data directly to database or files
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging
from sqlalchemy.orm import Session

from .specialized_scrapers import OfficialDataScraper, ScrapedCode
from ..database import SessionLocal
from ..models import CPTCode, ICD10Code, HCPCSCode

logger = logging.getLogger(__name__)

class EnhancedDataScraper:
    """Enhanced scraper with database integration options"""
    
    def __init__(self):
        self.scraper = OfficialDataScraper()
    
    async def scrape_and_save_to_database(self, save_to_db: bool = True, save_to_file: bool = False) -> Dict[str, Any]:
        """
        Scrape data and optionally save to database and/or file
        
        Args:
            save_to_db: Whether to save scraped data to database
            save_to_file: Whether to save scraped data to JSON file
        """
        logger.info(f"Starting enhanced scraping - DB: {save_to_db}, File: {save_to_file}")
        
        # Scrape data from all sources
        scraped_data = self.scraper.scrape_all_official_data()
        
        results = {
            'scraped_data': scraped_data,
            'database_saved': False,
            'file_saved': False,
            'filename': None,
            'db_counts': {'cpt': 0, 'icd10': 0, 'hcpcs': 0}
        }
        
        # Save to database if requested
        if save_to_db:
            db_results = await self._save_to_database(scraped_data)
            results['database_saved'] = True
            results['db_counts'] = db_results
        
        # Save to file if requested
        if save_to_file:
            filename = self.scraper.save_scraped_data(scraped_data)
            results['file_saved'] = True
            results['filename'] = filename
        
        return results
    
    async def _save_to_database(self, scraped_data: Dict[str, List[ScrapedCode]]) -> Dict[str, int]:
        """Save scraped data to database"""
        db = SessionLocal()
        try:
            counts = {'cpt': 0, 'icd10': 0, 'hcpcs': 0}
            
            # Save CPT codes
            if scraped_data.get('cpt_codes'):
                counts['cpt'] = await self._save_cpt_codes_to_db(scraped_data['cpt_codes'], db)
            
            # Save ICD-10 codes
            if scraped_data.get('icd10_codes'):
                counts['icd10'] = await self._save_icd10_codes_to_db(scraped_data['icd10_codes'], db)
            
            # Save HCPCS codes
            if scraped_data.get('hcpcs_codes'):
                counts['hcpcs'] = await self._save_hcpcs_codes_to_db(scraped_data['hcpcs_codes'], db)
            
            db.commit()
            logger.info(f"Database save completed: CPT={counts['cpt']}, ICD10={counts['icd10']}, HCPCS={counts['hcpcs']}")
            return counts
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving to database: {e}")
            return {'cpt': 0, 'icd10': 0, 'hcpcs': 0}
        finally:
            db.close()
    
    async def _save_cpt_codes_to_db(self, cpt_codes: List[ScrapedCode], db: Session) -> int:
        """Save CPT codes to database"""
        saved_count = 0
        for scraped_code in cpt_codes:
            try:
                existing = db.query(CPTCode).filter(CPTCode.code == scraped_code.code).first()
                
                if existing:
                    # Update existing code
                    existing.description = scraped_code.description
                    existing.category = scraped_code.category or existing.category
                    existing.section = scraped_code.section or existing.section
                    existing.subsection = scraped_code.subsection or existing.subsection
                    if scraped_code.effective_date:
                        existing.effective_date = scraped_code.effective_date
                else:
                    # Create new code
                    new_code = CPTCode(
                        code=scraped_code.code,
                        description=scraped_code.description,
                        category=scraped_code.category or "Category I",
                        section=scraped_code.section or "",
                        subsection=scraped_code.subsection or "",
                        effective_date=scraped_code.effective_date,
                        is_active=scraped_code.is_active
                    )
                    db.add(new_code)
                
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Error saving CPT code {scraped_code.code}: {e}")
                continue
        
        return saved_count
    
    async def _save_icd10_codes_to_db(self, icd10_codes: List[ScrapedCode], db: Session) -> int:
        """Save ICD-10 codes to database"""
        saved_count = 0
        for scraped_code in icd10_codes:
            try:
                existing = db.query(ICD10Code).filter(ICD10Code.code == scraped_code.code).first()
                
                if existing:
                    # Update existing code
                    existing.description = scraped_code.description
                    existing.code_type = scraped_code.code_type or existing.code_type
                    existing.chapter = scraped_code.chapter or existing.chapter
                    existing.block = scraped_code.block or existing.block
                    existing.is_billable = scraped_code.is_billable or existing.is_billable
                else:
                    # Create new code
                    new_code = ICD10Code(
                        code=scraped_code.code,
                        description=scraped_code.description,
                        code_type=scraped_code.code_type or "Diagnosis",
                        chapter=scraped_code.chapter or "",
                        block=scraped_code.block or "",
                        is_billable=scraped_code.is_billable or "Y",
                        is_active=scraped_code.is_active
                    )
                    db.add(new_code)
                
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Error saving ICD-10 code {scraped_code.code}: {e}")
                continue
        
        return saved_count
    
    async def _save_hcpcs_codes_to_db(self, hcpcs_codes: List[ScrapedCode], db: Session) -> int:
        """Save HCPCS codes to database"""
        saved_count = 0
        for scraped_code in hcpcs_codes:
            try:
                existing = db.query(HCPCSCode).filter(HCPCSCode.code == scraped_code.code).first()
                
                if existing:
                    # Update existing code
                    existing.description = scraped_code.description
                    existing.level = scraped_code.level or existing.level
                    existing.category = scraped_code.category or existing.category
                    existing.coverage_status = scraped_code.coverage_status or existing.coverage_status
                else:
                    # Create new code
                    new_code = HCPCSCode(
                        code=scraped_code.code,
                        description=scraped_code.description,
                        level=scraped_code.level or "Level II",
                        category=scraped_code.category or "",
                        coverage_status=scraped_code.coverage_status or "",
                        is_active=scraped_code.is_active
                    )
                    db.add(new_code)
                
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Error saving HCPCS code {scraped_code.code}: {e}")
                continue
        
        return saved_count
    
    async def scrape_cpt_to_database(self) -> Dict[str, Any]:
        """Scrape CPT codes and save directly to database"""
        logger.info("Scraping CPT codes and saving to database...")
        
        # Scrape CPT codes
        cpt_codes = self.scraper.cpt_scraper.scrape_cpt_codes()
        
        # Save to database
        db = SessionLocal()
        try:
            saved_count = await self._save_cpt_codes_to_db(cpt_codes, db)
            db.commit()
            
            return {
                'success': True,
                'message': f"Successfully scraped and saved {saved_count} CPT codes to database",
                'scraped_count': len(cpt_codes),
                'saved_count': saved_count,
                'source': 'AMA CPT'
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving CPT codes to database: {e}")
            return {
                'success': False,
                'message': f"Error saving CPT codes to database: {str(e)}",
                'scraped_count': len(cpt_codes),
                'saved_count': 0
            }
        finally:
            db.close()
    
    async def scrape_icd10_to_database(self) -> Dict[str, Any]:
        """Scrape ICD-10 codes and save directly to database"""
        logger.info("Scraping ICD-10 codes and saving to database...")
        
        # Scrape ICD-10 codes
        icd10_codes = self.scraper.icd10_scraper.scrape_icd10_codes()
        
        # Save to database
        db = SessionLocal()
        try:
            saved_count = await self._save_icd10_codes_to_db(icd10_codes, db)
            db.commit()
            
            return {
                'success': True,
                'message': f"Successfully scraped and saved {saved_count} ICD-10 codes to database",
                'scraped_count': len(icd10_codes),
                'saved_count': saved_count,
                'source': 'CMS ICD-10'
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving ICD-10 codes to database: {e}")
            return {
                'success': False,
                'message': f"Error saving ICD-10 codes to database: {str(e)}",
                'scraped_count': len(icd10_codes),
                'saved_count': 0
            }
        finally:
            db.close()
    
    async def scrape_hcpcs_to_database(self) -> Dict[str, Any]:
        """Scrape HCPCS codes and save directly to database"""
        logger.info("Scraping HCPCS codes and saving to database...")
        
        # Scrape HCPCS codes
        hcpcs_codes = self.scraper.hcpcs_scraper.scrape_hcpcs_codes()
        
        # Save to database
        db = SessionLocal()
        try:
            saved_count = await self._save_hcpcs_codes_to_db(hcpcs_codes, db)
            db.commit()
            
            return {
                'success': True,
                'message': f"Successfully scraped and saved {saved_count} HCPCS codes to database",
                'scraped_count': len(hcpcs_codes),
                'saved_count': saved_count,
                'source': 'CMS HCPCS'
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving HCPCS codes to database: {e}")
            return {
                'success': False,
                'message': f"Error saving HCPCS codes to database: {str(e)}",
                'scraped_count': len(hcpcs_codes),
                'saved_count': 0
            }
        finally:
            db.close()

# Global instance
enhanced_scraper = EnhancedDataScraper() 