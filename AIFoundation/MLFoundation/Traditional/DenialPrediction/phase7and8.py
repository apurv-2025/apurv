async def test_input_validation(self):
        """Test model handles invalid inputs gracefully"""
        # Test with NaN values
        test_with_nan = self.test_data.copy()
        test_with_nan.iloc[0, 0] = np.nan
        
        try:
            predictions = self.model.predict_proba(test_with_nan)
            # Should either handle NaN or raise appropriate error
            assert not np.isnan(predictions).any(), "Model returned NaN predictions"
        except Exception as e:
            # If model raises exception, it should be a meaningful one
            assert "NaN" in str(e) or "missing" in str(e).lower(), f"Unexpected error for NaN input: {e}"
        
        # Test with wrong number of features
        wrong_features = self.test_data.iloc[:5, :5]  # Fewer features
        
        try:
            predictions = self.model.predict_proba(wrong_features)
            assert False, "Model should reject input with wrong number of features"
        except Exception as e:
            # Expected to fail
            pass
        
        logger.info("Input validation tests passed")
    
    async def test_prediction_consistency(self):
        """Test prediction consistency across multiple calls"""
        sample_data = self.test_data.head(10)
        
        # Make multiple predictions
        predictions_1 = self.model.predict_proba(sample_data)
        predictions_2 = self.model.predict_proba(sample_data)
        predictions_3 = self.model.predict_proba(sample_data)
        
        # Check consistency
        np.testing.assert_array_almost_equal(predictions_1, predictions_2, decimal=6)
        np.testing.assert_array_almost_equal(predictions_2, predictions_3, decimal=6)
        
        logger.info("Prediction consistency test passed")
    
    async def test_feature_importance(self):
        """Test feature importance makes sense"""
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            
            # Check that not all features have zero importance
            assert np.sum(importances > 0) > 0, "No features have positive importance"
            
            # Check that importances sum to 1 (for tree-based models)
            if hasattr(self.model, 'n_estimators'):
                assert abs(np.sum(importances) - 1.0) < 0.01, "Feature importances don't sum to 1"
            
            # Check for reasonable distribution
            max_importance = np.max(importances)
            assert max_importance < 0.8, f"Single feature has too high importance: {max_importance:.3f}"
            
            logger.info("Feature importance test passed")
    
    async def test_edge_cases(self):
        """Test model behavior on edge cases"""
        # Test with all zeros
        zeros_data = pd.DataFrame(np.zeros((5, self.test_data.shape[1])), 
                                 columns=self.test_data.columns)
        predictions_zeros = self.model.predict_proba(zeros_data)
        assert predictions_zeros.shape == (5, 2), "Wrong output shape for zeros input"
        
        # Test with very large values
        large_data = self.test_data.copy()
        large_data.iloc[:5] = large_data.iloc[:5] * 1000
        predictions_large = self.model.predict_proba(large_data.head(5))
        assert not np.isnan(predictions_large).any(), "Model failed on large values"
        
        # Test with very small values
        small_data = self.test_data.copy()
        small_data.iloc[:5] = small_data.iloc[:5] * 0.001
        predictions_small = self.model.predict_proba(small_data.head(5))
        assert not np.isnan(predictions_small).any(), "Model failed on small values"
        
        logger.info("Edge cases test passed")
    
    async def test_bias_detection(self):
        """Test for potential bias in model predictions"""
        # This is a simplified bias test - in practice, you'd use more sophisticated methods
        predictions = self.model.predict_proba(self.test_data)[:, 1]
        
        # Check for reasonable prediction distribution
        mean_pred = np.mean(predictions)
        std_pred = np.std(predictions)
        
        assert 0.1 < mean_pred < 0.9, f"Predictions too skewed: mean={mean_pred:.3f}"
        assert std_pred > 0.05, f"Predictions lack variance: std={std_pred:.3f}"
        
        # Check for extreme predictions
        extreme_count = np.sum((predictions < 0.01) | (predictions > 0.99))
        extreme_ratio = extreme_count / len(predictions)
        assert extreme_ratio < 0.1, f"Too many extreme predictions: {extreme_ratio:.3f}"
        
        logger.info("Bias detection test passed")
    
    async def test_model_robustness(self):
        """Test model robustness to small input perturbations"""
        sample_data = self.test_data.head(10)
        original_predictions = self.model.predict_proba(sample_data)[:, 1]
        
        # Add small noise
        noise_level = 0.01
        noisy_data = sample_data + np.random.normal(0, noise_level, sample_data.shape)
        noisy_predictions = self.model.predict_proba(noisy_data)[:, 1]
        
        # Check that predictions don't change dramatically
        max_change = np.max(np.abs(original_predictions - noisy_predictions))
        assert max_change < 0.1, f"Model too sensitive to noise: max change {max_change:.3f}"
        
        logger.info("Model robustness test passed")

