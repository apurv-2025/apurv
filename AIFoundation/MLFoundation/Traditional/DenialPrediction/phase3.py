# Phase 3: Advanced Features Implementation
# Continuous Learning, Model Drift Detection, and Auto-Retraining

import mlflow
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import asyncio
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass
from evidently.report import Report
from evidently.metrics import DataDriftPreset, TargetDriftPreset, ClassificationPreset
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfMissingValues, TestShareOfMissingValues
import joblib
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
import redis
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ModelPerformanceMetrics:
    """Model performance metrics structure"""
    auc: float
    precision: float
    recall: float
    f1_score: float
    timestamp: datetime
    model_version: str
    data_drift_score: float
    target_drift_detected: bool

class ContinuousLearning:
    """Continuous learning system for model monitoring and retraining"""
    
    def __init__(self, model_name: str, redis_host: str = 'localhost'):
        self.model_name = model_name
        self.client = mlflow.tracking.MlflowClient()
        self.redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        self.performance_threshold = 0.8
        self.drift_threshold = 0.3
        self.retraining_cooldown = timedelta(days=1)
        
    def monitor_data_drift(self, reference_data: pd.DataFrame, 
                          current_data: pd.DataFrame) -> Dict[str, Any]:
        """Monitor data and target drift using Evidently AI"""
        try:
            # Create drift report
            drift_report = Report(metrics=[
                DataDriftPreset(),
                TargetDriftPreset() if 'is_denied' in current_data.columns else None
            ])
            
            drift_report.run(
                reference_data=reference_data, 
                current_data=current_data,
                column_mapping=self._get_column_mapping()
            )
            
            results = drift_report.as_dict()
            
            # Extract key metrics
            data_drift_metrics = results['metrics'][0]['result']
            drift_results = {
                'data_drift_detected': data_drift_metrics.get('dataset_drift', False),
                'drift_score': data_drift_metrics.get('drift_share', 0.0),
                'drifted_features': self._extract_drifted_features(data_drift_metrics),
                'timestamp': datetime.now().isoformat()
            }
            
            # Add target drift if available
            if len(results['metrics']) > 1:
                target_drift_metrics = results['metrics'][1]['result']
                drift_results.update({
                    'target_drift_detected': target_drift_metrics.get('target_drift', False),
                    'target_drift_score': target_drift_metrics.get('drift_score', 0.0)
                })
            
            # Cache results
            self._cache_drift_results(drift_results)
            
            logger.info(f"Drift monitoring completed. Drift detected: {drift_results['data_drift_detected']}")
            return drift_results
            
        except Exception as e:
            logger.error(f"Error in drift monitoring: {str(e)}")
            raise
    
    def _get_column_mapping(self):
        """Define column mapping for Evidently"""
        from evidently.utils import ColumnMapping
        return ColumnMapping(
            target='is_denied',
            numerical_features=[
                'claim_amount', 'patient_age', 'historical_denial_rate',
                'avg_days_to_pay', 'provider_volume'
            ],
            categorical_features=[
                'payer_id', 'provider_specialty', 'claim_type',
                'authorization_required'
            ]
        )
    
    def _extract_drifted_features(self, drift_metrics: Dict) -> List[str]:
        """Extract features that show significant drift"""
        drifted_features = []
        if 'drift_by_columns' in drift_metrics:
            for feature, metrics in drift_metrics['drift_by_columns'].items():
                if metrics.get('drift_detected', False):
                    drifted_features.append(feature)
        return drifted_features
    
    def evaluate_model_performance(self, model, X_test: pd.DataFrame, 
                                 y_test: pd.Series) -> ModelPerformanceMetrics:
        """Evaluate current model performance"""
        try:
            # Get predictions
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            y_pred = (y_pred_proba >= 0.5).astype(int)
            
            # Calculate metrics
            metrics = ModelPerformanceMetrics(
                auc=roc_auc_score(y_test, y_pred_proba),
                precision=precision_score(y_test, y_pred, zero_division=0),
                recall=recall_score(y_test, y_pred, zero_division=0),
                f1_score=f1_score(y_test, y_pred, zero_division=0),
                timestamp=datetime.now(),
                model_version=self._get_current_model_version(),
                data_drift_score=0.0,  # Updated separately
                target_drift_detected=False  # Updated separately
            )
            
            # Log metrics to MLflow
            with mlflow.start_run():
                mlflow.log_metrics({
                    'auc': metrics.auc,
                    'precision': metrics.precision,
                    'recall': metrics.recall,
                    'f1_score': metrics.f1_score
                })
            
            # Cache performance metrics
            self._cache_performance_metrics(metrics)
            
            logger.info(f"Model performance evaluated. AUC: {metrics.auc:.3f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error evaluating model performance: {str(e)}")
            raise
    
    def should_retrain(self, drift_results: Dict[str, Any], 
                      performance_metrics: ModelPerformanceMetrics) -> Dict[str, Any]:
        """Determine if model retraining is needed"""
        reasons = []
        
        # Check performance degradation
        if performance_metrics.auc < self.performance_threshold:
            reasons.append(f"AUC below threshold: {performance_metrics.auc:.3f} < {self.performance_threshold}")
        
        # Check data drift
        if drift_results.get('data_drift_detected', False):
            reasons.append(f"Data drift detected. Score: {drift_results.get('drift_score', 0):.3f}")
        
        # Check target drift
        if drift_results.get('target_drift_detected', False):
            reasons.append("Target drift detected")
        
        # Check retraining cooldown
        last_retrain = self._get_last_retrain_time()
        if last_retrain and datetime.now() - last_retrain < self.retraining_cooldown:
            return {
                'should_retrain': False,
                'reason': 'Retraining cooldown period active',
                'next_eligible_time': (last_retrain + self.retraining_cooldown).isoformat()
            }
        
        should_retrain = len(reasons) > 0
        
        result = {
            'should_retrain': should_retrain,
            'reasons': reasons,
            'drift_score': drift_results.get('drift_score', 0),
            'current_auc': performance_metrics.auc,
            'drifted_features': drift_results.get('drifted_features', [])
        }
        
        logger.info(f"Retrain decision: {should_retrain}. Reasons: {reasons}")
        return result
    
    async def trigger_retraining(self, retrain_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger model retraining pipeline"""
        if not retrain_decision['should_retrain']:
            return {'status': 'no_retraining_needed'}
        
        try:
            # Update last retrain time
            self._update_last_retrain_time()
            
            # Start retraining workflow
            retraining_job = await self._start_retraining_workflow(retrain_decision)
            
            logger.info(f"Retraining triggered. Job ID: {retraining_job.get('job_id')}")
            return retraining_job
            
        except Exception as e:
            logger.error(f"Error triggering retraining: {str(e)}")
            raise
    
    async def _start_retraining_workflow(self, retrain_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Start the actual retraining workflow"""
        import uuid
        
        job_id = str(uuid.uuid4())
        
        # This would integrate with your workflow orchestrator (Airflow, Prefect, etc.)
        # For now, we'll simulate the process
        retraining_config = {
            'job_id': job_id,
            'model_name': self.model_name,
            'retrain_reasons': retrain_decision['reasons'],
            'drifted_features': retrain_decision.get('drifted_features', []),
            'target_performance': self.performance_threshold + 0.05,  # Aim higher
            'started_at': datetime.now().isoformat(),
            'status': 'started'
        }
        
        # Cache job info
        self.redis_client.setex(
            f"retraining_job:{job_id}",
            3600 * 24,  # 24 hours TTL
            json.dumps(retraining_config)
        )
        
        # Here you would trigger your actual retraining pipeline
        # await self._trigger_airflow_dag('retrain_denial_model', retraining_config)
        
        return retraining_config
    
    def _cache_drift_results(self, drift_results: Dict[str, Any]):
        """Cache drift monitoring results"""
        key = f"drift_results:{self.model_name}:{datetime.now().strftime('%Y%m%d_%H')}"
        self.redis_client.setex(key, 3600 * 24, json.dumps(drift_results))
    
    def _cache_performance_metrics(self, metrics: ModelPerformanceMetrics):
        """Cache performance metrics"""
        key = f"performance:{self.model_name}:{datetime.now().strftime('%Y%m%d_%H')}"
        metrics_dict = {
            'auc': metrics.auc,
            'precision': metrics.precision,
            'recall': metrics.recall,
            'f1_score': metrics.f1_score,
            'timestamp': metrics.timestamp.isoformat(),
            'model_version': metrics.model_version
        }
        self.redis_client.setex(key, 3600 * 24, json.dumps(metrics_dict))
    
    def _get_current_model_version(self) -> str:
        """Get current model version from MLflow"""
        try:
            latest_version = self.client.get_latest_versions(
                self.model_name, 
                stages=["Production"]
            )[0]
            return latest_version.version
        except:
            return "unknown"
    
    def _get_last_retrain_time(self) -> Optional[datetime]:
        """Get last retraining time"""
        cached_time = self.redis_client.get(f"last_retrain:{self.model_name}")
        if cached_time:
            return datetime.fromisoformat(cached_time)
        return None
    
    def _update_last_retrain_time(self):
        """Update last retraining time"""
        self.redis_client.set(
            f"last_retrain:{self.model_name}",
            datetime.now().isoformat()
        )

class FeatureEvolution:
    """Handle feature evolution and backward compatibility"""
    
    def __init__(self):
        self.feature_registry = {}
        self.version_mappings = {}
    
    def register_feature_version(self, feature_name: str, version: str, 
                                definition: Dict[str, Any]):
        """Register a new feature version"""
        if feature_name not in self.feature_registry:
            self.feature_registry[feature_name] = {}
        
        self.feature_registry[feature_name][version] = definition
        logger.info(f"Registered feature {feature_name} version {version}")
    
    def get_feature_mapping(self, from_version: str, to_version: str) -> Dict[str, str]:
        """Get feature mapping between versions"""
        mapping_key = f"{from_version}_to_{to_version}"
        return self.version_mappings.get(mapping_key, {})
    
    def transform_features_for_version(self, features: pd.DataFrame, 
                                     target_version: str) -> pd.DataFrame:
        """Transform features to match target model version"""
        # Implementation would depend on specific feature evolution needs
        # This is a simplified example
        transformed = features.copy()
        
        # Handle deprecated features
        if 'old_feature_name' in transformed.columns and target_version >= "2.0":
            transformed['new_feature_name'] = transformed['old_feature_name']
            transformed.drop('old_feature_name', axis=1, inplace=True)
        
        return transformed

# Auto-Feature Engineering Pipeline
class AutoFeatureEngineering:
    """Automated feature engineering for improved model performance"""
    
    def __init__(self):
        self.feature_generators = []
        self.feature_importance_threshold = 0.01
    
    def generate_time_features(self, df: pd.DataFrame, 
                             timestamp_col: str = 'service_date') -> pd.DataFrame:
        """Generate time-based features"""
        if timestamp_col not in df.columns:
            return df
        
        df_enhanced = df.copy()
        df_enhanced[timestamp_col] = pd.to_datetime(df_enhanced[timestamp_col])
        
        # Extract time features
        df_enhanced['service_day_of_week'] = df_enhanced[timestamp_col].dt.dayofweek
        df_enhanced['service_month'] = df_enhanced[timestamp_col].dt.month
        df_enhanced['service_quarter'] = df_enhanced[timestamp_col].dt.quarter
        df_enhanced['is_weekend'] = df_enhanced['service_day_of_week'].isin([5, 6])
        df_enhanced['days_since_epoch'] = (df_enhanced[timestamp_col] - pd.Timestamp('2020-01-01')).dt.days
        
        return df_enhanced
    
    def generate_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate interaction features"""
        df_enhanced = df.copy()
        
        # Provider-Payer interactions
        if 'provider_id' in df.columns and 'payer_id' in df.columns:
            df_enhanced['provider_payer_combo'] = (
                df_enhanced['provider_id'].astype(str) + '_' + 
                df_enhanced['payer_id'].astype(str)
            )
        
        # Amount-based interactions
        if 'claim_amount' in df.columns and 'patient_age' in df.columns:
            df_enhanced['amount_per_age'] = df_enhanced['claim_amount'] / (df_enhanced['patient_age'] + 1)
        
        return df_enhanced
    
    def generate_aggregation_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate aggregation-based features"""
        df_enhanced = df.copy()
        
        # Provider aggregations (would be pre-computed in practice)
        if 'provider_id' in df.columns:
            provider_stats = df.groupby('provider_id').agg({
                'claim_amount': ['mean', 'std', 'count'],
                'is_denied': 'mean'
            }).round(4)
            
            provider_stats.columns = [f'provider_{col[0]}_{col[1]}' for col in provider_stats.columns]
            df_enhanced = df_enhanced.merge(provider_stats, on='provider_id', how='left')
        
        return df_enhanced
    
    def auto_feature_selection(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Automatic feature selection based on importance"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.feature_selection import SelectFromModel
        
        # Train a quick model for feature importance
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X, y)
        
        # Select features
        selector = SelectFromModel(rf, threshold=self.feature_importance_threshold)
        selector.fit(X, y)
        
        selected_features = X.columns[selector.get_support()].tolist()
        logger.info(f"Auto-selected {len(selected_features)} features from {len(X.columns)}")
        
        return selected_features

# Example usage and integration
async def run_continuous_learning_pipeline():
    """Example of running the continuous learning pipeline"""
    
    # Initialize system
    cl_system = ContinuousLearning("denial_predictor")
    
    # Simulate data (in practice, this would come from your data pipeline)
    reference_data = pd.DataFrame({
        'claim_amount': np.random.normal(1000, 500, 1000),
        'patient_age': np.random.randint(18, 80, 1000),
        'historical_denial_rate': np.random.beta(2, 8, 1000),
        'is_denied': np.random.binomial(1, 0.2, 1000)
    })
    
    current_data = pd.DataFrame({
        'claim_amount': np.random.normal(1200, 600, 1000),  # Drift in amount
        'patient_age': np.random.randint(18, 80, 1000),
        'historical_denial_rate': np.random.beta(2, 8, 1000),
        'is_denied': np.random.binomial(1, 0.25, 1000)  # Drift in target
    })
    
    try:
        # Monitor drift
        drift_results = cl_system.monitor_data_drift(reference_data, current_data)
        
        # Evaluate model performance (would use actual model)
        # For demo, we'll create a simple model
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(random_state=42)
        
        X_train = reference_data.drop('is_denied', axis=1)
        y_train = reference_data['is_denied']
        X_test = current_data.drop('is_denied', axis=1)
        y_test = current_data['is_denied']
        
        model.fit(X_train, y_train)
        
        performance_metrics = cl_system.evaluate_model_performance(model, X_test, y_test)
        
        # Check if retraining is needed
        retrain_decision = cl_system.should_retrain(drift_results, performance_metrics)
        
        # Trigger retraining if needed
        if retrain_decision['should_retrain']:
            retraining_result = await cl_system.trigger_retraining(retrain_decision)
            print(f"Retraining triggered: {retraining_result}")
        else:
            print("No retraining needed")
            
    except Exception as e:
        logger.error(f"Error in continuous learning pipeline: {str(e)}")

if __name__ == "__main__":
    # Run the pipeline
    asyncio.run(run_continuous_learning_pipeline())
