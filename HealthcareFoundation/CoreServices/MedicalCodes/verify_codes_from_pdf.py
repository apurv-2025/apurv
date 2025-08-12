#!/usr/bin/env python3
"""
Medical Codes Verification Script
Extracts CPT and HCPCS codes from PDF and compares with current database
"""

import re
import json
import requests
from typing import Dict, List, Set, Tuple
import sys
from pathlib import Path

class MedicalCodesVerifier:
    def __init__(self, pdf_path: str, api_base_url: str = "http://localhost:8003"):
        self.pdf_path = pdf_path
        self.api_base_url = api_base_url
        self.extracted_codes = {
            'cpt': set(),
            'hcpcs': set(),
            'icd10': set()
        }
        
    def extract_codes_from_pdf(self) -> Dict[str, Set[str]]:
        """Extract codes from PDF using text extraction"""
        print("📄 Extracting codes from PDF...")
        
        try:
            import PyPDF2
            import pdfplumber
        except ImportError:
            print("❌ Required libraries not found. Installing...")
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", "PyPDF2", "pdfplumber"])
            import PyPDF2
            import pdfplumber
        
        extracted_text = ""
        
        # Try pdfplumber first (better for structured PDFs)
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
            print("✅ Successfully extracted text using pdfplumber")
        except Exception as e:
            print(f"⚠️ pdfplumber failed: {e}")
            # Fallback to PyPDF2
            try:
                with open(self.pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        if text:
                            extracted_text += text + "\n"
                print("✅ Successfully extracted text using PyPDF2")
            except Exception as e2:
                print(f"❌ Both PDF extraction methods failed: {e2}")
                return self.extracted_codes
        
        # Extract CPT codes (5-digit numeric codes)
        cpt_pattern = r'\b(\d{5})\b'
        cpt_codes = re.findall(cpt_pattern, extracted_text)
        self.extracted_codes['cpt'] = set(cpt_codes)
        
        # Extract HCPCS codes (1 letter + 4 digits)
        hcpcs_pattern = r'\b([A-Z]\d{4})\b'
        hcpcs_codes = re.findall(hcpcs_pattern, extracted_text)
        self.extracted_codes['hcpcs'] = set(hcpcs_codes)
        
        # Extract ICD-10 codes (letter + 2 digits + optional letter + optional digit)
        icd10_pattern = r'\b([A-Z]\d{2}(?:[A-Z]\d?)?)\b'
        icd10_codes = re.findall(icd10_pattern, extracted_text)
        self.extracted_codes['icd10'] = set(icd10_codes)
        
        print(f"📊 Extracted codes from PDF:")
        print(f"   CPT: {len(self.extracted_codes['cpt'])} codes")
        print(f"   HCPCS: {len(self.extracted_codes['hcpcs'])} codes")
        print(f"   ICD-10: {len(self.extracted_codes['icd10'])} codes")
        
        return self.extracted_codes
    
    def get_current_database_codes(self) -> Dict[str, Set[str]]:
        """Get current codes from database via API"""
        print("🗄️ Fetching current codes from database...")
        
        current_codes = {
            'cpt': set(),
            'hcpcs': set(),
            'icd10': set()
        }
        
        try:
            # Get CPT codes from comprehensive search
            response = requests.get(f"{self.api_base_url}/api/comprehensive/search?query=&code_types=cpt")
            if response.status_code == 200:
                cpt_data = response.json()
                if 'results' in cpt_data and 'cpt_codes' in cpt_data['results']:
                    current_codes['cpt'] = {item['code'] for item in cpt_data['results']['cpt_codes']}
            
            # Get HCPCS codes from comprehensive search
            response = requests.get(f"{self.api_base_url}/api/comprehensive/search?query=&code_types=hcpcs")
            if response.status_code == 200:
                hcpcs_data = response.json()
                if 'results' in hcpcs_data and 'hcpcs_codes' in hcpcs_data['results']:
                    current_codes['hcpcs'] = {item['code'] for item in hcpcs_data['results']['hcpcs_codes']}
            
            # Get ICD-10 codes from comprehensive search
            response = requests.get(f"{self.api_base_url}/api/comprehensive/search?query=&code_types=icd10")
            if response.status_code == 200:
                icd10_data = response.json()
                if 'results' in icd10_data and 'icd10_codes' in icd10_data['results']:
                    current_codes['icd10'] = {item['code'] for item in icd10_data['results']['icd10_codes']}
                
        except Exception as e:
            print(f"❌ Error fetching from database: {e}")
            return current_codes
        
        print(f"📊 Current database codes:")
        print(f"   CPT: {len(current_codes['cpt'])} codes")
        print(f"   HCPCS: {len(current_codes['hcpcs'])} codes")
        print(f"   ICD-10: {len(current_codes['icd10'])} codes")
        
        return current_codes
    
    def compare_codes(self, pdf_codes: Dict[str, Set[str]], db_codes: Dict[str, Set[str]]) -> Dict:
        """Compare PDF codes with database codes"""
        print("🔍 Comparing codes...")
        
        comparison = {
            'cpt': {
                'pdf_total': len(pdf_codes['cpt']),
                'db_total': len(db_codes['cpt']),
                'matching': len(pdf_codes['cpt'] & db_codes['cpt']),
                'missing': pdf_codes['cpt'] - db_codes['cpt'],
                'extra': db_codes['cpt'] - pdf_codes['cpt'],
                'coverage': 0
            },
            'hcpcs': {
                'pdf_total': len(pdf_codes['hcpcs']),
                'db_total': len(db_codes['hcpcs']),
                'matching': len(pdf_codes['hcpcs'] & db_codes['hcpcs']),
                'missing': pdf_codes['hcpcs'] - db_codes['hcpcs'],
                'extra': db_codes['hcpcs'] - pdf_codes['hcpcs'],
                'coverage': 0
            },
            'icd10': {
                'pdf_total': len(pdf_codes['icd10']),
                'db_total': len(db_codes['icd10']),
                'matching': len(pdf_codes['icd10'] & db_codes['icd10']),
                'missing': pdf_codes['icd10'] - db_codes['icd10'],
                'extra': db_codes['icd10'] - pdf_codes['icd10'],
                'coverage': 0
            }
        }
        
        # Calculate coverage percentages
        for code_type in comparison:
            if comparison[code_type]['pdf_total'] > 0:
                comparison[code_type]['coverage'] = (
                    comparison[code_type]['matching'] / comparison[code_type]['pdf_total']
                ) * 100
        
        return comparison
    
    def generate_report(self, comparison: Dict) -> str:
        """Generate a comprehensive verification report"""
        report = []
        report.append("=" * 80)
        report.append("🏥 MEDICAL CODES VERIFICATION REPORT")
        report.append("=" * 80)
        report.append(f"📄 Source: {self.pdf_path}")
        report.append(f"📅 Verification Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        for code_type in ['cpt', 'hcpcs', 'icd10']:
            data = comparison[code_type]
            report.append(f"📋 {code_type.upper()} CODES ANALYSIS")
            report.append("-" * 40)
            report.append(f"📄 PDF Total: {data['pdf_total']:,}")
            report.append(f"🗄️ Database Total: {data['db_total']:,}")
            report.append(f"✅ Matching: {data['matching']:,}")
            report.append(f"❌ Missing: {len(data['missing']):,}")
            report.append(f"➕ Extra: {len(data['extra']):,}")
            report.append(f"📊 Coverage: {data['coverage']:.1f}%")
            report.append("")
            
            if data['missing']:
                report.append(f"❌ MISSING {code_type.upper()} CODES:")
                missing_list = sorted(list(data['missing']))[:20]  # Show first 20
                for code in missing_list:
                    report.append(f"   - {code}")
                if len(data['missing']) > 20:
                    report.append(f"   ... and {len(data['missing']) - 20} more")
                report.append("")
            
            if data['extra']:
                report.append(f"➕ EXTRA {code_type.upper()} CODES (not in PDF):")
                extra_list = sorted(list(data['extra']))[:10]  # Show first 10
                for code in extra_list:
                    report.append(f"   - {code}")
                if len(data['extra']) > 10:
                    report.append(f"   ... and {len(data['extra']) - 10} more")
                report.append("")
        
        # Summary
        report.append("📊 SUMMARY")
        report.append("-" * 40)
        total_pdf = sum(comparison[ct]['pdf_total'] for ct in comparison)
        total_matching = sum(comparison[ct]['matching'] for ct in comparison)
        overall_coverage = (total_matching / total_pdf * 100) if total_pdf > 0 else 0
        
        report.append(f"📄 Total PDF Codes: {total_pdf:,}")
        report.append(f"✅ Total Matching: {total_matching:,}")
        report.append(f"📊 Overall Coverage: {overall_coverage:.1f}%")
        report.append("")
        
        if overall_coverage < 90:
            report.append("⚠️ RECOMMENDATION: Consider updating database with missing codes")
        else:
            report.append("✅ EXCELLENT: Database has good coverage of current codes")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_detailed_results(self, comparison: Dict, filename: str = "code_verification_results.json"):
        """Save detailed results to JSON file"""
        # Convert sets to lists for JSON serialization
        serializable_comparison = {}
        for code_type, data in comparison.items():
            serializable_comparison[code_type] = {
                'pdf_total': data['pdf_total'],
                'db_total': data['db_total'],
                'matching': data['matching'],
                'missing': list(data['missing']),
                'extra': list(data['extra']),
                'coverage': data['coverage']
            }
        
        results = {
            'verification_date': __import__('datetime').datetime.now().isoformat(),
            'pdf_source': self.pdf_path,
            'comparison': serializable_comparison,
            'extracted_codes': {
                'cpt': list(self.extracted_codes['cpt']),
                'hcpcs': list(self.extracted_codes['hcpcs']),
                'icd10': list(self.extracted_codes['icd10'])
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Detailed results saved to: {filename}")
    
    def run_verification(self):
        """Run the complete verification process"""
        print("🚀 Starting Medical Codes Verification...")
        print(f"📄 PDF File: {self.pdf_path}")
        print(f"🌐 API Base URL: {self.api_base_url}")
        print("")
        
        # Extract codes from PDF
        pdf_codes = self.extract_codes_from_pdf()
        
        # Get current database codes
        db_codes = self.get_current_database_codes()
        
        # Compare codes
        comparison = self.compare_codes(pdf_codes, db_codes)
        
        # Generate and display report
        report = self.generate_report(comparison)
        print(report)
        
        # Save detailed results
        self.save_detailed_results(comparison)
        
        return comparison

def main():
    """Main function"""
    pdf_path = "advancedmd-eguide-CPT-HCPCS-2025.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    verifier = MedicalCodesVerifier(pdf_path)
    verifier.run_verification()

if __name__ == "__main__":
    main() 