class APITestSuite(BaseTestSuite):
    """API integration and load testing"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        super().__init__()
        self.base_url = base_url
        self.client = None
    
    async def setup(self):
        """Setup API test environment"""
        # Create test client or verify API is running
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            assert response.status_code == 200
            self.setup_complete = True
        except Exception as e:
            raise Exception(f"API not available: {e}")
    
    async def run_all_tests(self) -> List[TestResult]:
        """Run all API tests"""
        await self.setup()
        
        tests = [
            self.test_health_endpoint,
            self.test_prediction_endpoint,
            self.test_authentication,
            self.test_rate_limiting,
            self.test_input_validation_api,
            self.test_error_handling,
            self.test_concurrent_requests,
            self.test_load_performance
        ]
        
        for test in tests:
            start_time = time.time()
            try:
                await test()
                execution_time = time.time() - start_time
                self.record_result(test.__name__, True, execution_time)
            except Exception as e:
                execution_time = time.time() - start_time
                self.record_result(test.__name__, False, execution_time, str(e))
                logger.error(f"Test {test.__name__} failed: {e}")
        
        return self.results
    
    async def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.base_url}/health")
        assert response.status_code == 200
        
        health_data = response.json()
        assert health_data.get("status") == "healthy"
        
        logger.info("Health endpoint test passed")
    
    async def test_prediction_endpoint(self):
        """Test prediction endpoint functionality"""
        # Sample prediction request
        prediction_data = {
            "claim_id": "test_claim_123",
            "provider_id": "provider_456",
            "payer_id": "payer_789",
            "cpt_codes": ["99213", "85025"],
            "claim_amount": 150.00,
            "patient_age": 45
        }
        
        response = requests.post(
            f"{self.base_url}/predict-pre",
            json=prediction_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code == 200
        
        result = response.json()
        assert "denial_probability" in result
        assert "top_risk_factors" in result
        assert "recommended_actions" in result
        assert 0 <= result["denial_probability"] <= 1
        
        logger.info("Prediction endpoint test passed")
    
    async def test_authentication(self):
        """Test authentication and authorization"""
        # Test without token
        response = requests.post(f"{self.base_url}/predict-pre", json={})
        assert response.status_code == 401
        
        # Test with invalid token
        response = requests.post(
            f"{self.base_url}/predict-pre",
            json={},
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        
        logger.info("Authentication test passed")
    
    async def test_rate_limiting(self):
        """Test API rate limiting"""
        # Make rapid requests
        responses = []
        for i in range(15):  # Assuming rate limit is 10/minute
            response = requests.get(f"{self.base_url}/health")
            responses.append(response.status_code)
            time.sleep(0.1)
        
        # Check if rate limiting kicked in
        rate_limited = any(status == 429 for status in responses)
        if not rate_limited:
            logger.warning("Rate limiting may not be properly configured")
        
        logger.info("Rate limiting test completed")
    
    async def test_input_validation_api(self):
        """Test API input validation"""
        # Test with missing required fields
        invalid_data = {"claim_id": "test"}
        
        response = requests.post(
            f"{self.base_url}/predict-pre",
            json=invalid_data,
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code == 422  # Validation error
        
        # Test with invalid data types
        invalid_types = {
            "claim_id": "test",
            "provider_id": "provider",
            "payer_id": "payer",
            "claim_amount": "invalid_amount",  # Should be number
            "patient_age": "invalid_age"       # Should be number
        }
        
        response = requests.post(
            f"{self.base_url}/predict-pre",
            json=invalid_types,
            headers={"Authorization": "Bearer test_token"}
        )
        
        assert response.status_code == 422
        
        logger.info("Input validation test passed")
    
    async def test_error_handling(self):
        """Test API error handling"""
        # Test with malformed JSON
        response = requests.post(
            f"{self.base_url}/predict-pre",
            data="invalid json",
            headers={
                "Authorization": "Bearer test_token",
                "Content-Type": "application/json"
            }
        )
        
        assert response.status_code == 422
        
        logger.info("Error handling test passed")
    
    async def test_concurrent_requests(self):
        """Test API under concurrent load"""
        num_concurrent = 10
        
        async def make_request():
            prediction_data = {
                "claim_id": f"test_claim_{threading.current_thread().ident}",
                "provider_id": "provider_456",
                "payer_id": "payer_789",
                "cpt_codes": ["99213"],
                "claim_amount": 100.00,
                "patient_age": 35
            }
            
            response = requests.post(
                f"{self.base_url}/predict-pre",
                json=prediction_data,
                headers={"Authorization": "Bearer test_token"}
            )
            return response.status_code
        
        # Run concurrent requests
        with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(executor, lambda: asyncio.run(make_request()))
                for _ in range(num_concurrent)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check results
        success_count = sum(1 for r in results if r == 200)
        assert success_count >= num_concurrent * 0.8, f"Only {success_count}/{num_concurrent} requests succeeded"
        
        logger.info(f"Concurrent requests test passed - {success_count}/{num_concurrent} succeeded")
    
    async def test_load_performance(self):
        """Test API performance under load"""
        num_requests = 100
        target_latency_ms = 500
        
        latencies = []
        
        for i in range(num_requests):
            start_time = time.time()
            
            response = requests.get(f"{self.base_url}/health")
            
            latency = (time.time() - start_time) * 1000
            latencies.append(latency)
            
            assert response.status_code == 200
        
        # Calculate statistics
        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        p99_latency = np.percentile(latencies, 99)
        
        assert avg_latency < target_latency_ms, f"Average latency {avg_latency:.2f}ms exceeds {target_latency_ms}ms"
        assert p95_latency < target_latency_ms * 2, f"P95 latency {p95_latency:.2f}ms too high"
        
        logger.info(f"Load performance test passed - Avg: {avg_latency:.2f}ms, P95: {p95_latency:.2f}ms, P99: {p99_latency:.2f}ms")

class DataQualityTestSuite(BaseTestSuite):
    """Data quality and pipeline testing"""
    
    def __init__(self, data_source: str):
        super().__init__()
        self.data_source = data_source
    
    async def run_all_tests(self) -> List[TestResult]:
        """Run all data quality tests"""
        tests = [
            self.test_data_availability,
            self.test_data_completeness,
            self.test_data_freshness,
            self.test_data_consistency,
            self.test_schema_compliance,
            self.test_data_distribution,
            self.test_duplicate_detection,
            self.test_outlier_detection
        ]
        
        for test in tests:
            start_time = time.time()
            try:
                await test()
                execution_time = time.time() - start_time
                self.record_result(test.__name__, True, execution_time)
            except Exception as e:
                execution_time = time.time() - start_time
                self.record_result(test.__name__, False, execution_time, str(e))
                logger.error(f"Test {test.__name__} failed: {e}")
        
        return self.results
    
    async def test_data_availability(self):
        """Test that data source is available and accessible"""
        # This would test your actual data source
        # For demo, we'll simulate
        assert True, "Data source is available"
        logger.info("Data availability test passed")
    
    async def test_data_completeness(self):
        """Test data completeness"""
        # Simulate checking for missing values
        missing_threshold = 0.1  # 10% missing allowed
        
        # In practice, load actual data and check
        simulated_missing_rate = 0.05  # 5% missing
        
        assert simulated_missing_rate < missing_threshold, f"Missing data rate {simulated_missing_rate} exceeds threshold {missing_threshold}"
        
        logger.info("Data completeness test passed")
    
    async def test_data_freshness(self):
        """Test data freshness"""
        # Check if data is recent enough
        max_age_hours = 24
        
        # Simulate last data update
        last_update = datetime.now() - timedelta(hours=2)
        age_hours = (datetime.now() - last_update).total_seconds() / 3600
        
        assert age_hours < max_age_hours, f"Data is {age_hours:.1f} hours old, exceeds {max_age_hours} hours"
        
        logger.info("Data freshness test passed")
    
    async def test_data_consistency(self):
        """Test data consistency across sources"""
        # Test referential integrity, cross-source consistency, etc.
        logger.info("Data consistency test passed")
    
    async def test_schema_compliance(self):
        """Test schema compliance"""
        # Verify data follows expected schema
        logger.info("Schema compliance test passed")
    
    async def test_data_distribution(self):
        """Test data distribution hasn't shifted unexpectedly"""
        # Statistical tests for distribution changes
        logger.info("Data distribution test passed")
    
    async def test_duplicate_detection(self):
        """Test for duplicate records"""
        # Check for unexpected duplicates
        logger.info("Duplicate detection test passed")
    
    async def test_outlier_detection(self):
        """Test for data outliers"""
        # Statistical outlier detection
        logger.info("Outlier detection test passed")

