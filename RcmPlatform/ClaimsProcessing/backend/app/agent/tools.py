# =============================================================================
# FILE: backend/app/agent/tools.py
# =============================================================================
from langchain.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from decimal import Decimal
import json
from datetime import datetime

from ..database.connection import SessionLocal
from ..database.models import Claim, ServiceLine, Payer, ClaimStatus
from ..services.claim_processor import ClaimProcessor
from ..services.validators import ClaimValidator

class ClaimsTools:
    """Collection of tools for the claims processing agent"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def get_tools(self) -> List[BaseTool]:
        return [
            GetClaimTool(db=self.db),
            ValidateClaimTool(db=self.db),
            ProcessEDIFileTool(db=self.db),
            AnalyzeRejectionTool(db=self.db),
            GetPayerInfoTool(db=self.db),
            GenerateReportTool(db=self.db),
            SearchClaimsTool(db=self.db),
            UpdateClaimStatusTool(db=self.db),
            GetDashboardStatsTool(db=self.db),
            CalculateFinancialMetricsTool(db=self.db)
        ]

class GetClaimTool(BaseTool):
    name = "get_claim"
    description = "Retrieve detailed information about a specific claim by ID"
    db: Session
    
    def _run(
        self, 
        claim_id: int,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            claim = self.db.query(Claim).filter(Claim.id == claim_id).first()
            if not claim:
                return f"Claim with ID {claim_id} not found"
            
            claim_data = {
                "id": claim.id,
                "claim_number": claim.claim_number,
                "status": claim.status.value,
                "claim_type": claim.claim_type.value,
                "patient_name": f"{claim.patient_first_name} {claim.patient_last_name}",
                "provider": claim.provider_name,
                "provider_npi": claim.provider_npi,
                "total_charge": float(claim.total_charge),
                "paid_amount": float(claim.paid_amount) if claim.paid_amount else None,
                "service_lines_count": len(claim.service_lines),
                "created_at": claim.created_at.isoformat(),
                "validation_errors": claim.validation_errors
            }
            
            return json.dumps(claim_data, indent=2)
        except Exception as e:
            return f"Error retrieving claim: {str(e)}"

class ValidateClaimTool(BaseTool):
    name = "validate_claim"
    description = "Validate a claim and return validation results"
    db: Session
    
    def _run(
        self, 
        claim_id: int,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            processor = ClaimProcessor(self.db)
            result = processor.validate_claim(claim_id)
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error validating claim: {str(e)}"

class ProcessEDIFileTool(BaseTool):
    name = "process_edi_file"
    description = "Process an EDI file and create claims"
    db: Session
    
    def _run(
        self, 
        file_path: str,
        payer_id: int = 1,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            with open(file_path, 'r') as f:
                edi_content = f.read()
            
            processor = ClaimProcessor(self.db)
            claim = processor.create_claim_from_edi(edi_content, payer_id)
            
            return json.dumps({
                "success": True,
                "claim_id": claim.id,
                "claim_number": claim.claim_number,
                "status": claim.status.value
            }, indent=2)
        except Exception as e:
            return f"Error processing EDI file: {str(e)}"

class AnalyzeRejectionTool(BaseTool):
    name = "analyze_rejection"
    description = "Analyze why a claim was rejected and suggest fixes"
    db: Session
    
    def _run(
        self, 
        claim_id: int,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            claim = self.db.query(Claim).filter(Claim.id == claim_id).first()
            if not claim:
                return f"Claim {claim_id} not found"
            
            if claim.status != ClaimStatus.REJECTED:
                return f"Claim {claim_id} is not rejected (status: {claim.status.value})"
            
            analysis = {
                "claim_id": claim_id,
                "rejection_errors": claim.validation_errors.get('errors', []) if claim.validation_errors else [],
                "suggested_fixes": self._generate_fix_suggestions(claim.validation_errors),
                "common_patterns": self._identify_common_patterns(claim)
            }
            
            return json.dumps(analysis, indent=2)
        except Exception as e:
            return f"Error analyzing rejection: {str(e)}"
    
    def _generate_fix_suggestions(self, validation_errors: Dict) -> List[str]:
        suggestions = []
        if not validation_errors:
            return suggestions
        
        for error in validation_errors.get('errors', []):
            if 'NPI' in error:
                suggestions.append("Verify provider NPI is correct and properly formatted")
            elif 'tooth' in error.lower():
                suggestions.append("Check tooth number and surface codes for dental procedures")
            elif 'procedure code' in error.lower():
                suggestions.append("Verify procedure codes are valid CPT/CDT codes")
            elif 'date' in error.lower():
                suggestions.append("Check service dates are valid and not in the future")
        
        return suggestions
    
    def _identify_common_patterns(self, claim: Claim) -> List[str]:
        patterns = []
        if claim.claim_type.value == "837D":
            patterns.append("Dental claim - ensure tooth-specific information is complete")
        if len(claim.service_lines) > 5:
            patterns.append("Multiple service lines - verify each line has proper diagnosis codes")
        return patterns

class GetPayerInfoTool(BaseTool):
    name = "get_payer_info"
    description = "Get information about a specific payer including validation rules"
    db: Session
    
    def _run(
        self, 
        payer_id: int,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            payer = self.db.query(Payer).filter(Payer.id == payer_id).first()
            if not payer:
                return f"Payer with ID {payer_id} not found"
            
            payer_info = {
                "id": payer.id,
                "name": payer.name,
                "payer_id": payer.payer_id,
                "transmission_method": payer.transmission_method,
                "validation_rules": payer.validation_rules,
                "companion_guide_url": payer.companion_guide_url,
                "is_active": payer.is_active
            }
            
            return json.dumps(payer_info, indent=2)
        except Exception as e:
            return f"Error retrieving payer info: {str(e)}"

class SearchClaimsTool(BaseTool):
    name = "search_claims"
    description = "Search for claims based on various criteria"
    db: Session
    
    def _run(
        self, 
        status: Optional[str] = None,
        claim_type: Optional[str] = None,
        patient_name: Optional[str] = None,
        provider_npi: Optional[str] = None,
        limit: int = 10,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            query = self.db.query(Claim)
            
            if status:
                query = query.filter(Claim.status == status)
            if claim_type:
                query = query.filter(Claim.claim_type == claim_type)
            if patient_name:
                query = query.filter(
                    (Claim.patient_first_name.contains(patient_name)) |
                    (Claim.patient_last_name.contains(patient_name))
                )
            if provider_npi:
                query = query.filter(Claim.provider_npi == provider_npi)
            
            claims = query.limit(limit).all()
            
            results = []
            for claim in claims:
                results.append({
                    "id": claim.id,
                    "claim_number": claim.claim_number,
                    "status": claim.status.value,
                    "patient_name": f"{claim.patient_first_name} {claim.patient_last_name}",
                    "total_charge": float(claim.total_charge),
                    "created_at": claim.created_at.isoformat()
                })
            
            return json.dumps({"results": results, "count": len(results)}, indent=2)
        except Exception as e:
            return f"Error searching claims: {str(e)}"

class UpdateClaimStatusTool(BaseTool):
    name = "update_claim_status"
    description = "Update the status of a claim"
    db: Session
    
    def _run(
        self, 
        claim_id: int,
        new_status: str,
        reason: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            claim = self.db.query(Claim).filter(Claim.id == claim_id).first()
            if not claim:
                return f"Claim {claim_id} not found"
            
            old_status = claim.status.value
            claim.status = ClaimStatus(new_status)
            self.db.commit()
            
            result = {
                "claim_id": claim_id,
                "old_status": old_status,
                "new_status": new_status,
                "reason": reason,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error updating claim status: {str(e)}"

class GenerateReportTool(BaseTool):
    name = "generate_report"
    description = "Generate various types of reports"
    db: Session
    
    def _run(
        self, 
        report_type: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            if report_type == "dashboard":
                return self._generate_dashboard_report()
            elif report_type == "rejection_analysis":
                return self._generate_rejection_report()
            elif report_type == "financial_summary":
                return self._generate_financial_report()
            else:
                return f"Unknown report type: {report_type}"
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    def _generate_dashboard_report(self) -> str:
        from sqlalchemy import func
        
        # Status distribution
        status_counts = self.db.query(
            Claim.status, func.count(Claim.id)
        ).group_by(Claim.status).all()
        
        # Financial summary
        financial = self.db.query(
            func.sum(Claim.total_charge),
            func.sum(Claim.paid_amount)
        ).first()
        
        report = {
            "report_type": "dashboard",
            "status_distribution": {str(status): count for status, count in status_counts},
            "financial_summary": {
                "total_charged": float(financial[0] or 0),
                "total_paid": float(financial[1] or 0)
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return json.dumps(report, indent=2)
    
    def _generate_rejection_report(self) -> str:
        rejected_claims = self.db.query(Claim).filter(
            Claim.status == ClaimStatus.REJECTED
        ).all()
        
        error_patterns = {}
        for claim in rejected_claims:
            if claim.validation_errors:
                for error in claim.validation_errors.get('errors', []):
                    error_patterns[error] = error_patterns.get(error, 0) + 1
        
        report = {
            "report_type": "rejection_analysis",
            "total_rejected": len(rejected_claims),
            "common_errors": error_patterns,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return json.dumps(report, indent=2)
    
    def _generate_financial_report(self) -> str:
        from sqlalchemy import func
        
        financial_data = self.db.query(
            func.sum(Claim.total_charge).label('total_charged'),
            func.sum(Claim.paid_amount).label('total_paid'),
            func.sum(Claim.patient_responsibility).label('patient_responsibility'),
            func.count(Claim.id).label('total_claims')
        ).first()
        
        report = {
            "report_type": "financial_summary",
            "metrics": {
                "total_claims": financial_data.total_claims,
                "total_charged": float(financial_data.total_charged or 0),
                "total_paid": float(financial_data.total_paid or 0),
                "patient_responsibility": float(financial_data.patient_responsibility or 0),
                "collection_rate": (float(financial_data.total_paid or 0) / float(financial_data.total_charged or 1)) * 100
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return json.dumps(report, indent=2)

class GetDashboardStatsTool(BaseTool):
    name = "get_dashboard_stats"
    description = "Get current dashboard statistics"
    db: Session
    
    def _run(self, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        try:
            from sqlalchemy import func
            from datetime import datetime, timedelta
            
            # Total claims by status
            status_counts = self.db.query(
                Claim.status, func.count(Claim.id)
            ).group_by(Claim.status).all()
            
            # Recent activity
            today = datetime.utcnow().date()
            week_ago = today - timedelta(days=7)
            
            today_claims = self.db.query(func.count(Claim.id)).filter(
                func.date(Claim.created_at) == today
            ).scalar()
            
            week_claims = self.db.query(func.count(Claim.id)).filter(
                func.date(Claim.created_at) >= week_ago
            ).scalar()
            
            stats = {
                "status_distribution": {str(status): count for status, count in status_counts},
                "activity": {
                    "claims_today": today_claims,
                    "claims_this_week": week_claims
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return json.dumps(stats, indent=2)
        except Exception as e:
            return f"Error getting dashboard stats: {str(e)}"

class CalculateFinancialMetricsTool(BaseTool):
    name = "calculate_financial_metrics"
    description = "Calculate various financial metrics and KPIs"
    db: Session
    
    def _run(
        self, 
        metric_type: str = "all",
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            from sqlalchemy import func
            
            # Basic financial data
            financial_data = self.db.query(
                func.sum(Claim.total_charge).label('total_charged'),
                func.sum(Claim.paid_amount).label('total_paid'),
                func.sum(Claim.allowed_amount).label('total_allowed'),
                func.sum(Claim.patient_responsibility).label('patient_responsibility'),
                func.count(Claim.id).label('total_claims')
            ).first()
            
            total_charged = float(financial_data.total_charged or 0)
            total_paid = float(financial_data.total_paid or 0)
            total_allowed = float(financial_data.total_allowed or 0)
            
            metrics = {
                "basic_metrics": {
                    "total_claims": financial_data.total_claims,
                    "total_charged": total_charged,
                    "total_paid": total_paid,
                    "total_allowed": total_allowed,
                    "patient_responsibility": float(financial_data.patient_responsibility or 0)
                },
                "calculated_metrics": {
                    "collection_rate": (total_paid / total_charged * 100) if total_charged > 0 else 0,
                    "denial_rate": ((total_charged - total_paid) / total_charged * 100) if total_charged > 0 else 0,
                    "average_claim_value": total_charged / financial_data.total_claims if financial_data.total_claims > 0 else 0,
                    "reimbursement_rate": (total_paid / total_allowed * 100) if total_allowed > 0 else 0
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return json.dumps(metrics, indent=2)
        except Exception as e:
            return f"Error calculating financial metrics: {str(e)}"
