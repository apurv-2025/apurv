"""
Airflow DAGs for Healthcare Claims Data Pipeline
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from datetime import datetime, timedelta
import logging
import os
import json
import asyncio

# Import our modules
from data_pipeline.ingestion import DataIngestionPipeline
from models.database import SessionLocal, Claim, Provider, Payer
from features.feature_engineering import FeatureEngineer
from models.denial_predictor import DenialPredictor
from data_pipeline.streaming_processor import StreamProcessor, StreamEvent

# Default arguments
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

# ============================================================================
# DAILY CLAIMS INGESTION DAG
# ============================================================================

def ingest_claims_data(**context):
    """Ingest claims data from various sources"""
    pipeline = DataIngestionPipeline()
    
    # Process 837 files (claim submissions)
    claims_data = []
    
    # Check for 837 files in the data directory
    data_dir = "/data/claims"
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith('.837') or file.endswith('.txt'):
                file_path = os.path.join(data_dir, file)
                claims = pipeline.process_837_file(file_path)
                claims_data.extend(claims)
    
    # Process CSV files if no 837 files found
    if not claims_data:
        csv_dir = "/data/csv"
        if os.path.exists(csv_dir):
            for file in os.listdir(csv_dir):
                if file.endswith('.csv'):
                    file_path = os.path.join(csv_dir, file)
                    claims = pipeline.process_csv_file(file_path)
                    claims_data.extend(claims)
    
    # Generate sample data if no files found (for demo purposes)
    if not claims_data:
        logging.info("No data files found, generating sample data")
        claims_data = pipeline.generate_sample_data(100)
    
    # Ingest claims into database
    if claims_data:
        result = pipeline.ingest_claims_data(claims_data)
        logging.info(f"Ingested {result['ingested_count']} claims, {result['error_count']} errors")
        
        # Push result to XCom for downstream tasks
        context['task_instance'].xcom_push(key='ingestion_result', value=result)
    else:
        logging.warning("No claims data to ingest")

def process_payment_data(**context):
    """Process payment/denial data from 835 files"""
    pipeline = DataIngestionPipeline()
    
    # Process 835 files (remittance advice)
    payment_data = []
    
    # Check for 835 files in the data directory
    data_dir = "/data/payments"
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith('.835') or file.endswith('.txt'):
                file_path = os.path.join(data_dir, file)
                payments = pipeline.process_835_file(file_path)
                payment_data.extend(payments)
    
    # Update claims with payment information
    if payment_data:
        result = pipeline.update_payment_data(payment_data)
        logging.info(f"Updated {result['updated_count']} claims with payment data")
        
        # Push result to XCom
        context['task_instance'].xcom_push(key='payment_result', value=result)
    else:
        logging.info("No payment data to process")

def validate_data_quality(**context):
    """Validate data quality"""
    db = SessionLocal()
    try:
        # Check for duplicate claims
        duplicate_count = db.execute("""
            SELECT COUNT(*) as count FROM (
                SELECT claim_id, COUNT(*) 
                FROM claims 
                GROUP BY claim_id 
                HAVING COUNT(*) > 1
            ) duplicates
        """).fetchone().count
        
        if duplicate_count > 0:
            raise ValueError(f"Found {duplicate_count} duplicate claims")
        
        # Check for missing required fields
        missing_data = db.execute("""
            SELECT COUNT(*) as count 
            FROM claims 
            WHERE provider_id IS NULL 
            OR payer_id IS NULL 
            OR claim_amount IS NULL
        """).fetchone().count
        
        if missing_data > 0:
            logging.warning(f"Found {missing_data} claims with missing data")
        
        # Check for invalid claim amounts
        invalid_amounts = db.execute("""
            SELECT COUNT(*) as count 
            FROM claims 
            WHERE claim_amount <= 0
        """).fetchone().count
        
        if invalid_amounts > 0:
            logging.warning(f"Found {invalid_amounts} claims with invalid amounts")
        
        logging.info("Data quality validation passed")
        
        # Push validation results to XCom
        context['task_instance'].xcom_push(key='validation_result', value={
            'duplicate_count': duplicate_count,
            'missing_data_count': missing_data,
            'invalid_amounts_count': invalid_amounts
        })
        
    finally:
        db.close()

def update_features(**context):
    """Update feature store with latest data"""
    engineer = FeatureEngineer()
    
    db = SessionLocal()
    try:
        # Update provider features
        providers = db.query(Provider).all()
        for provider in providers:
            # Calculate updated features
            features = engineer._create_provider_features(db, provider.provider_id)
            provider.historical_denial_rate = features['provider_historical_denial_rate']
            provider.avg_claim_amount = features['provider_avg_claim_amount']
        
        # Update payer features
        payers = db.query(Payer).all()
        for payer in payers:
            features = engineer._create_payer_features(db, payer.payer_id)
            payer.denial_rate = features['payer_denial_rate']
            payer.avg_days_to_pay = features['payer_avg_days_to_pay']
        
        db.commit()
        logging.info(f"Updated features for {len(providers)} providers and {len(payers)} payers")
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating features: {e}")
        raise
    finally:
        db.close()

def retrain_model(**context):
    """Retrain the denial prediction model"""
    try:
        predictor = DenialPredictor()
        
        # Prepare training data
        X, y = predictor.prepare_training_data()
        
        # Train model
        metrics = predictor.train(X, y)
        
        logging.info(f"Model retraining completed. Test AUC: {metrics['test_auc']:.4f}")
        
        # Push metrics to XCom
        context['task_instance'].xcom_push(key='training_metrics', value=metrics)
        
        # Send notification if model performance is poor
        if metrics['test_auc'] < 0.7:
            context['task_instance'].xcom_push(key='model_alert', value={
                'message': f"Model performance below threshold: AUC = {metrics['test_auc']:.4f}",
                'severity': 'warning'
            })
        
    except Exception as e:
        logging.error(f"Error retraining model: {e}")
        raise

def generate_reports(**context):
    """Generate daily reports"""
    pipeline = DataIngestionPipeline()
    
    # Get ingestion statistics
    stats = pipeline.get_ingestion_stats()
    
    # Export claims to CSV for reporting
    report_date = datetime.now().strftime('%Y%m%d')
    export_path = f"/reports/claims_{report_date}.csv"
    
    # Ensure reports directory exists
    os.makedirs("/reports", exist_ok=True)
    
    # Export claims from last 30 days
    filters = {
        'start_date': datetime.now() - timedelta(days=30)
    }
    
    success = pipeline.export_claims_to_csv(export_path, filters)
    
    if success:
        logging.info(f"Generated report: {export_path}")
        context['task_instance'].xcom_push(key='report_path', value=export_path)
    else:
        logging.error("Failed to generate report")

def send_notifications(**context):
    """Send notifications based on pipeline results"""
    # Get results from previous tasks
    ingestion_result = context['task_instance'].xcom_pull(key='ingestion_result')
    validation_result = context['task_instance'].xcom_pull(key='validation_result')
    training_metrics = context['task_instance'].xcom_pull(key='training_metrics')
    model_alert = context['task_instance'].xcom_pull(key='model_alert')
    
    # Prepare notification message
    message = "Healthcare Claims Pipeline Summary:\n\n"
    
    if ingestion_result:
        message += f"📊 Claims Ingested: {ingestion_result['ingested_count']}\n"
        message += f"❌ Errors: {ingestion_result['error_count']}\n\n"
    
    if validation_result:
        message += f"🔍 Data Quality:\n"
        message += f"   - Duplicates: {validation_result['duplicate_count']}\n"
        message += f"   - Missing Data: {validation_result['missing_data_count']}\n"
        message += f"   - Invalid Amounts: {validation_result['invalid_amounts_count']}\n\n"
    
    if training_metrics:
        message += f"🤖 Model Performance:\n"
        message += f"   - Test AUC: {training_metrics['test_auc']:.4f}\n"
        message += f"   - Precision: {training_metrics['test_precision']:.4f}\n"
        message += f"   - Recall: {training_metrics['test_recall']:.4f}\n\n"
    
    if model_alert:
        message += f"⚠️ {model_alert['message']}\n"
    
    # Log the message (in production, would send to Slack/email)
    logging.info(f"Notification: {message}")
    
    # Push notification to XCom
    context['task_instance'].xcom_push(key='notification_message', value=message)

# Create the main DAG
claims_pipeline_dag = DAG(
    'healthcare_claims_pipeline',
    default_args=default_args,
    description='Healthcare claims data pipeline',
    schedule_interval='@daily',
    max_active_runs=1,
    tags=['healthcare', 'claims', 'data-pipeline']
)

# Define tasks
ingest_task = PythonOperator(
    task_id='ingest_claims_data',
    python_callable=ingest_claims_data,
    dag=claims_pipeline_dag
)

payment_task = PythonOperator(
    task_id='process_payment_data',
    python_callable=process_payment_data,
    dag=claims_pipeline_dag
)

validate_task = PythonOperator(
    task_id='validate_data_quality',
    python_callable=validate_data_quality,
    dag=claims_pipeline_dag
)

update_features_task = PythonOperator(
    task_id='update_features',
    python_callable=update_features,
    dag=claims_pipeline_dag
)

retrain_task = PythonOperator(
    task_id='retrain_model',
    python_callable=retrain_model,
    dag=claims_pipeline_dag
)

report_task = PythonOperator(
    task_id='generate_reports',
    python_callable=generate_reports,
    dag=claims_pipeline_dag
)

notify_task = PythonOperator(
    task_id='send_notifications',
    python_callable=send_notifications,
    dag=claims_pipeline_dag
)

# Define task dependencies
ingest_task >> payment_task >> validate_task >> update_features_task >> retrain_task
retrain_task >> report_task >> notify_task

# ============================================================================
# HOURLY STREAMING DAG
# ============================================================================

def process_streaming_events(**context):
    """Process real-time streaming events"""
    from data_pipeline.streaming_processor import StreamProcessor
    import redis
    
    # Initialize Redis client
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    
    # Initialize stream processor
    stream_processor = StreamProcessor(redis_client, batch_size=100)
    
    # Process any pending events
    current_hour = datetime.now().strftime('%Y%m%d_%H')
    batch_key = f"batch:{current_hour}"
    
    # Get all events in batch
    events = []
    while True:
        event_data = redis_client.rpop(batch_key)
        if not event_data:
            break
        events.append(json.loads(event_data))
    
    if events:
        # Process events
        for event_data in events:
            # Create StreamEvent object
            event = StreamEvent(
                event_type=event_data["event_type"],
                event_id=event_data["event_id"],
                timestamp=datetime.fromisoformat(event_data["timestamp"]),
                data=event_data["data"],
                source=event_data["source"],
                priority=event_data.get("priority", 1)
            )
            
            # Process event
            asyncio.run(stream_processor._process_single_event(event))
        
        logging.info(f"Processed {len(events)} streaming events")
    else:
        logging.info("No streaming events to process")

def update_realtime_metrics(**context):
    """Update real-time metrics"""
    import redis
    
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    
    # Get current metrics
    metrics = asyncio.run(stream_processor.get_realtime_metrics())
    
    # Store metrics for dashboard
    redis_client.setex(
        f"realtime_metrics:{datetime.now().strftime('%Y%m%d_%H')}",
        3600,  # 1 hour TTL
        json.dumps(metrics)
    )
    
    logging.info("Updated real-time metrics")

# Create streaming DAG
streaming_dag = DAG(
    'healthcare_streaming_pipeline',
    default_args=default_args,
    description='Real-time healthcare data streaming',
    schedule_interval='@hourly',
    max_active_runs=1,
    tags=['healthcare', 'streaming', 'real-time']
)

# Define streaming tasks
streaming_task = PythonOperator(
    task_id='process_streaming_events',
    python_callable=process_streaming_events,
    dag=streaming_dag
)

metrics_task = PythonOperator(
    task_id='update_realtime_metrics',
    python_callable=update_realtime_metrics,
    dag=streaming_dag
)

# Define streaming task dependencies
streaming_task >> metrics_task

# ============================================================================
# WEEKLY MODEL EVALUATION DAG
# ============================================================================

def evaluate_model_performance(**context):
    """Evaluate model performance on recent data"""
    from data_pipeline.advanced_analytics import AdvancedAnalytics
    
    analytics = AdvancedAnalytics()
    
    # Get prediction accuracy analysis
    accuracy_analysis = analytics.get_prediction_accuracy_analysis(days=7)
    
    # Check if model performance is degrading
    if 'accuracy_metrics' in accuracy_analysis:
        metrics = accuracy_analysis['accuracy_metrics']
        
        if metrics['accuracy'] < 0.8:
            context['task_instance'].xcom_push(key='performance_alert', value={
                'message': f"Model accuracy below threshold: {metrics['accuracy']:.4f}",
                'severity': 'critical'
            })
        
        logging.info(f"Model evaluation completed. Accuracy: {metrics['accuracy']:.4f}")
        
        # Push metrics to XCom
        context['task_instance'].xcom_push(key='evaluation_metrics', value=metrics)
    else:
        logging.warning("No evaluation metrics available")

def generate_weekly_report(**context):
    """Generate weekly analytics report"""
    from data_pipeline.advanced_analytics import AdvancedAnalytics
    
    analytics = AdvancedAnalytics()
    
    # Generate comprehensive report
    report = analytics.generate_insights_report(days=7)
    
    # Create visualizations
    charts = analytics.create_visualizations(report['analytics'])
    
    # Save report to file
    report_date = datetime.now().strftime('%Y%m%d')
    report_path = f"/reports/weekly_analytics_{report_date}.json"
    
    os.makedirs("/reports", exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    logging.info(f"Generated weekly report: {report_path}")
    context['task_instance'].xcom_push(key='weekly_report_path', value=report_path)

# Create weekly evaluation DAG
weekly_evaluation_dag = DAG(
    'healthcare_weekly_evaluation',
    default_args=default_args,
    description='Weekly model evaluation and reporting',
    schedule_interval='0 2 * * 1',  # Every Monday at 2 AM
    max_active_runs=1,
    tags=['healthcare', 'evaluation', 'reporting']
)

# Define evaluation tasks
evaluate_task = PythonOperator(
    task_id='evaluate_model_performance',
    python_callable=evaluate_model_performance,
    dag=weekly_evaluation_dag
)

weekly_report_task = PythonOperator(
    task_id='generate_weekly_report',
    python_callable=generate_weekly_report,
    dag=weekly_evaluation_dag
)

# Define evaluation task dependencies
evaluate_task >> weekly_report_task

# ============================================================================
# MONTHLY DATA CLEANUP DAG
# ============================================================================

def cleanup_old_data(**context):
    """Clean up old data and archive"""
    db = SessionLocal()
    try:
        # Archive claims older than 2 years
        cutoff_date = datetime.now() - timedelta(days=730)
        
        # Count old claims
        old_claims_count = db.query(Claim).filter(
            Claim.submission_date < cutoff_date
        ).count()
        
        if old_claims_count > 0:
            # Archive old claims (in production, would move to archive table)
            logging.info(f"Found {old_claims_count} claims older than 2 years")
            
            # For demo purposes, just log the count
            # In production, would move to archive table or delete
            
        # Clean up old predictions
        old_predictions_count = db.execute("""
            DELETE FROM predictions 
            WHERE prediction_timestamp < NOW() - INTERVAL '1 year'
        """).rowcount
        
        logging.info(f"Cleaned up {old_predictions_count} old predictions")
        
        context['task_instance'].xcom_push(key='cleanup_result', value={
            'old_claims_count': old_claims_count,
            'old_predictions_deleted': old_predictions_count
        })
        
    finally:
        db.close()

def optimize_database(**context):
    """Optimize database performance"""
    db = SessionLocal()
    try:
        # Update table statistics
        db.execute("ANALYZE claims")
        db.execute("ANALYZE predictions")
        db.execute("ANALYZE denial_records")
        
        # Vacuum tables (PostgreSQL)
        db.execute("VACUUM ANALYZE claims")
        db.execute("VACUUM ANALYZE predictions")
        db.execute("VACUUM ANALYZE denial_records")
        
        logging.info("Database optimization completed")
        
    finally:
        db.close()

# Create monthly cleanup DAG
cleanup_dag = DAG(
    'healthcare_monthly_cleanup',
    default_args=default_args,
    description='Monthly data cleanup and optimization',
    schedule_interval='0 3 1 * *',  # First day of month at 3 AM
    max_active_runs=1,
    tags=['healthcare', 'cleanup', 'maintenance']
)

# Define cleanup tasks
cleanup_task = PythonOperator(
    task_id='cleanup_old_data',
    python_callable=cleanup_old_data,
    dag=cleanup_dag
)

optimize_task = PythonOperator(
    task_id='optimize_database',
    python_callable=optimize_database,
    dag=cleanup_dag
)

# Define cleanup task dependencies
cleanup_task >> optimize_task 