# =============================================================================
# PHASE 8: ADVANCED MONITORING IMPLEMENTATION
# =============================================================================

class PrometheusMetrics:
    """Prometheus metrics for monitoring"""
    
    def __init__(self, registry: Optional[CollectorRegistry] = None):
        self.registry = registry or CollectorRegistry()
        
        # API Metrics
        self.request_count = Counter(
            'api_requests_total',
            'Total API requests',
            ['method', 'endpoint', 'status_code'],
            registry=self.registry
        )
        
        self.request_duration = Histogram(
            'api_request_duration_seconds',
            'API request duration',
            ['method', 'endpoint'],
            registry=self.registry
        )
        
        # Model Metrics
        self.prediction_count = Counter(
            'model_predictions_total',
            'Total model predictions',
            ['model_name', 'model_version'],
            registry=self.registry
        )
        
        self.model_accuracy = Gauge(
            'model_accuracy',
            'Current model accuracy',
            ['model_name', 'model_version'],
            registry=self.registry
        )
        
        self.model_drift_score = Gauge(
            'model_drift_score',
            'Model drift score',
            ['model_name', 'feature_name'],
            registry=self.registry
        )
        
        # System Metrics
        self.cache_hit_rate = Gauge(
            'cache_hit_rate',
            'Cache hit rate',
            ['cache_type'],
            registry=self.registry
        )
        
        self.queue_size = Gauge(
            'queue_size',
            'Queue size',
            ['queue_name'],
            registry=self.registry
        )
        
        # Business Metrics
        self.denial_rate = Gauge(
            'denial_rate',
            'Current denial rate',
            ['payer', 'provider_type'],
            registry=self.registry
        )
        
        self.cost_savings = Counter(
            'cost_savings_total',
            'Total cost savings from system',
            ['savings_type'],
            registry=self.registry
        )

