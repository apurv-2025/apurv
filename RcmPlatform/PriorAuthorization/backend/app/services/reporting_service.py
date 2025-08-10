# File: app/services/enhanced_reporting_service.py
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.dao.enhanced_authorization_dao import EnhancedAuthorizationDAO
from app.dao.enhanced_patient_dao import EnhancedPatientDAO
from app.dao.enhanced_codes_dao import EnhancedCodesDAO
from app.schemas.reports import ReportRequest, ReportResponse, ReportMetadata, ReportType
from app.schemas.statistics import SystemStatistics
from datetime import datetime, date
import uuid
import json


class EnhancedReportingService:
    def __init__(self):
        self.auth_dao = EnhancedAuthorizationDAO()
        self.patient_dao = EnhancedPatientDAO()
        self.codes_dao = EnhancedCodesDAO()

    def generate_report(self, db: Session, report_request: ReportRequest) -> ReportResponse:
        """Generate report based on request"""
        report_id = f"RPT-{uuid.uuid4().hex[:8].upper()}"
        
        try:
            data = None
            
            if report_request.report_type == ReportType.AUTHORIZATION_SUMMARY:
                data = self._generate_authorization_summary(db, report_request)
            elif report_request.report_type == ReportType.PROVIDER_PERFORMANCE:
                data = self._generate_provider_performance(db, report_request)
            elif report_request.report_type == ReportType.PATIENT_DEMOGRAPHICS:
                data = self._generate_patient_demographics(db, report_request)
            elif report_request.report_type == ReportType.AUDIT_TRAIL:
                data = self._generate_audit_trail(db, report_request)
            elif report_request.report_type == ReportType.EDI_TRANSACTION_LOG:
                data = self._generate_edi_transaction_log(db, report_request)
            
            metadata = ReportMetadata(
                report_id=report_id,
                report_type=report_request.report_type,
                format=report_request.format,
                status="completed",
                date_from=report_request.date_from,
                date_to=report_request.date_to,
                record_count=len(data.get('records', [])) if data else 0,
                completed_at=datetime.utcnow(),
                created_at=datetime.utcnow()
            )
            
            return ReportResponse(
                metadata=metadata,
                data=data,
                message="Report generated successfully"
            )
            
        except Exception as e:
            metadata = ReportMetadata(
                report_id=report_id,
                report_type=report_request.report_type,
                format=report_request.format,
                status="failed",
                date_from=report_request.date_from,
                date_to=report_request.date_to,
                error_message=str(e),
                created_at=datetime.utcnow()
            )
            
            return ReportResponse(
                metadata=metadata,
                message=f"Report generation failed: {str(e)}"
            )

    def _generate_authorization_summary(self, db: Session, request: ReportRequest) -> Dict[str, Any]:
        """Generate authorization summary report"""
        stats = self.auth_dao.get_authorization_statistics(
            db, request.date_from, request.date_to
        )
        
        # Get detailed records if requested
        records = []
        if request.include_details:
            from app.schemas.prior_authorization import AuthorizationSearchRequest
            search_req = AuthorizationSearchRequest(
                created_from=datetime.combine(request.date_from, datetime.min.time()),
                created_to=datetime.combine(request.date_to, datetime.max.time())
            )
            summaries, _ = self.auth_dao.advanced_search(db, search_req, limit=10000)
            records = [summary.model_dump() for summary in summaries]
        
        return {
            "summary": stats.model_dump(),
            "records": records
        }

    def _generate_provider_performance(self, db: Session, request: ReportRequest) -> Dict[str, Any]:
        """Generate provider performance report"""
        provider_npi = request.filters.get('provider_npi') if request.filters else None
        
        if provider_npi:
            # Single provider report
            stats = self.auth_dao.get_provider_statistics(
                db, provider_npi, request.date_from, request.date_to
            )
            return {"provider": stats.model_dump() if stats else None}
        else:
            # All providers summary
            auth_stats = self.auth_dao.get_authorization_statistics(
                db, request.date_from, request.date_to
            )
            return {"providers": auth_stats.by_provider}

    def _generate_patient_demographics(self, db: Session, request: ReportRequest) -> Dict[str, Any]:
        """Generate patient demographics report"""
        stats = self.patient_dao.get_patient_statistics(db)
        
        records = []
        if request.include_details:
            from app.schemas.patient_information import PatientSearchRequest
            search_req = PatientSearchRequest()
            summaries, _ = self.patient_dao.advanced_search(db, search_req, limit=10000)
            records = [summary.model_dump() for summary in summaries]
        
        return {
            "demographics": stats.model_dump(),
            "records": records
        }

    def _generate_audit_trail(self, db: Session, request: ReportRequest) -> Dict[str, Any]:
        """Generate audit trail report"""
        # This would integrate with the audit DAO
        return {"audit_records": []}

    def _generate_edi_transaction_log(self, db: Session, request: ReportRequest) -> Dict[str, Any]:
        """Generate EDI transaction log report"""
        # This would track EDI transactions
        return {"edi_transactions": []}

    def get_system_statistics(self, db: Session) -> SystemStatistics:
        """Get comprehensive system statistics"""
        # Get authorization stats for last 30 days
        end_date = date.today()
        start_date = end_date.replace(day=1)  # First day of current month
        
        auth_stats = self.auth_dao.get_authorization_statistics(db, start_date, end_date)
        patient_stats = self.patient_dao.get_patient_statistics(db)
        
        # Get top providers
        top_providers = []
        for provider_info in auth_stats.by_provider[:5]:
            provider_stats = self.auth_dao.get_provider_statistics(
                db, provider_info['npi'], start_date, end_date
            )
            if provider_stats:
                top_providers.append(provider_stats)
        
        return SystemStatistics(
            authorization_stats=auth_stats,
            patient_stats=patient_stats,
            top_providers=top_providers,
            edi_transaction_volume={
                "278_requests": auth_stats.total_requests,
                "278_responses": auth_stats.approved_requests + auth_stats.denied_requests,
                "275_patient_info": patient_stats.total_patients
            },
            system_uptime_hours=0.0,  # Would be implemented with system monitoring
            database_size_mb=0.0,     # Would be implemented with DB monitoring
            generated_at=datetime.utcnow()
        )
