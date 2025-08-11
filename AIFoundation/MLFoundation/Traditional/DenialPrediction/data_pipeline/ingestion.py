"""
Data Ingestion Pipeline
Handles ingestion of healthcare claims data from various sources
"""

import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
import csv
import os

from models.database import SessionLocal, Claim, Provider, Payer

logger = logging.getLogger(__name__)

class DataIngestionPipeline:
    """Data ingestion pipeline for healthcare claims"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def process_837_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Process 837 (claim submission) file"""
        claims = []
        
        try:
            # Simulated 837 processing - in reality, would use specialized EDI library
            # This is a simplified example
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line.startswith('CLM'):  # Claim segment
                        try:
                            claim_data = self._parse_claim_segment(line)
                            if claim_data:
                                claims.append(claim_data)
                        except Exception as e:
                            self.logger.warning(f"Error parsing claim at line {line_num}: {e}")
                            continue
            
            self.logger.info(f"Processed {len(claims)} claims from 837 file")
            return claims
            
        except FileNotFoundError:
            self.logger.error(f"837 file not found: {file_path}")
            return []
        except Exception as e:
            self.logger.error(f"Error processing 837 file: {e}")
            return []
    
    def process_835_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Process 835 (remittance advice) file"""
        payments = []
        
        try:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line.startswith('CLP'):  # Claim payment segment
                        try:
                            payment_data = self._parse_payment_segment(line)
                            if payment_data:
                                payments.append(payment_data)
                        except Exception as e:
                            self.logger.warning(f"Error parsing payment at line {line_num}: {e}")
                            continue
            
            self.logger.info(f"Processed {len(payments)} payments from 835 file")
            return payments
            
        except FileNotFoundError:
            self.logger.error(f"835 file not found: {file_path}")
            return []
        except Exception as e:
            self.logger.error(f"Error processing 835 file: {e}")
            return []
    
    def process_csv_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Process CSV file with claims data"""
        claims = []
        
        try:
            df = pd.read_csv(file_path)
            
            for _, row in df.iterrows():
                try:
                    claim_data = self._validate_claim_data(row.to_dict())
                    if claim_data:
                        claims.append(claim_data)
                except Exception as e:
                    self.logger.warning(f"Error processing row: {e}")
                    continue
            
            self.logger.info(f"Processed {len(claims)} claims from CSV file")
            return claims
            
        except Exception as e:
            self.logger.error(f"Error processing CSV file: {e}")
            return []
    
    def _parse_claim_segment(self, segment: str) -> Optional[Dict[str, Any]]:
        """Parse individual claim segment from 837"""
        try:
            # Simplified parsing - real implementation would be more complex
            parts = segment.split('*')
            
            if len(parts) < 4:
                return None
            
            claim_data = {
                'claim_id': parts[1] if len(parts) > 1 else '',
                'claim_amount': float(parts[2]) if len(parts) > 2 and parts[2] else 0.0,
                'provider_id': parts[3] if len(parts) > 3 else '',
                'service_date': datetime.now().strftime('%Y-%m-%d'),
                'submission_date': datetime.now().isoformat(),
                'patient_id': parts[4] if len(parts) > 4 else '',
                'payer_id': parts[5] if len(parts) > 5 else '',
                'patient_age': int(parts[6]) if len(parts) > 6 and parts[6].isdigit() else 45,
                'patient_gender': parts[7] if len(parts) > 7 else 'M',
                'cpt_codes': [parts[8]] if len(parts) > 8 else [],
                'icd_codes': [parts[9]] if len(parts) > 9 else [],
                'place_of_service': parts[10] if len(parts) > 10 else '11',
                'authorization_number': parts[11] if len(parts) > 11 else None,
                'modifiers': []
            }
            
            return claim_data
            
        except Exception as e:
            self.logger.warning(f"Error parsing claim segment: {e}")
            return None
    
    def _parse_payment_segment(self, segment: str) -> Optional[Dict[str, Any]]:
        """Parse payment segment from 835"""
        try:
            parts = segment.split('*')
            
            if len(parts) < 4:
                return None
            
            payment_data = {
                'claim_id': parts[1] if len(parts) > 1 else '',
                'payment_amount': float(parts[2]) if len(parts) > 2 and parts[2] else 0.0,
                'status_code': parts[3] if len(parts) > 3 else '',
                'payment_date': datetime.now().isoformat(),
                'denial_codes': [parts[4]] if len(parts) > 4 and parts[4] else [],
                'denial_reason': parts[5] if len(parts) > 5 else ''
            }
            
            return payment_data
            
        except Exception as e:
            self.logger.warning(f"Error parsing payment segment: {e}")
            return None
    
    def ingest_claims_data(self, claims_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Ingest claims data into database"""
        db = SessionLocal()
        ingested_count = 0
        error_count = 0
        
        try:
            for claim_data in claims_data:
                try:
                    # Validate and clean data
                    cleaned_claim = self._validate_claim_data(claim_data)
                    if cleaned_claim:
                        # Convert dates
                        if 'service_date' in cleaned_claim and isinstance(cleaned_claim['service_date'], str):
                            cleaned_claim['service_date'] = datetime.fromisoformat(cleaned_claim['service_date'])
                        
                        if 'submission_date' in cleaned_claim and isinstance(cleaned_claim['submission_date'], str):
                            cleaned_claim['submission_date'] = datetime.fromisoformat(cleaned_claim['submission_date'])
                        
                        # Create or update claim
                        existing_claim = db.query(Claim).filter(
                            Claim.claim_id == cleaned_claim['claim_id']
                        ).first()
                        
                        if existing_claim:
                            # Update existing claim
                            for key, value in cleaned_claim.items():
                                if hasattr(existing_claim, key):
                                    setattr(existing_claim, key, value)
                            existing_claim.updated_at = datetime.utcnow()
                        else:
                            # Create new claim
                            claim = Claim(**cleaned_claim)
                            db.add(claim)
                        
                        ingested_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    self.logger.error(f"Error ingesting claim {claim_data.get('claim_id', 'unknown')}: {e}")
                    error_count += 1
                    continue
            
            db.commit()
            self.logger.info(f"Ingested {ingested_count} claims, {error_count} errors")
            
            return {
                "ingested_count": ingested_count,
                "error_count": error_count,
                "total_processed": len(claims_data)
            }
            
        except Exception as e:
            db.rollback()
            self.logger.error(f"Error ingesting claims: {str(e)}")
            raise
        finally:
            db.close()
    
    def update_payment_data(self, payment_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Update claims with payment/denial information"""
        db = SessionLocal()
        updated_count = 0
        error_count = 0
        
        try:
            for payment in payment_data:
                try:
                    claim_id = payment.get('claim_id')
                    if not claim_id:
                        continue
                    
                    # Find corresponding claim
                    claim = db.query(Claim).filter(Claim.claim_id == claim_id).first()
                    if claim:
                        # Update payment information
                        if payment.get('payment_amount', 0) > 0:
                            claim.is_denied = False
                        else:
                            claim.is_denied = True
                            claim.denial_codes = payment.get('denial_codes', [])
                            claim.denial_reason = payment.get('denial_reason', '')
                        
                        claim.denial_date = datetime.fromisoformat(payment['payment_date']) if payment.get('payment_date') else datetime.utcnow()
                        claim.updated_at = datetime.utcnow()
                        
                        updated_count += 1
                    else:
                        self.logger.warning(f"Claim {claim_id} not found for payment update")
                        error_count += 1
                        
                except Exception as e:
                    self.logger.error(f"Error updating payment for claim {payment.get('claim_id', 'unknown')}: {e}")
                    error_count += 1
                    continue
            
            db.commit()
            self.logger.info(f"Updated {updated_count} claims with payment data, {error_count} errors")
            
            return {
                "updated_count": updated_count,
                "error_count": error_count,
                "total_processed": len(payment_data)
            }
            
        except Exception as e:
            db.rollback()
            self.logger.error(f"Error updating payment data: {str(e)}")
            raise
        finally:
            db.close()
    
    def _validate_claim_data(self, claim_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Validate and clean claim data"""
        required_fields = ['claim_id', 'provider_id', 'payer_id', 'claim_amount']
        
        # Check required fields
        for field in required_fields:
            if field not in claim_data or not claim_data[field]:
                self.logger.warning(f"Missing required field {field} in claim")
                return None
        
        # Data type validation and conversion
        try:
            # Convert claim amount
            if isinstance(claim_data['claim_amount'], str):
                claim_data['claim_amount'] = float(claim_data['claim_amount'].replace('$', '').replace(',', ''))
            else:
                claim_data['claim_amount'] = float(claim_data['claim_amount'])
            
            # Convert patient age
            if 'patient_age' in claim_data:
                if isinstance(claim_data['patient_age'], str):
                    claim_data['patient_age'] = int(claim_data['patient_age'])
                else:
                    claim_data['patient_age'] = int(claim_data['patient_age'])
            else:
                claim_data['patient_age'] = 45  # Default age
            
            # Ensure lists for codes
            if 'cpt_codes' in claim_data and not isinstance(claim_data['cpt_codes'], list):
                claim_data['cpt_codes'] = [claim_data['cpt_codes']] if claim_data['cpt_codes'] else []
            
            if 'icd_codes' in claim_data and not isinstance(claim_data['icd_codes'], list):
                claim_data['icd_codes'] = [claim_data['icd_codes']] if claim_data['icd_codes'] else []
            
            if 'modifiers' in claim_data and not isinstance(claim_data['modifiers'], list):
                claim_data['modifiers'] = [claim_data['modifiers']] if claim_data['modifiers'] else []
            
        except (ValueError, TypeError) as e:
            self.logger.warning(f"Invalid data types in claim: {e}")
            return None
        
        # Business rule validation
        if claim_data['claim_amount'] <= 0:
            self.logger.warning("Invalid claim amount")
            return None
        
        if claim_data['patient_age'] < 0 or claim_data['patient_age'] > 120:
            self.logger.warning("Invalid patient age")
            return None
        
        # Ensure patient gender is valid
        if 'patient_gender' in claim_data:
            gender = claim_data['patient_gender'].upper()
            if gender not in ['M', 'F']:
                claim_data['patient_gender'] = 'M'  # Default to male
        
        # Set default values for missing optional fields
        if 'place_of_service' not in claim_data:
            claim_data['place_of_service'] = '11'  # Office
        
        if 'submission_date' not in claim_data:
            claim_data['submission_date'] = datetime.utcnow().isoformat()
        
        return claim_data
    
    def generate_sample_data(self, num_claims: int = 1000) -> List[Dict[str, Any]]:
        """Generate sample claims data for testing"""
        import random
        
        providers = [f"PROV_{i:03d}" for i in range(1, 21)]
        payers = ["MEDICARE", "MEDICAID", "AETNA", "BCBS", "UNITEDHEALTH"]
        cpt_codes = ["99213", "99214", "99215", "90834", "90837", "90853", "90863"]
        icd_codes = ["F32.9", "F33.2", "Z00.00", "Z23", "E11.9", "I10", "M79.3"]
        
        claims = []
        
        for i in range(num_claims):
            claim_data = {
                'claim_id': f"CLM_{i+1:06d}",
                'provider_id': random.choice(providers),
                'payer_id': random.choice(payers),
                'patient_id': f"PAT_{random.randint(1000, 9999)}",
                'claim_amount': round(random.uniform(100, 5000), 2),
                'service_date': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
                'submission_date': datetime.now().isoformat(),
                'patient_age': random.randint(18, 85),
                'patient_gender': random.choice(['M', 'F']),
                'cpt_codes': random.sample(cpt_codes, random.randint(1, 3)),
                'icd_codes': random.sample(icd_codes, random.randint(1, 2)),
                'place_of_service': str(random.randint(11, 23)),
                'authorization_number': f"AUTH_{random.randint(1000, 9999)}" if random.random() > 0.3 else None,
                'modifiers': random.sample(['25', '59', '76', '77'], random.randint(0, 2)) if random.random() > 0.5 else []
            }
            
            claims.append(claim_data)
        
        return claims
    
    def export_claims_to_csv(self, output_path: str, filters: Optional[Dict[str, Any]] = None) -> bool:
        """Export claims data to CSV file"""
        db = SessionLocal()
        
        try:
            query = db.query(Claim)
            
            # Apply filters
            if filters:
                if 'start_date' in filters:
                    query = query.filter(Claim.submission_date >= filters['start_date'])
                if 'end_date' in filters:
                    query = query.filter(Claim.submission_date <= filters['end_date'])
                if 'provider_id' in filters:
                    query = query.filter(Claim.provider_id == filters['provider_id'])
                if 'payer_id' in filters:
                    query = query.filter(Claim.payer_id == filters['payer_id'])
            
            claims = query.all()
            
            # Convert to DataFrame
            data = []
            for claim in claims:
                data.append({
                    'claim_id': claim.claim_id,
                    'provider_id': claim.provider_id,
                    'payer_id': claim.payer_id,
                    'patient_id': claim.patient_id,
                    'claim_amount': claim.claim_amount,
                    'service_date': claim.service_date.isoformat() if claim.service_date else None,
                    'submission_date': claim.submission_date.isoformat() if claim.submission_date else None,
                    'patient_age': claim.patient_age,
                    'patient_gender': claim.patient_gender,
                    'cpt_codes': json.dumps(claim.cpt_codes) if claim.cpt_codes else None,
                    'icd_codes': json.dumps(claim.icd_codes) if claim.icd_codes else None,
                    'place_of_service': claim.place_of_service,
                    'authorization_number': claim.authorization_number,
                    'modifiers': json.dumps(claim.modifiers) if claim.modifiers else None,
                    'is_denied': claim.is_denied,
                    'denial_reason': claim.denial_reason,
                    'created_at': claim.created_at.isoformat() if claim.created_at else None
                })
            
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)
            
            self.logger.info(f"Exported {len(data)} claims to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting claims: {e}")
            return False
        finally:
            db.close()
    
    def get_ingestion_stats(self) -> Dict[str, Any]:
        """Get ingestion statistics"""
        db = SessionLocal()
        
        try:
            # Total claims
            total_claims = db.query(Claim).count()
            
            # Claims by date
            today = datetime.now().date()
            claims_today = db.query(Claim).filter(
                Claim.submission_date >= today
            ).count()
            
            claims_week = db.query(Claim).filter(
                Claim.submission_date >= today - timedelta(days=7)
            ).count()
            
            claims_month = db.query(Claim).filter(
                Claim.submission_date >= today - timedelta(days=30)
            ).count()
            
            # Denial rate
            denied_claims = db.query(Claim).filter(Claim.is_denied == True).count()
            denial_rate = (denied_claims / total_claims * 100) if total_claims > 0 else 0
            
            # Average claim amount
            avg_amount = db.query(text('AVG(claim_amount)')).scalar() or 0
            
            return {
                'total_claims': total_claims,
                'claims_today': claims_today,
                'claims_week': claims_week,
                'claims_month': claims_month,
                'denial_rate': round(denial_rate, 2),
                'avg_claim_amount': round(avg_amount, 2),
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting ingestion stats: {e}")
            return {}
        finally:
            db.close() 