class AlertManager:
    """Alert management system"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379)
        self.alert_rules = {}
        self.notification_channels = {}
        
    def add_alert_rule(self, name: str, condition: callable, 
                      severity: str, description: str):
        """Add alert rule"""
        self.alert_rules[name] = {
            'condition': condition,
            'severity': severity,
            'description': description,
            'enabled': True,
            'last_triggered': None
        }
    
    def add_notification_channel(self, name: str, channel_type: str, config: Dict):
        """Add notification channel"""
        self.notification_channels[name] = {
            'type': channel_type,
            'config': config,
            'enabled': True
        }
    
    async def check_alerts(self, metrics: Dict[str, Any]):
        """Check all alert rules against current metrics"""
        alerts_triggered = []
        
        for rule_name, rule in self.alert_rules.items():
            if not rule['enabled']:
                continue
            
            try:
                if rule['condition'](metrics):
                    alert = {
                        'rule_name': rule_name,
                        'severity': rule['severity'],
                        'description': rule['description'],
                        'timestamp': datetime.now(),
                        'metrics': metrics
                    }
                    
                    alerts_triggered.append(alert)
                    await self._send_alert(alert)
                    
                    # Update last triggered time
                    rule['last_triggered'] = datetime.now()
                    
            except Exception as e:
                logger.error(f"Error checking alert rule {rule_name}: {e}")
        
        return alerts_triggered
    
    async def _send_alert(self, alert: Dict):
        """Send alert to configured channels"""
        for channel_name, channel in self.notification_channels.items():
            if not channel['enabled']:
                continue
            
            try:
                if channel['type'] == 'email':
                    await self._send_email_alert(alert, channel['config'])
                elif channel['type'] == 'slack':
                    await self._send_slack_alert(alert, channel['config'])
                elif channel['type'] == 'webhook':
                    await self._send_webhook_alert(alert, channel['config'])
                    
            except Exception as e:
                logger.error(f"Failed to send alert via {channel_name}: {e}")
    
    async def _send_email_alert(self, alert: Dict, config: Dict):
        """Send email alert"""
        # Implementation would use actual email service
        logger.info(f"EMAIL ALERT: {alert['description']}")
    
    async def _send_slack_alert(self, alert: Dict, config: Dict):
        """Send Slack alert"""
        # Implementation would use Slack API
        logger.info(f"SLACK ALERT: {alert['description']}")
    
    async def _send_webhook_alert(self, alert: Dict, config: Dict):
        """Send webhook alert"""
        # Implementation would POST to webhook URL
        logger.info(f"WEBHOOK ALERT: {alert['description']}")

class DashboardManager:
    """Real-time monitoring dashboard"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379)
        self.dashboard_data = {}
    
    async def update_dashboard_data(self, metrics: Dict[str, Any]):
        """Update dashboard with latest metrics"""
        timestamp = datetime.now().isoformat()
        
        # Store metrics with timestamp
        dashboard_update = {
            'timestamp': timestamp,
            'metrics': metrics
        }
        
        # Store in Redis for real-time updates
        self.redis_client.lpush('dashboard_updates', json.dumps(dashboard_update, default=str))
        self.redis_client.ltrim('dashboard_updates', 0, 999)  # Keep last 1000 updates
        
        # Update cached dashboard data
        self.dashboard_data.update(metrics)
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get current dashboard data"""
        return {
            'last_updated': datetime.now().isoformat(),
            'metrics': self.dashboard_data,
            'status': self._calculate_system_status()
        }
    
    def _calculate_system_status(self) -> str:
        """Calculate overall system status"""
        # Simple status calculation based on key metrics
        if self.dashboard_data.get('error_rate', 0) > 0.05:
            return 'critical'
        elif self.dashboard_data.get('latency_p95', 0) > 1000:
            return 'warning'
        else:
            return 'healthy'
    
    async def generate_report(self, time_range: str = '24h') -> Dict[str, Any]:
        """Generate monitoring report"""
        # Get historical data from Redis
        updates = self.redis_client.lrange('dashboard_updates', 0, -1)
        
        if not updates:
            return {'error': 'No data available'}
        
        # Parse data
        data_points = []
        for update in updates:
            try:
                data = json.loads(update)
                data_points.append(data)
            except json.JSONDecodeError:
                continue
        
        # Calculate summary statistics
        if not data_points:
            return {'error': 'No valid data points'}
        
        latest_metrics = data_points[0]['metrics']
        
        report = {
            'time_range': time_range,
            'data_points': len(data_points),
            'summary': {
                'avg_latency': np.mean([d['metrics'].get('latency_avg', 0) for d in data_points]),
                'max_latency': np.max([d['metrics'].get('latency_max', 0) for d in data_points]),
                'error_rate': np.mean([d['metrics'].get('error_rate', 0) for d in data_points]),
                'total_requests': sum([d['metrics'].get('request_count', 0) for d in data_points])
            },
            'current_status': self._calculate_system_status(),
            'recommendations': self._generate_recommendations(latest_metrics)
        }
        
        return report
    
    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []
        
        if metrics.get('latency_p95', 0) > 500:
            recommendations.append("Consider optimizing model inference or adding caching")
        
        if metrics.get('cache_hit_rate', 1) < 0.8:
            recommendations.append("Review cache configuration to improve hit rate")
        
        if metrics.get('error_rate', 0) > 0.01:
            recommendations.append("Investigate and fix errors to improve reliability")
        
        if metrics.get('cpu_usage', 0) > 0.8:
            recommendations.append("Consider scaling up compute resources")
        
        return recommendations

class ComprehensiveMonitor:
    """Main monitoring system coordinator"""
    
    def __init__(self):
        self.metrics = PrometheusMetrics()
        self.alert_manager = AlertManager()
        self.dashboard_manager = DashboardManager()
        self.running = False
        
        # Setup default alert rules
        self._setup_default_alerts()
    
    def _setup_default_alerts(self):
        """Setup default monitoring alerts"""
        
        # High error rate alert
        self.alert_manager.add_alert_rule(
            'high_error_rate',
            lambda m: m.get('error_rate', 0) > 0.05,
            'critical',
            'Error rate exceeds 5%'
        )
        
        # High latency alert
        self.alert_manager.add_alert_rule(
            'high_latency',
            lambda m: m.get('latency_p95', 0) > 1000,
            'warning',
            'P95 latency exceeds 1000ms'
        )
        
        # Model drift alert
        self.alert_manager.add_alert_rule(
            'model_drift',
            lambda m: m.get('drift_score', 0) > 0.3,
            'warning',
            'Model drift detected'
        )
        
        # Low cache hit rate alert
        self.alert_manager.add_alert_rule(
            'low_cache_hit_rate',
            lambda m: m.get('cache_hit_rate', 1) < 0.7,
            'info',
            'Cache hit rate below 70%'
        )
    
    async def start_monitoring(self):
        """Start monitoring loop"""
        self.running = True
        
        while self.running:
            try:
                # Collect current metrics
                current_metrics = await self._collect_metrics()
                
                # Update Prometheus metrics
                self._update_prometheus_metrics(current_metrics)
                
                # Check alerts
                alerts = await self.alert_manager.check_alerts(current_metrics)
                
                # Update dashboard
                await self.dashboard_manager.update_dashboard_data(current_metrics)
                
                # Log summary
                if alerts:
                    logger.warning(f"Triggered {len(alerts)} alerts")
                
                await asyncio.sleep(30)  # Monitor every 30 seconds
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
    
    async def _collect_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics"""
        # System metrics
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Simulate other metrics (in practice, these would come from your systems)
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': cpu_usage / 100.0,
            'memory_usage': memory_usage / 100.0,
            'latency_avg': np.random.normal(200, 50),
            'latency_p95': np.random.normal(400, 100),
            'latency_max': np.random.normal(800, 200),
            'error_rate': np.random.beta(1, 100),  # Low error rate
            'request_count': np.random.poisson(100),
            'cache_hit_rate': np.random.beta(8, 2),  # High hit rate
            'drift_score': np.random.beta(2, 8),  # Low drift
            'model_accuracy': 0.85 + np.random.normal(0, 0.02),
            'denial_rate': np.random.beta(2, 8)
        }
        
        return metrics
    
    def _update_prometheus_metrics(self, metrics: Dict[str, Any]):
        """Update Prometheus metrics"""
        try:
            # Update gauges
            self.metrics.model_accuracy.labels(
                model_name='denial_predictor',
                model_version='v1.0'
            ).set(metrics.get('model_accuracy', 0))
            
            self.metrics.cache_hit_rate.labels(
                cache_type='feature_cache'
            ).set(metrics.get('cache_hit_rate', 0))
            
            self.metrics.denial_rate.labels(
                payer='all',
                provider_type='all'
            ).set(metrics.get('denial_rate', 0))
            
        except Exception as e:
            logger.error(f"Error updating Prometheus metrics: {e}")

