# File: app/services/ocr_service.py
import cv2
import numpy as np
import pytesseract
import fitz  # PyMuPDF
import logging
from PIL import Image
from typing import Dict, Optional, Tuple
import re
import io

from app.core.config import settings
from app.core.exceptions import OCRException
from app.schemas.insurance_card import InsuranceCardCreate

logger = logging.getLogger(__name__)


class OCRService:
    """Service for OCR processing of insurance cards."""
    
    def __init__(self):
        # Configure Tesseract path if specified
        if settings.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results."""
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Apply noise reduction
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Apply dilation to connect text components
            kernel = np.ones((1, 1), np.uint8)
            processed = cv2.dilate(thresh, kernel, iterations=1)
            
            return processed
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise OCRException(f"Failed to preprocess image: {str(e)}")
    
    def extract_text_from_image(self, image_data: bytes) -> Tuple[str, float]:
        """Extract text from image using OCR."""
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data))
            image_np = np.array(image)
            
            # Preprocess image
            processed_image = self.preprocess_image(image_np)
            
            # Configure OCR with confidence data
            config = '--psm 6 -c tessedit_create_tsv=1'
            
            # Extract text with confidence scores
            data = pytesseract.image_to_data(
                processed_image, 
                config=config, 
                output_type=pytesseract.Output.DICT
            )
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Extract text
            text = pytesseract.image_to_string(processed_image, config='--psm 6')
            
            logger.info(f"OCR completed with confidence: {avg_confidence:.2f}%")
            return text.strip(), avg_confidence
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            raise OCRException(f"Failed to extract text from image: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_data: bytes) -> Tuple[str, float]:
        """Extract text from PDF."""
        try:
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                text += page_text + "\n"
            
            doc.close()
            
            # For PDF text extraction, confidence is based on text length
            confidence = min(95.0, len(text.strip()) * 0.5) if text.strip() else 0
            
            logger.info(f"PDF text extraction completed with confidence: {confidence:.2f}%")
            return text.strip(), confidence
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise OCRException(f"Failed to extract text from PDF: {str(e)}")
    
    def parse_insurance_card_text(self, text: str) -> InsuranceCardCreate:
        """Parse extracted text to identify insurance card information."""
        try:
            logger.info("Parsing insurance card text")
            
            # Initialize card data
            card_data = {
                'raw_text': text,
                'patient_name': None,
                'member_id': None,
                'group_number': None,
                'plan_name': None,
                'insurance_company': None,
                'effective_date': None,
                'phone_number': None
            }
            
            # Define patterns for different fields
            patterns = {
                'member_id': [
                    r'Member\s*ID[:\s]*([A-Z0-9]+)',
                    r'ID[:\s]*([A-Z0-9]+)',
                    r'Member[:\s]*([A-Z0-9]+)',
                    r'Subscriber[:\s]*([A-Z0-9]+)'
                ],
                'group_number': [
                    r'Group[:\s]*([A-Z0-9-]+)',
                    r'Grp[:\s]*([A-Z0-9-]+)',
                    r'Group\s*#[:\s]*([A-Z0-9-]+)'
                ],
                'phone_number': [
                    r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',
                    r'1[-.\s]?(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',
                    r'Customer\s*Service[:\s]*(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})'
                ],
                'effective_date': [
                    r'Effective[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                    r'Eff[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                    r'Valid[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
                ]
            }
            
            # Extract information using patterns
            for field, field_patterns in patterns.items():
                for pattern in field_patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        card_data[field] = match.group(1).strip()
                        break
            
            # Extract patient name (usually first lines or after "Name:")
            name_patterns = [
                r'Name[:\s]*([A-Za-z\s,]+)',
                r'^([A-Z][a-z]+\s+[A-Z][a-z]+)',
                r'Member[:\s]*([A-Za-z\s,]+?)(?:\n|$)',
                r'Patient[:\s]*([A-Za-z\s,]+)'
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
                if match:
                    name = match.group(1).strip()
                    # Clean up name (remove common suffixes/prefixes)
                    name = re.sub(r'\b(Name|Member|Patient)[:\s]*', '', name, flags=re.IGNORECASE)
                    if len(name) > 2 and not name.isdigit():
                        card_data['patient_name'] = name
                        break
            
            # Extract insurance company
            insurance_companies = [
                'Aetna', 'Anthem', 'BCBS', 'Blue Cross', 'Blue Shield',
                'Cigna', 'Humana', 'UnitedHealth', 'UnitedHealthcare',
                'Kaiser', 'Medicaid', 'Medicare', 'Molina', 'WellCare',
                'Centene', 'Independence', 'Harvard Pilgrim'
            ]
            
            for company in insurance_companies:
                if company.lower() in text.lower():
                    card_data['insurance_company'] = company
                    break
            
            # Extract plan name (look for plan-related keywords)
            plan_patterns = [
                r'Plan[:\s]*([A-Za-z0-9\s]+?)(?:\n|$)',
                r'Coverage[:\s]*([A-Za-z0-9\s]+?)(?:\n|$)',
                r'Product[:\s]*([A-Za-z0-9\s]+?)(?:\n|$)'
            ]
            
            for pattern in plan_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    plan = match.group(1).strip()
                    if len(plan) > 3 and not plan.isdigit():
                        card_data['plan_name'] = plan
                        break
            
            # Ensure member_id is required
            if not card_data['member_id']:
                # Try to find any alphanumeric ID that looks like a member ID
                id_patterns = [
                    r'\b([A-Z]{2,3}\d{6,12})\b',
                    r'\b(\d{9,12})\b',
                    r'\b([A-Z0-9]{8,15})\b'
                ]
                
                for pattern in id_patterns:
                    matches = re.findall(pattern, text)
                    if matches:
                        card_data['member_id'] = matches[0]
                        break
            
            if not card_data['member_id']:
                raise ValueError("Could not extract member ID from insurance card")
            
            logger.info(f"Successfully parsed insurance card data: {card_data}")
            return InsuranceCardCreate(**card_data)
            
        except Exception as e:
            logger.error(f"Error parsing insurance card text: {str(e)}")
            raise OCRException(f"Failed to parse insurance card information: {str(e)}")

