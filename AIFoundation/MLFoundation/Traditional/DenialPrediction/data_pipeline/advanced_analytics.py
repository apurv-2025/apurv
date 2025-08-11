"""
Advanced Analytics Module
Advanced analytics and insights for healthcare denial prediction
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, text
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

from models.database import SessionLocal, Claim, DenialRecord, Provider, Payer
from features.feature_engineering import FeatureEngineer

logger = logging.getLogger(__name__)

class AdvancedAnalytics:
    """Advanced analytics for healthcare denial insights"""
    
    def __init__(self):
        self.feature_engineer = FeatureEngineer()
        
    def get_denial_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get denial trends over time"""
        db = SessionLocal()
        try:
            # Get claims and denials for the period
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Daily denial rates
            daily_stats = db.query(
                func.date(Claim.submission_date).label('date'),
                func.count(Claim.claim_id).label('total_claims'),
                func.sum(func.cast(Claim.is_denied, func.Integer)).label('denials')
            ).filter(
                Claim.submission_date >= start_date
            ).group_by(
                func.date(Claim.submission_date)
            ).order_by(
                func.date(Claim.submission_date)
            ).all()
            
            # Calculate daily denial rates
            trends = []
            for stat in daily_stats:
                denial_rate = (stat.denials / stat.total_claims * 100) if stat.total_claims > 0 else 0
                trends.append({
                    'date': stat.date.strftime('%Y-%m-%d'),
                    'total_claims': stat.total_claims,
                    'denials': stat.denials,
                    'denial_rate': round(denial_rate, 2)
                })
            
            # Calculate moving averages
            df = pd.DataFrame(trends)
            if not df.empty:
                df['denial_rate_ma_7'] = df['denial_rate'].rolling(window=7).mean()
                df['denial_rate_ma_30'] = df['denial_rate'].rolling(window=30).mean()
                
                trends = df.to_dict('records')
            
            return {
                'trends': trends,
                'period_days': days,
                'total_claims': sum(t['total_claims'] for t in trends),
                'total_denials': sum(t['denials'] for t in trends),
                'overall_denial_rate': round(
                    sum(t['denials'] for t in trends) / sum(t['total_claims'] for t in trends) * 100, 2
                ) if sum(t['total_claims'] for t in trends) > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting denial trends: {e}")
            return {'error': str(e)}
        finally:
            db.close()
    
    def get_provider_analytics(self, provider_id: Optional[str] = None) -> Dict[str, Any]:
        """Get provider-specific analytics"""
        db = SessionLocal()
        try:
            query = db.query(Claim)
            if provider_id:
                query = query.filter(Claim.provider_id == provider_id)
            
            # Provider performance metrics
            provider_stats = db.query(
                Claim.provider_id,
                func.count(Claim.claim_id).label('total_claims'),
                func.sum(func.cast(Claim.is_denied, func.Integer)).label('denials'),
                func.avg(Claim.claim_amount).label('avg_claim_amount'),
                func.sum(Claim.claim_amount).label('total_claim_amount')
            ).filter(
                Claim.submission_date >= datetime.utcnow() - timedelta(days=90)
            ).group_by(Claim.provider_id).all()
            
            providers = []
            for stat in provider_stats:
                denial_rate = (stat.denials / stat.total_claims * 100) if stat.total_claims > 0 else 0
                providers.append({
                    'provider_id': stat.provider_id,
                    'total_claims': stat.total_claims,
                    'denials': stat.denials,
                    'denial_rate': round(denial_rate, 2),
                    'avg_claim_amount': round(stat.avg_claim_amount, 2),
                    'total_claim_amount': round(stat.total_claim_amount, 2)
                })
            
            # Sort by denial rate (highest first)
            providers.sort(key=lambda x: x['denial_rate'], reverse=True)
            
            return {
                'providers': providers,
                'total_providers': len(providers),
                'avg_denial_rate': round(
                    sum(p['denial_rate'] for p in providers) / len(providers), 2
                ) if providers else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting provider analytics: {e}")
            return {'error': str(e)}
        finally:
            db.close()
    
    def get_payer_analytics(self, payer_id: Optional[str] = None) -> Dict[str, Any]:
        """Get payer-specific analytics"""
        db = SessionLocal()
        try:
            query = db.query(Claim)
            if payer_id:
                query = query.filter(Claim.payer_id == payer_id)
            
            # Payer performance metrics
            payer_stats = db.query(
                Claim.payer_id,
                func.count(Claim.claim_id).label('total_claims'),
                func.sum(func.cast(Claim.is_denied, func.Integer)).label('denials'),
                func.avg(Claim.claim_amount).label('avg_claim_amount'),
                func.avg(func.extract('day', Claim.submission_date - Claim.service_date)).label('avg_days_to_submit')
            ).filter(
                Claim.submission_date >= datetime.utcnow() - timedelta(days=90)
            ).group_by(Claim.payer_id).all()
            
            payers = []
            for stat in payer_stats:
                denial_rate = (stat.denials / stat.total_claims * 100) if stat.total_claims > 0 else 0
                payers.append({
                    'payer_id': stat.payer_id,
                    'total_claims': stat.total_claims,
                    'denials': stat.denials,
                    'denial_rate': round(denial_rate, 2),
                    'avg_claim_amount': round(stat.avg_claim_amount, 2),
                    'avg_days_to_submit': round(stat.avg_days_to_submit, 1) if stat.avg_days_to_submit else 0
                })
            
            # Sort by denial rate (highest first)
            payers.sort(key=lambda x: x['denial_rate'], reverse=True)
            
            return {
                'payers': payers,
                'total_payers': len(payers),
                'avg_denial_rate': round(
                    sum(p['denial_rate'] for p in payers) / len(payers), 2
                ) if payers else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting payer analytics: {e}")
            return {'error': str(e)}
        finally:
            db.close()
    
    def get_denial_cause_analysis(self, days: int = 90) -> Dict[str, Any]:
        """Analyze denial causes and patterns"""
        db = SessionLocal()
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Get denial records with classification
            denial_records = db.query(DenialRecord).filter(
                DenialRecord.denial_date >= start_date,
                DenialRecord.classification_result.isnot(None)
            ).all()
            
            # Analyze denial causes
            cause_counts = {}
            cause_amounts = {}
            
            for record in denial_records:
                try:
                    classification = json.loads(record.classification_result)
                    cause = classification.get('cause_category', 'unknown')
                    
                    # Get claim amount
                    claim = db.query(Claim).filter(Claim.claim_id == record.claim_id).first()
                    claim_amount = claim.claim_amount if claim else 0
                    
                    # Count causes
                    cause_counts[cause] = cause_counts.get(cause, 0) + 1
                    cause_amounts[cause] = cause_amounts.get(cause, 0) + claim_amount
                    
                except (json.JSONDecodeError, KeyError):
                    cause_counts['unknown'] = cause_counts.get('unknown', 0) + 1
            
            # Calculate percentages and average amounts
            total_denials = sum(cause_counts.values())
            cause_analysis = []
            
            for cause, count in cause_counts.items():
                percentage = (count / total_denials * 100) if total_denials > 0 else 0
                avg_amount = (cause_amounts.get(cause, 0) / count) if count > 0 else 0
                
                cause_analysis.append({
                    'cause': cause,
                    'count': count,
                    'percentage': round(percentage, 2),
                    'total_amount': round(cause_amounts.get(cause, 0), 2),
                    'avg_amount': round(avg_amount, 2)
                })
            
            # Sort by count (highest first)
            cause_analysis.sort(key=lambda x: x['count'], reverse=True)
            
            return {
                'cause_analysis': cause_analysis,
                'total_denials': total_denials,
                'period_days': days
            }
            
        except Exception as e:
            logger.error(f"Error getting denial cause analysis: {e}")
            return {'error': str(e)}
        finally:
            db.close()
    
    def get_revenue_impact_analysis(self, days: int = 90) -> Dict[str, Any]:
        """Analyze revenue impact of denials"""
        db = SessionLocal()
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Get claims and denials
            claims = db.query(Claim).filter(
                Claim.submission_date >= start_date
            ).all()
            
            total_revenue = sum(claim.claim_amount for claim in claims)
            denied_revenue = sum(claim.claim_amount for claim in claims if claim.is_denied)
            approved_revenue = total_revenue - denied_revenue
            
            # Calculate denial impact by provider
            provider_impact = {}
            for claim in claims:
                if claim.provider_id not in provider_impact:
                    provider_impact[claim.provider_id] = {
                        'total_revenue': 0,
                        'denied_revenue': 0,
                        'total_claims': 0,
                        'denied_claims': 0
                    }
                
                provider_impact[claim.provider_id]['total_revenue'] += claim.claim_amount
                provider_impact[claim.provider_id]['total_claims'] += 1
                
                if claim.is_denied:
                    provider_impact[claim.provider_id]['denied_revenue'] += claim.claim_amount
                    provider_impact[claim.provider_id]['denied_claims'] += 1
            
            # Calculate impact metrics
            provider_analysis = []
            for provider_id, impact in provider_impact.items():
                denial_rate = (impact['denied_claims'] / impact['total_claims'] * 100) if impact['total_claims'] > 0 else 0
                revenue_loss_rate = (impact['denied_revenue'] / impact['total_revenue'] * 100) if impact['total_revenue'] > 0 else 0
                
                provider_analysis.append({
                    'provider_id': provider_id,
                    'total_revenue': round(impact['total_revenue'], 2),
                    'denied_revenue': round(impact['denied_revenue'], 2),
                    'revenue_loss_rate': round(revenue_loss_rate, 2),
                    'total_claims': impact['total_claims'],
                    'denied_claims': impact['denied_claims'],
                    'denial_rate': round(denial_rate, 2)
                })
            
            # Sort by revenue loss (highest first)
            provider_analysis.sort(key=lambda x: x['revenue_loss_rate'], reverse=True)
            
            return {
                'overall_impact': {
                    'total_revenue': round(total_revenue, 2),
                    'denied_revenue': round(denied_revenue, 2),
                    'approved_revenue': round(approved_revenue, 2),
                    'revenue_loss_rate': round((denied_revenue / total_revenue * 100), 2) if total_revenue > 0 else 0
                },
                'provider_impact': provider_analysis,
                'period_days': days
            }
            
        except Exception as e:
            logger.error(f"Error getting revenue impact analysis: {e}")
            return {'error': str(e)}
        finally:
            db.close()
    
    def get_prediction_accuracy_analysis(self, days: int = 30) -> Dict[str, Any]:
        """Analyze prediction accuracy and model performance"""
        db = SessionLocal()
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Get predictions with actual outcomes
            predictions = db.query(Claim).filter(
                Claim.submission_date >= start_date,
                Claim.is_denied.isnot(None)  # Has actual outcome
            ).all()
            
            # Calculate accuracy metrics
            total_predictions = len(predictions)
            correct_predictions = 0
            false_positives = 0
            false_negatives = 0
            true_positives = 0
            true_negatives = 0
            
            # For demo purposes, we'll simulate prediction accuracy
            # In production, this would compare actual predictions with outcomes
            for claim in predictions:
                # Simulate prediction (in production, this would be the actual prediction)
                predicted_denial = claim.claim_amount > 5000  # Simple rule for demo
                actual_denial = claim.is_denied
                
                if predicted_denial == actual_denial:
                    correct_predictions += 1
                    if actual_denial:
                        true_positives += 1
                    else:
                        true_negatives += 1
                else:
                    if predicted_denial and not actual_denial:
                        false_positives += 1
                    else:
                        false_negatives += 1
            
            # Calculate metrics
            accuracy = (correct_predictions / total_predictions * 100) if total_predictions > 0 else 0
            precision = (true_positives / (true_positives + false_positives) * 100) if (true_positives + false_positives) > 0 else 0
            recall = (true_positives / (true_positives + false_negatives) * 100) if (true_positives + false_negatives) > 0 else 0
            f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            return {
                'accuracy_metrics': {
                    'total_predictions': total_predictions,
                    'correct_predictions': correct_predictions,
                    'accuracy': round(accuracy, 2),
                    'precision': round(precision, 2),
                    'recall': round(recall, 2),
                    'f1_score': round(f1_score, 2)
                },
                'confusion_matrix': {
                    'true_positives': true_positives,
                    'true_negatives': true_negatives,
                    'false_positives': false_positives,
                    'false_negatives': false_negatives
                },
                'period_days': days
            }
            
        except Exception as e:
            logger.error(f"Error getting prediction accuracy analysis: {e}")
            return {'error': str(e)}
        finally:
            db.close()
    
    def generate_insights_report(self, days: int = 90) -> Dict[str, Any]:
        """Generate comprehensive insights report"""
        try:
            # Get all analytics
            trends = self.get_denial_trends(days)
            provider_analytics = self.get_provider_analytics()
            payer_analytics = self.get_payer_analytics()
            cause_analysis = self.get_denial_cause_analysis(days)
            revenue_impact = self.get_revenue_impact_analysis(days)
            accuracy_analysis = self.get_prediction_accuracy_analysis(days)
            
            # Generate insights
            insights = []
            
            # Trend insights
            if 'trends' in trends and trends['trends']:
                recent_trends = trends['trends'][-7:]  # Last 7 days
                if recent_trends:
                    avg_recent_rate = sum(t['denial_rate'] for t in recent_trends) / len(recent_trends)
                    overall_rate = trends.get('overall_denial_rate', 0)
                    
                    if avg_recent_rate > overall_rate * 1.1:
                        insights.append({
                            'type': 'trend',
                            'severity': 'high',
                            'message': f'Denial rate has increased by {round((avg_recent_rate - overall_rate), 2)}% in the last 7 days',
                            'recommendation': 'Review recent claim submissions and identify common issues'
                        })
            
            # Provider insights
            if 'providers' in provider_analytics and provider_analytics['providers']:
                high_risk_providers = [p for p in provider_analytics['providers'][:5] if p['denial_rate'] > 20]
                if high_risk_providers:
                    insights.append({
                        'type': 'provider',
                        'severity': 'medium',
                        'message': f'{len(high_risk_providers)} providers have denial rates above 20%',
                        'recommendation': 'Provide targeted training and support to high-risk providers'
                    })
            
            # Revenue insights
            if 'overall_impact' in revenue_impact:
                revenue_loss = revenue_impact['overall_impact']['revenue_loss_rate']
                if revenue_loss > 15:
                    insights.append({
                        'type': 'revenue',
                        'severity': 'high',
                        'message': f'Revenue loss due to denials is {revenue_loss}%',
                        'recommendation': 'Implement immediate denial prevention strategies'
                    })
            
            # Cause insights
            if 'cause_analysis' in cause_analysis and cause_analysis['cause_analysis']:
                top_cause = cause_analysis['cause_analysis'][0]
                if top_cause['percentage'] > 30:
                    insights.append({
                        'type': 'cause',
                        'severity': 'medium',
                        'message': f'{top_cause["cause"]} accounts for {top_cause["percentage"]}% of denials',
                        'recommendation': f'Focus on preventing {top_cause["cause"]} denials'
                    })
            
            return {
                'insights': insights,
                'analytics': {
                    'trends': trends,
                    'provider_analytics': provider_analytics,
                    'payer_analytics': payer_analytics,
                    'cause_analysis': cause_analysis,
                    'revenue_impact': revenue_impact,
                    'accuracy_analysis': accuracy_analysis
                },
                'summary': {
                    'total_insights': len(insights),
                    'high_severity': len([i for i in insights if i['severity'] == 'high']),
                    'medium_severity': len([i for i in insights if i['severity'] == 'medium']),
                    'low_severity': len([i for i in insights if i['severity'] == 'low'])
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating insights report: {e}")
            return {'error': str(e)}
    
    def create_visualizations(self, analytics_data: Dict[str, Any]) -> Dict[str, str]:
        """Create visualization charts from analytics data"""
        try:
            charts = {}
            
            # Denial trends chart
            if 'trends' in analytics_data and 'trends' in analytics_data['trends']:
                df = pd.DataFrame(analytics_data['trends']['trends'])
                if not df.empty:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df['date'], y=df['denial_rate'],
                        mode='lines+markers', name='Daily Denial Rate'
                    ))
                    if 'denial_rate_ma_7' in df.columns:
                        fig.add_trace(go.Scatter(
                            x=df['date'], y=df['denial_rate_ma_7'],
                            mode='lines', name='7-Day Moving Average'
                        ))
                    fig.update_layout(
                        title='Denial Rate Trends',
                        xaxis_title='Date',
                        yaxis_title='Denial Rate (%)'
                    )
                    charts['denial_trends'] = fig.to_json()
            
            # Provider performance chart
            if 'provider_analytics' in analytics_data and 'providers' in analytics_data['provider_analytics']:
                providers = analytics_data['provider_analytics']['providers'][:10]  # Top 10
                if providers:
                    df = pd.DataFrame(providers)
                    fig = px.bar(
                        df, x='provider_id', y='denial_rate',
                        title='Provider Denial Rates (Top 10)',
                        labels={'provider_id': 'Provider ID', 'denial_rate': 'Denial Rate (%)'}
                    )
                    charts['provider_performance'] = fig.to_json()
            
            # Denial causes chart
            if 'cause_analysis' in analytics_data and 'cause_analysis' in analytics_data['cause_analysis']:
                causes = analytics_data['cause_analysis']['cause_analysis']
                if causes:
                    df = pd.DataFrame(causes)
                    fig = px.pie(
                        df, values='count', names='cause',
                        title='Denial Causes Distribution'
                    )
                    charts['denial_causes'] = fig.to_json()
            
            return charts
            
        except Exception as e:
            logger.error(f"Error creating visualizations: {e}")
            return {'error': str(e)}
    
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
            logger.error(f"Error getting ingestion stats: {e}")
            return {}
        finally:
            db.close() 