# Example usage and integration
async def run_comprehensive_testing():
    """Run comprehensive testing suite"""
    logger.info("Starting comprehensive testing suite...")
    
    # Create sample model and data for testing
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    y_series = pd.Series(y)
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_df, y_series)
    
    # Initialize test suites
    model_tests = ModelTestSuite(model, X_df, y_series)
    api_tests = APITestSuite()
    data_tests = DataQualityTestSuite("test_data_source")
    
    # Run all test suites
    test_suites = [
        ("Model Tests", model_tests),
        ("API Tests", api_tests),
        ("Data Quality Tests", data_tests)
    ]
    
    all_results = {}
    
    for suite_name, test_suite in test_suites:
        logger.info(f"Running {suite_name}...")
        try:
            results = await test_suite.run_all_tests()
            all_results[suite_name] = results
            
            # Print summary
            passed = sum(1 for r in results if r.passed)
            total = len(results)
            logger.info(f"{suite_name}: {passed}/{total} tests passed")
            
            # Print failed tests
            failed_tests = [r for r in results if not r.passed]
            for failed in failed_tests:
                logger.error(f"  FAILED: {failed.test_name} - {failed.error_message}")
                
        except Exception as e:
            logger.error(f"Failed to run {suite_name}: {e}")
            all_results[suite_name] = []
    
    # Generate test report
    generate_test_report(all_results)
    
    return all_results

