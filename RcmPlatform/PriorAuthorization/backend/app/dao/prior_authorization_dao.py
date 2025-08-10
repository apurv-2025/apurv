# File: app/dao/enhanced_authorization_dao.py
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, func, text, case
from app.dao.base import BaseDAO
from app.models.health_insurance import (
    PriorAuthorizationRequest, 
    PriorAuthorizationResponse,
    AuthorizationAudit
)
from app.schemas.prior_authorization import (
    AuthorizationSummary,
    AuthorizationSearchRequest
)
from app.schemas.statistics import (
    AuthorizationStatistics,
    ProviderStatistics
)
from datetime import date, datetime, timedelta
import uuid


class EnhancedAuthorizationDAO(BaseDAO[PriorAuthorizationRequest]):
    def __init__(self):
        super().__init__(PriorAuthorizationRequest)

    def create_request_with_id(self, db: Session, request_data: Dict[str, Any]) -> PriorAuthorizationRequest:
        """Create authorization request with auto-generated IDs"""
        if 'request_id' not in request_data:
            request_data['request_id'] = f"PA-{uuid.uuid4().hex[:8].upper()}"
        
        if 'patient_id' not in request_data:
            request_data['patient_id'] = f"PAT-{uuid.uuid4().hex[:8].upper()}"
        
        # Generate control numbers
        timestamp = datetime.now()
        request_data.setdefault('interchange_control_number', f"ICN{timestamp.strftime('%Y%m%d%H%M%S')}")
        request_data.setdefault('group_control_number', f"GCN{timestamp.strftime('%H%M%S')}")
        request_data.setdefault('transaction_control_number', f"TCN{timestamp.strftime('%M%S')}")
        
        return self.create(db, obj_in=request_data)

    def get_authorization_summary(self, db: Session, request_id: str) -> Optional[AuthorizationSummary]:
        """Get authorization summary"""
        request = self.get_by_field(db, 'request_id', request_id)
        if request:
            return AuthorizationSummary.model_validate(request)
        return None

    def advanced_search(
        self, 
        db: Session, 
        search_request: AuthorizationSearchRequest,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[AuthorizationSummary], int]:
        """Advanced authorization search with count"""
        query = db.query(PriorAuthorizationRequest)
        
        # Build filters
        if search_request.patient_name:
            query = query.filter(
                or_(
                    PriorAuthorizationRequest.patient_first_name.ilike(f"%{search_request.patient_name}%"),
                    PriorAuthorizationRequest.patient_last_name.ilike(f"%{search_request.patient_name}%")
                )
            )
        
        if search_request.member_id:
            query = query.filter(PriorAuthorizationRequest.member_id == search_request.member_id)
        
        if search_request.provider_npi:
            query = query.filter(
                or_(
                    PriorAuthorizationRequest.requesting_provider_npi == search_request.provider_npi,
                    PriorAuthorizationRequest.servicing_provider_npi == search_request.provider_npi
                )
            )
        
        if search_request.status:
            query = query.filter(PriorAuthorizationRequest.status == search_request.status)
        
        if search_request.service_date_from:
            query = query.filter(PriorAuthorizationRequest.service_date_from >= search_request.service_date_from)
        
        if search_request.service_date_to:
            query = query.filter(PriorAuthorizationRequest.service_date_to <= search_request.service_date_to)
        
        if search_request.created_from:
            query = query.filter(PriorAuthorizationRequest.created_at >= search_request.created_from)
        
        if search_request.created_to:
            query = query.filter(PriorAuthorizationRequest.created_at <= search_request.created_to)
        
        if search_request.priority:
            query = query.filter(PriorAuthorizationRequest.priority == search_request.priority.value)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        requests = query.order_by(desc(PriorAuthorizationRequest.created_at)).offset(skip).limit(limit).all()
        summaries = [AuthorizationSummary.model_validate(r) for r in requests]
        
        return summaries, total

    def get_requests_by_status_count(self, db: Session) -> Dict[str, int]:
        """Get count of requests by status"""
        status_counts = db.query(
            PriorAuthorizationRequest.status,
            func.count(PriorAuthorizationRequest.id)
        ).group_by(PriorAuthorizationRequest.status).all()
        
        return {status: count for status, count in status_counts}

    def get_urgent_requests(
        self, 
        db: Session, 
        hours_threshold: int = 24,
        skip: int = 0,
        limit: int = 100
    ) -> List[PriorAuthorizationRequest]:
        """Get urgent requests older than threshold"""
        threshold_time = datetime.utcnow() - timedelta(hours=hours_threshold)
        
        query = db.query(PriorAuthorizationRequest).filter(
            and_(
                PriorAuthorizationRequest.priority == 'urgent',
                PriorAuthorizationRequest.status.in_(['submitted', 'under_review']),
                PriorAuthorizationRequest.created_at <= threshold_time
            )
        )
        
        return query.order_by(PriorAuthorizationRequest.created_at).offset(skip).limit(limit).all()

    def get_requests_requiring_followup(self, db: Session) -> List[PriorAuthorizationRequest]:
        """Get requests that require follow-up"""
        query = text("""
            SELECT par.* 
            FROM prior_authorization_requests par
            JOIN prior_authorization_responses pres ON par.request_id = pres.request_id
            WHERE pres.follow_up_required = true 
            AND pres.follow_up_date <= CURRENT_DATE
        """)
        
        result = db.execute(query)
        return [PriorAuthorizationRequest(**row._asdict()) for row in result]

    def get_authorization_statistics(
        self, 
        db: Session, 
        date_from: date, 
        date_to: date
    ) -> AuthorizationStatistics:
        """Get authorization statistics for date range"""
        
        # Base query for date range
        base_query = db.query(PriorAuthorizationRequest).filter(
            and_(
                PriorAuthorizationRequest.created_at >= date_from,
                PriorAuthorizationRequest.created_at <= date_to
            )
        )
        
        total_requests = base_query.count()
        
        # Status counts
        status_query = base_query.join(PriorAuthorizationResponse, isouter=True)
        status_counts = status_query.with_entities(
            PriorAuthorizationResponse.response_code,
            func.count(PriorAuthorizationRequest.id)
        ).group_by(PriorAuthorizationResponse.response_code).all()
        
        approved = sum(count for code, count in status_counts if code in ['A1', 'A2'])
        denied = sum(count for code, count in status_counts if code == 'A3')
        pending = sum(count for code, count in status_counts if code in ['A4', None])
        
        approval_rate = (approved / total_requests * 100) if total_requests > 0 else 0
        
        # Priority distribution
        priority_query = base_query.with_entities(
            PriorAuthorizationRequest.priority,
            func.count(PriorAuthorizationRequest.id)
        ).group_by(PriorAuthorizationRequest.priority).all()
        
        by_priority = {priority: count for priority, count in priority_query}
        
        # Status distribution
        by_status = {
            'submitted': pending,
            'approved': approved,
            'denied': denied,
            'pending': pending
        }
        
        # Processing time calculation
        processing_time_query = text("""
            SELECT AVG(EXTRACT(EPOCH FROM (pres.created_at - par.created_at))/3600) as avg_hours
            FROM prior_authorization_requests par
            JOIN prior_authorization_responses pres ON par.request_id = pres.request_id
            WHERE par.created_at BETWEEN :date_from AND :date_to
        """)
        
        avg_processing_time = db.execute(
            processing_time_query, 
            {"date_from": date_from, "date_to": date_to}
        ).scalar() or 0
        
        # Top providers
        provider_query = base_query.with_entities(
            PriorAuthorizationRequest.requesting_provider_npi,
            PriorAuthorizationRequest.requesting_provider_name,
            func.count(PriorAuthorizationRequest.id).label('total')
        ).group_by(
            PriorAuthorizationRequest.requesting_provider_npi,
            PriorAuthorizationRequest.requesting_provider_name
        ).order_by(desc('total')).limit(10).all()
        
        by_provider = [
            {
                "npi": npi,
                "name": name,
                "total_requests": total
            }
            for npi, name, total in provider_query
        ]
        
        return AuthorizationStatistics(
            total_requests=total_requests,
            approved_requests=approved,
            denied_requests=denied,
            pending_requests=pending,
            approval_rate=approval_rate,
            average_processing_time_hours=avg_processing_time,
            by_priority=by_priority,
            by_status=by_status,
            by_provider=by_provider,
            period_start=date_from,
            period_end=date_to,
            generated_at=datetime.utcnow()
        )

    def get_provider_statistics(
        self, 
        db: Session, 
        provider_npi: str,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Optional[ProviderStatistics]:
        """Get statistics for specific provider"""
        
        query = db.query(PriorAuthorizationRequest).filter(
            or_(
                PriorAuthorizationRequest.requesting_provider_npi == provider_npi,
                PriorAuthorizationRequest.servicing_provider_npi == provider_npi
            )
        )
        
        if date_from:
            query = query.filter(PriorAuthorizationRequest.created_at >= date_from)
        if date_to:
            query = query.filter(PriorAuthorizationRequest.created_at <= date_to)
        
        requests = query.all()
        if not requests:
            return None
        
        total_requests = len(requests)
        provider_name = requests[0].requesting_provider_name
        
        # Get responses for approval calculation
        response_query = db.query(PriorAuthorizationResponse).filter(
            PriorAuthorizationResponse.request_id.in_([r.request_id for r in requests])
        )
        responses = response_query.all()
        
        approved = sum(1 for r in responses if r.response_code in ['A1', 'A2'])
        denied = sum(1 for r in responses if r.response_code == 'A3')
        approval_rate = (approved / len(responses) * 100) if responses else 0
        
        # Processing time
        if responses:
            processing_times = [
                (r.created_at - next(req.created_at for req in requests if req.request_id == r.request_id)).total_seconds() / 3600
                for r in responses
            ]
            avg_processing_time = sum(processing_times) / len(processing_times)
        else:
            avg_processing_time = 0
        
        # Common procedures and diagnoses
        all_procedures = []
        all_diagnoses = []
        
        for request in requests:
            if request.procedure_codes:
                all_procedures.extend([p.get('code') for p in request.procedure_codes if p.get('code')])
            if request.diagnosis_codes:
                all_diagnoses.extend([d.get('code') for d in request.diagnosis_codes if d.get('code')])
        
        # Count frequencies
        from collections import Counter
        procedure_counts = Counter(all_procedures)
        diagnosis_counts = Counter(all_diagnoses)
        
        common_procedures = [
            {"code": code, "count": count}
            for code, count in procedure_counts.most_common(10)
        ]
        
        common_diagnoses = [
            {"code": code, "count": count}
            for code, count in diagnosis_counts.most_common(10)
        ]
        
        return ProviderStatistics(
            provider_npi=provider_npi,
            provider_name=provider_name,
            total_requests=total_requests,
            approved_requests=approved,
            denied_requests=denied,
            approval_rate=approval_rate,
            average_processing_time_hours=avg_processing_time,
            common_procedures=common_procedures,
            common_diagnoses=common_diagnoses
        )

    def get_expiring_authorizations(
        self, 
        db: Session, 
        days_ahead: int = 30
    ) -> List[PriorAuthorizationResponse]:
        """Get authorizations expiring within specified days"""
        expiration_date = date.today() + timedelta(days=days_ahead)
        
        query = db.query(PriorAuthorizationResponse).filter(
            and_(
                PriorAuthorizationResponse.response_code.in_(['A1', 'A2']),
                PriorAuthorizationResponse.expiration_date <= expiration_date,
                PriorAuthorizationResponse.expiration_date >= date.today()
            )
        )
        
        return query.order_by(PriorAuthorizationResponse.expiration_date).all()