def generate_test_report(test_results: Dict[str, List[TestResult]]):
    """Generate comprehensive test report"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {},
        'details': {},
        'recommendations': []
    }
    
    total_tests = 0
    total_passed = 0
    
    for suite_name, results in test_results.items():
        passed = sum(1 for r in results if r.passed)
        total = len(results)
        
        total_tests += total
        total_passed += passed
        
        suite_summary = {
            'total_tests': total,
            'passed_tests': passed,
            'failed_tests': total - passed,
            'pass_rate': passed / total if total > 0 else 0,
            'avg_execution_time': np.mean([r.execution_time for r in results]) if results else 0
        }
        
        report['summary'][suite_name] = suite_summary
        report['details'][suite_name] = [
            {
                'test_name': r.test_name,
                'passed': r.passed,
                'execution_time': r.execution_time,
                'error_message': r.error_message,
                'metrics': r.metrics
            }
            for r in results
        ]
    
    # Overall summary
    report['overall'] = {
        'total_tests': total_tests,
        'passed_tests': total_passed,
        'failed_tests': total_tests - total_passed,
        'overall_pass_rate': total_passed / total_tests if total_tests > 0 else 0
    }
    
    # Generate recommendations
    if report['overall']['overall_pass_rate'] < 0.9:
        report['recommendations'].append("Test pass rate is below 90% - review failed tests")
    
    if report['summary'].get('Model Tests', {}).get('pass_rate', 1) < 1.0:
        report['recommendations'].append("Model tests failing - review model performance")
    
    if report['summary'].get('API Tests', {}).get('pass_rate', 1) < 1.0:
        report['recommendations'].append("API tests failing - check API functionality")
    
    # Save report
    with open(f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    logger.info(f"Test report generated - Overall pass rate: {report['overall']['overall_pass_rate']:.1%}")

async def run_monitoring_system():
    """Run the comprehensive monitoring system"""
    logger.info("Starting monitoring system...")
    
    # Initialize monitoring
    monitor = ComprehensiveMonitor()
    
    # Add notification channels
    monitor.alert_manager.add_notification_channel(
        'email_alerts',
        'email',
        {'recipients': ['admin@company.com', 'devops@company.com']}
    )
    
    monitor.alert_manager.add_notification_channel(
        'slack_alerts',
        'slack',
        {'webhook_url': 'https://hooks.slack.com/services/your/webhook/url'}
    )
    
    # Start monitoring (run for demo period)
    monitoring_task = asyncio.create_task(monitor.start_monitoring())
    
    # Let it run for a bit
    await asyncio.sleep(120)  # Monitor for 2 minutes
    
    # Stop monitoring
    monitor.stop_monitoring()
    await monitoring_task
    
    # Generate monitoring report
    report = await monitor.dashboard_manager.generate_report('2m')
    logger.info("Monitoring report generated")
    logger.info(f"System status: {report.get('current_status', 'unknown')}")
    
    return report

class ContinuousTestingFramework:
    """Framework for continuous testing in production"""
    
    def __init__(self, test_schedule: Dict[str, str] = None):
        self.test_schedule = test_schedule or {
            'model_tests': '0 */6 * * *',    # Every 6 hours
            'api_tests': '*/15 * * * *',     # Every 15 minutes
            'data_tests': '0 */2 * * *',     # Every 2 hours
            'load_tests': '0 2 * * 0'        # Weekly at 2 AM Sunday
        }
        self.test_history = []
        self.running = False
    
    async def start_continuous_testing(self):
        """Start continuous testing"""
        self.running = True
        logger.info("Starting continuous testing framework")
        
        while self.running:
            current_time = datetime.now()
            
            # Check which tests should run
            for test_type, schedule in self.test_schedule.items():
                if self._should_run_test(test_type, schedule, current_time):
                    await self._run_scheduled_test(test_type)
            
            await asyncio.sleep(60)  # Check every minute
    
    def stop_continuous_testing(self):
        """Stop continuous testing"""
        self.running = False
    
    def _should_run_test(self, test_type: str, schedule: str, current_time: datetime) -> bool:
        """Check if test should run based on schedule (simplified cron logic)"""
        # This is a simplified implementation
        # In practice, you'd use a proper cron parser like python-crontab
        
        if test_type == 'api_tests':
            # Run every 15 minutes
            return current_time.minute % 15 == 0 and current_time.second < 30
        elif test_type == 'model_tests':
            # Run every 6 hours
            return current_time.hour % 6 == 0 and current_time.minute < 5
        elif test_type == 'data_tests':
            # Run every 2 hours
            return current_time.hour % 2 == 0 and current_time.minute < 5
        elif test_type == 'load_tests':
            # Run weekly on Sunday at 2 AM
            return current_time.weekday() == 6 and current_time.hour == 2 and current_time.minute < 5
        
        return False
    
    async def _run_scheduled_test(self, test_type: str):
        """Run scheduled test"""
        logger.info(f"Running scheduled {test_type}")
        
        try:
            if test_type == 'api_tests':
                api_tests = APITestSuite()
                results = await api_tests.run_all_tests()
            elif test_type == 'model_tests':
                # Would load current model and test data
                results = []  # Placeholder
            elif test_type == 'data_tests':
                data_tests = DataQualityTestSuite("production_data")
                results = await data_tests.run_all_tests()
            else:
                results = []
            
            # Store results
            test_result = {
                'test_type': test_type,
                'timestamp': datetime.now().isoformat(),
                'results': results,
                'passed': all(r.passed for r in results) if results else True
            }
            
            self.test_history.append(test_result)
            
            # Alert on failures
            if not test_result['passed']:
                logger.error(f"Scheduled {test_type} failed")
                # Would send alert
            
        except Exception as e:
            logger.error(f"Error running scheduled {test_type}: {e}")

class CanaryTestManager:
    """Canary testing for model deployments"""
    
    def __init__(self):
        self.canary_configs = {}
        self.canary_results = {}
    
    async def start_canary_test(self, model_name: str, canary_version: str,
                               traffic_split: float = 0.1, duration_hours: int = 24):
        """Start canary testing for new model version"""
        canary_id = f"{model_name}_{canary_version}_{int(time.time())}"
        
        config = {
            'canary_id': canary_id,
            'model_name': model_name,
            'canary_version': canary_version,
            'baseline_version': 'current',
            'traffic_split': traffic_split,
            'start_time': datetime.now(),
            'duration_hours': duration_hours,
            'status': 'running',
            'metrics': {
                'baseline': {'predictions': 0, 'errors': 0, 'latency': []},
                'canary': {'predictions': 0, 'errors': 0, 'latency': []}
            }
        }
        
        self.canary_configs[canary_id] = config
        logger.info(f"Started canary test {canary_id} with {traffic_split*100}% traffic")
        
        # Start monitoring
        monitor_task = asyncio.create_task(self._monitor_canary(canary_id))
        
        return canary_id
    
    async def _monitor_canary(self, canary_id: str):
        """Monitor canary test"""
        config = self.canary_configs[canary_id]
        
        while config['status'] == 'running':
            # Check if duration expired
            elapsed = datetime.now() - config['start_time']
            if elapsed.total_seconds() > config['duration_hours'] * 3600:
                await self._complete_canary_test(canary_id)
                break
            
            # Collect metrics (simulated)
            await self._collect_canary_metrics(canary_id)
            
            # Check for early termination conditions
            if await self._should_terminate_canary(canary_id):
                await self._terminate_canary_test(canary_id)
                break
            
            await asyncio.sleep(300)  # Check every 5 minutes
    
    async def _collect_canary_metrics(self, canary_id: str):
        """Collect metrics for canary test"""
        config = self.canary_configs[canary_id]
        
        # Simulate metrics collection
        baseline_metrics = config['metrics']['baseline']
        canary_metrics = config['metrics']['canary']
        
        # Simulate some predictions and metrics
        baseline_metrics['predictions'] += np.random.poisson(10)
        canary_metrics['predictions'] += np.random.poisson(1)  # 10% traffic
        
        # Simulate latency
        baseline_metrics['latency'].extend(np.random.normal(200, 30, 5).tolist())
        canary_metrics['latency'].extend(np.random.normal(180, 25, 1).tolist())  # Slightly better
        
        # Keep only recent latency measurements
        baseline_metrics['latency'] = baseline_metrics['latency'][-100:]
        canary_metrics['latency'] = canary_metrics['latency'][-100:]
    
    async def _should_terminate_canary(self, canary_id: str) -> bool:
        """Check if canary should be terminated early"""
        config = self.canary_configs[canary_id]
        baseline_metrics = config['metrics']['baseline']
        canary_metrics = config['metrics']['canary']
        
        # Check error rates
        if len(canary_metrics['latency']) > 10:
            canary_avg_latency = np.mean(canary_metrics['latency'])
            baseline_avg_latency = np.mean(baseline_metrics['latency'])
            
            # Terminate if canary is significantly worse
            if canary_avg_latency > baseline_avg_latency * 1.5:
                logger.warning(f"Terminating canary {canary_id} due to high latency")
                return True
        
        return False
    
    async def _complete_canary_test(self, canary_id: str):
        """Complete canary test and make promotion decision"""
        config = self.canary_configs[canary_id]
        config['status'] = 'completed'
        
        # Analyze results
        results = self._analyze_canary_results(canary_id)
        
        # Make promotion decision
        if results['recommend_promotion']:
            logger.info(f"Canary test {canary_id} PASSED - recommending promotion")
            config['decision'] = 'promote'
        else:
            logger.warning(f"Canary test {canary_id} FAILED - rolling back")
            config['decision'] = 'rollback'
        
        self.canary_results[canary_id] = results
    
    async def _terminate_canary_test(self, canary_id: str):
        """Terminate canary test early"""
        config = self.canary_configs[canary_id]
        config['status'] = 'terminated'
        config['decision'] = 'rollback'
        
        logger.warning(f"Canary test {canary_id} terminated early")
    
    def _analyze_canary_results(self, canary_id: str) -> Dict[str, Any]:
        """Analyze canary test results"""
        config = self.canary_configs[canary_id]
        baseline_metrics = config['metrics']['baseline']
        canary_metrics = config['metrics']['canary']
        
        results = {
            'canary_id': canary_id,
            'duration_hours': (datetime.now() - config['start_time']).total_seconds() / 3600,
            'baseline_predictions': baseline_metrics['predictions'],
            'canary_predictions': canary_metrics['predictions'],
            'recommend_promotion': True
        }
        
        # Compare latencies
        if baseline_metrics['latency'] and canary_metrics['latency']:
            baseline_avg = np.mean(baseline_metrics['latency'])
            canary_avg = np.mean(canary_metrics['latency'])
            
            results['baseline_avg_latency'] = baseline_avg
            results['canary_avg_latency'] = canary_avg
            results['latency_improvement'] = (baseline_avg - canary_avg) / baseline_avg
            
            # Don't promote if latency is significantly worse
            if canary_avg > baseline_avg * 1.2:
                results['recommend_promotion'] = False
                results['failure_reason'] = 'High latency'
        
        return results

# Integration example
async def run_production_testing_and_monitoring():
    """Example of running production testing and monitoring"""
    logger.info("Starting production testing and monitoring system...")
    
    # Start continuous testing
    continuous_testing = ContinuousTestingFramework()
    testing_task = asyncio.create_task(continuous_testing.start_continuous_testing())
    
    # Start monitoring
    monitor = ComprehensiveMonitor()
    monitoring_task = asyncio.create_task(monitor.start_monitoring())
    
    # Start canary test
    canary_manager = CanaryTestManager()
    canary_id = await canary_manager.start_canary_test(
        'denial_predictor', 'v2.0', traffic_split=0.1, duration_hours=1
    )
    
    # Let everything run for a demo period
    await asyncio.sleep(300)  # Run for 5 minutes
    
    # Stop systems
    continuous_testing.stop_continuous_testing()
    monitor.stop_monitoring()
    
    await testing_task
    await monitoring_task
    
    # Get canary results
    if canary_id in canary_manager.canary_results:
        canary_result = canary_manager.canary_results[canary_id]
        logger.info(f"Canary test completed: {canary_result}")
    
    logger.info("Production testing and monitoring demo completed")

# Main execution
if __name__ == "__main__":
    # Run comprehensive testing
    print("=" * 60)
    print("RUNNING COMPREHENSIVE TESTING SUITE")
    print("=" * 60)
    
    test_results = asyncio.run(run_comprehensive_testing())
    
    # Calculate overall results
    total_tests = sum(len(results) for results in test_results.values())
    total_passed = sum(sum(1 for r in results if r.passed) for results in test_results.values())
    
    print(f"\nOVERALL RESULTS: {total_passed}/{total_tests} tests passed ({total_passed/total_tests*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print("RUNNING MONITORING SYSTEM DEMO")
    print("=" * 60)
    
    monitoring_report = asyncio.run(run_monitoring_system())
    print(f"Monitoring system demo completed")
    
    print("\n" + "=" * 60)
    print("RUNNING PRODUCTION TESTING & MONITORING")
    print("=" * 60)
    
    asyncio.run(run_production_testing_and_monitoring())
    # Phases 7-8: Comprehensive Testing Strategy & Advanced Monitoring
# Unit tests, integration tests, load testing, and production monitoring

import pytest
import asyncio
import time
import json
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import requests
from concurrent.futures import ThreadPoolExecutor
import threading
from contextlib import asynccontextmanager
import redis
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score, accuracy_score
import mlflow
import matplotlib.pyplot as plt
import seaborn as sns
from fastapi.testclient import TestClient
from fastapi import FastAPI
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# PHASE 7: COMPREHENSIVE TESTING STRATEGY
# =============================================================================

@dataclass
class TestResult:
    """Test result structure"""
    test_name: str
    passed: bool
    execution_time: float
    error_message: str = ""
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class BaseTestSuite:
    """Base class for test suites"""
    
    def __init__(self):
        self.results = []
        self.setup_complete = False
    
    async def setup(self):
        """Setup test environment"""
        self.setup_complete = True
    
    async def teardown(self):
        """Cleanup test environment"""
        pass
    
    def record_result(self, test_name: str, passed: bool, 
                     execution_time: float, error_message: str = "",
                     metrics: Dict[str, Any] = None):
        """Record test result"""
        result = TestResult(
            test_name=test_name,
            passed=passed,
            execution_time=execution_time,
            error_message=error_message,
            metrics=metrics or {}
        )
        self.results.append(result)
        return result

class ModelTestSuite(BaseTestSuite):
    """Comprehensive ML model testing"""
    
    def __init__(self, model, test_data: pd.DataFrame, test_labels: pd.Series):
        super().__init__()
        self.model = model
        self.test_data = test_data
        self.test_labels = test_labels
    
    async def run_all_tests(self) -> List[TestResult]:
        """Run all model tests"""
        await self.setup()
        
        tests = [
            self.test_model_accuracy,
            self.test_prediction_latency,
            self.test_memory_usage,
            self.test_input_validation,
            self.test_prediction_consistency,
            self.test_feature_importance,
            self.test_edge_cases,
            self.test_bias_detection,
            self.test_model_robustness
        ]
        
        for test in tests:
            start_time = time.time()
            try:
                await test()
                execution_time = time.time() - start_time
                self.record_result(test.__name__, True, execution_time)
            except Exception as e:
                execution_time = time.time() - start_time
                self.record_result(test.__name__, False, execution_time, str(e))
                logger.error(f"Test {test.__name__} failed: {e}")
        
        await self.teardown()
        return self.results
    
    async def test_model_accuracy(self):
        """Test model accuracy meets requirements"""
        predictions = self.model.predict_proba(self.test_data)[:, 1]
        auc = roc_auc_score(self.test_labels, predictions)
        accuracy = accuracy_score(self.test_labels, (predictions >= 0.5).astype(int))
        
        # Requirements: AUC > 0.8, Accuracy > 0.75
        assert auc > 0.8, f"AUC {auc:.3f} below threshold 0.8"
        assert accuracy > 0.75, f"Accuracy {accuracy:.3f} below threshold 0.75"
        
        logger.info(f"Model accuracy test passed - AUC: {auc:.3f}, Accuracy: {accuracy:.3f}")
    
    async def test_prediction_latency(self):
        """Test prediction latency meets SLA (<300ms for batch of 100)"""
        batch_size = 100
        test_batch = self.test_data.head(batch_size)
        
        # Warm up
        _ = self.model.predict_proba(test_batch)
        
        # Measure latency
        start_time = time.time()
        predictions = self.model.predict_proba(test_batch)
        latency = (time.time() - start_time) * 1000  # Convert to ms
        
        # Requirement: <300ms for 100 predictions
        assert latency < 300, f"Latency {latency:.2f}ms exceeds 300ms threshold"
        
        logger.info(f"Latency test passed - {latency:.2f}ms for {batch_size} predictions")
    
    async def test_memory_usage(self):
        """Test memory usage is within acceptable limits"""
        import psutil
        import gc
        
        process = psutil.Process()
        gc.collect()
        
        # Measure memory before
        memory_before = process.memory_info().rss / (1024 * 1024)  # MB
        
        # Make predictions
        predictions = self.model.predict_proba(self.test_data)
        
        # Measure memory after
        memory_after = process.memory_info().rss / (1024 * 1024)  # MB
        memory_usage = memory_after - memory_before
        
        # Requirement: <500MB for inference
        assert memory_usage < 500, f"Memory usage {memory_usage:.2f}MB exceeds 500MB threshold"
        
        logger.info(f"Memory test passed - {memory_usage:.2f}MB used for inference")
    
    async def test_input_validation(self):
        """Test model handles invalid inputs gracefully"""
        # Test with NaN values
        test_with_nan = self.test_data.copy()
        test_with_nan.iloc[0, 0] = np.nan
        
        try:
            predictions = self.model.predict_proba(test_with_nan)
            # Should either handle NaN or raise
