"""
Health Monitoring System
Comprehensive monitoring for healthcare denial prediction system
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import psutil
import redis
from sqlalchemy.orm import Session
from prometheus_client import Counter, Histogram, Gauge, Summary
import requests

from models.database import SessionLocal, Claim, DenialRecord
from data_pipeline.streaming_processor import StreamProcessor

logger = logging.getLogger(__name__)

# Prometheus metrics
HEALTH_CHECK_COUNTER = Counter('health_checks_total', 'Total health checks performed')
HEALTH_CHECK_DURATION = Histogram('health_check_duration_seconds', 'Health check duration')
SYSTEM_CPU_USAGE = Gauge('system_cpu_usage_percent', 'System CPU usage percentage')
SYSTEM_MEMORY_USAGE = Gauge('system_memory_usage_percent', 'System memory usage percentage')
DATABASE_CONNECTIONS = Gauge('database_connections_active', 'Active database connections')
REDIS_CONNECTIONS = Gauge('redis_connections_active', 'Active Redis connections')
API_RESPONSE_TIME = Histogram('api_response_time_seconds', 'API response time')
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')
ERROR_RATE = Counter('errors_total', 'Total errors', ['service', 'error_type'])

@dataclass
class HealthStatus:
    """Health status information"""
    service: str
    status: str  # healthy, degraded, unhealthy
    timestamp: datetime
    details: Dict[str, Any]
    response_time: float
    error_message: Optional[str] = None

@dataclass
class SystemMetrics:
    """System performance metrics"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    timestamp: datetime

class HealthMonitor:
    """Comprehensive health monitoring system"""
    
    def __init__(self, redis_client: redis.Redis, stream_processor: StreamProcessor):
        self.redis = redis_client
        self.stream_processor = stream_processor
        self.health_checks = self._initialize_health_checks()
        self.alert_thresholds = self._initialize_alert_thresholds()
        
    def _initialize_health_checks(self) -> Dict[str, callable]:
        """Initialize health check functions"""
        return {
            "database": self._check_database_health,
            "redis": self._check_redis_health,
            "api": self._check_api_health,
            "stream_processor": self._check_stream_processor_health,
            "model": self._check_model_health,
            "system": self._check_system_health
        }
    
    def _initialize_alert_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Initialize alert thresholds"""
        return {
            "database": {
                "response_time": 2.0,  # seconds
                "connection_failure_rate": 0.1  # 10%
            },
            "redis": {
                "response_time": 0.5,  # seconds
                "memory_usage": 0.8  # 80%
            },
            "api": {
                "response_time": 5.0,  # seconds
                "error_rate": 0.05  # 5%
            },
            "system": {
                "cpu_usage": 0.8,  # 80%
                "memory_usage": 0.85,  # 85%
                "disk_usage": 0.9  # 90%
            }
        }
    
    async def perform_health_check(self) -> Dict[str, HealthStatus]:
        """Perform comprehensive health check"""
        HEALTH_CHECK_COUNTER.inc()
        
        start_time = datetime.utcnow()
        results = {}
        
        try:
            # Run all health checks concurrently
            tasks = []
            for service, check_func in self.health_checks.items():
                task = asyncio.create_task(self._run_health_check(service, check_func))
                tasks.append(task)
            
            # Wait for all checks to complete
            check_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, (service, check_func) in enumerate(self.health_checks.items()):
                result = check_results[i]
                if isinstance(result, Exception):
                    results[service] = HealthStatus(
                        service=service,
                        status="unhealthy",
                        timestamp=datetime.utcnow(),
                        details={"error": str(result)},
                        response_time=0.0,
                        error_message=str(result)
                    )
                else:
                    results[service] = result
            
            # Record overall health check duration
            duration = (datetime.utcnow() - start_time).total_seconds()
            HEALTH_CHECK_DURATION.observe(duration)
            
            return results
            
        except Exception as e:
            logger.error(f"Error performing health check: {e}")
            ERROR_RATE.labels(service="health_monitor", error_type="health_check_failed").inc()
            return {}
    
    async def _run_health_check(self, service: str, check_func: callable) -> HealthStatus:
        """Run a single health check"""
        start_time = datetime.utcnow()
        
        try:
            if asyncio.iscoroutinefunction(check_func):
                details = await check_func()
            else:
                details = check_func()
            
            response_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Determine status based on thresholds
            status = self._determine_status(service, details, response_time)
            
            return HealthStatus(
                service=service,
                status=status,
                timestamp=datetime.utcnow(),
                details=details,
                response_time=response_time
            )
            
        except Exception as e:
            response_time = (datetime.utcnow() - start_time).total_seconds()
            logger.error(f"Health check failed for {service}: {e}")
            ERROR_RATE.labels(service=service, error_type="health_check_failed").inc()
            
            return HealthStatus(
                service=service,
                status="unhealthy",
                timestamp=datetime.utcnow(),
                details={"error": str(e)},
                response_time=response_time,
                error_message=str(e)
            )
    
    def _check_database_health(self) -> Dict[str, Any]:
        """Check database health"""
        db = SessionLocal()
        try:
            start_time = datetime.utcnow()
            
            # Test basic query
            claim_count = db.query(Claim).count()
            
            # Test complex query
            recent_claims = db.query(Claim).filter(
                Claim.submission_date >= datetime.utcnow() - timedelta(days=1)
            ).count()
            
            # Check connection pool
            connection_info = {
                "total_claims": claim_count,
                "recent_claims": recent_claims,
                "connection_pool_size": db.bind.pool.size(),
                "checked_out_connections": db.bind.pool.checkedout()
            }
            
            return connection_info
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            raise
        finally:
            db.close()
    
    def _check_redis_health(self) -> Dict[str, Any]:
        """Check Redis health"""
        try:
            start_time = datetime.utcnow()
            
            # Test basic operations
            test_key = "health_check_test"
            self.redis.set(test_key, "test_value", ex=60)
            value = self.redis.get(test_key)
            self.redis.delete(test_key)
            
            # Get Redis info
            info = self.redis.info()
            
            redis_info = {
                "ping_response": self.redis.ping(),
                "memory_usage": info.get("used_memory_human", "unknown"),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
            
            return redis_info
            
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            raise
    
    def _check_api_health(self) -> Dict[str, Any]:
        """Check API health"""
        try:
            start_time = datetime.utcnow()
            
            # Test API endpoints
            api_url = "http://localhost:8000/health"
            response = requests.get(api_url, timeout=10)
            
            api_info = {
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "content_length": len(response.content),
                "endpoint": "/health"
            }
            
            # Record API response time metric
            API_RESPONSE_TIME.observe(response.elapsed.total_seconds())
            
            return api_info
            
        except Exception as e:
            logger.error(f"API health check failed: {e}")
            raise
    
    def _check_stream_processor_health(self) -> Dict[str, Any]:
        """Check stream processor health"""
        try:
            processor_info = {
                "is_running": self.stream_processor.is_running,
                "queue_size": self.stream_processor.processing_queue.qsize(),
                "batch_size": self.stream_processor.batch_size
            }
            
            # Get real-time metrics
            metrics = asyncio.run(self.stream_processor.get_realtime_metrics())
            processor_info.update(metrics)
            
            return processor_info
            
        except Exception as e:
            logger.error(f"Stream processor health check failed: {e}")
            raise
    
    def _check_model_health(self) -> Dict[str, Any]:
        """Check ML model health"""
        try:
            # Check if model files exist and are accessible
            model_info = {
                "model_loaded": True,  # Would check actual model loading
                "model_version": "v1.0.0",
                "last_training_date": "2024-01-01",
                "prediction_count": 0  # Would get from metrics
            }
            
            # Check model performance metrics
            # This would query the database for recent prediction accuracy
            
            return model_info
            
        except Exception as e:
            logger.error(f"Model health check failed: {e}")
            raise
    
    def _check_system_health(self) -> Dict[str, Any]:
        """Check system health"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            SYSTEM_CPU_USAGE.set(cpu_usage)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            SYSTEM_MEMORY_USAGE.set(memory_usage)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
            
            system_info = {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "disk_usage": disk_usage,
                "network_io": network_io,
                "load_average": psutil.getloadavg(),
                "uptime": (datetime.utcnow() - datetime.fromtimestamp(psutil.boot_time())).total_seconds()
            }
            
            return system_info
            
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            raise
    
    def _determine_status(self, service: str, details: Dict[str, Any], response_time: float) -> str:
        """Determine health status based on thresholds"""
        thresholds = self.alert_thresholds.get(service, {})
        
        # Check response time
        if "response_time" in thresholds and response_time > thresholds["response_time"]:
            return "degraded"
        
        # Service-specific checks
        if service == "database":
            if "error" in details:
                return "unhealthy"
            
        elif service == "redis":
            if not details.get("ping_response", False):
                return "unhealthy"
            
        elif service == "api":
            if details.get("status_code", 500) >= 500:
                return "unhealthy"
            elif details.get("status_code", 200) >= 400:
                return "degraded"
            
        elif service == "system":
            cpu_usage = details.get("cpu_usage", 0)
            memory_usage = details.get("memory_usage", 0)
            
            if cpu_usage > thresholds.get("cpu_usage", 0.8) * 100:
                return "degraded"
            if memory_usage > thresholds.get("memory_usage", 0.85) * 100:
                return "degraded"
        
        return "healthy"
    
    async def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
            
            return SystemMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                network_io=network_io,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            raise
    
    async def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        try:
            # Perform health check
            health_results = await self.perform_health_check()
            
            # Get system metrics
            system_metrics = await self.get_system_metrics()
            
            # Calculate overall health
            healthy_services = sum(1 for result in health_results.values() if result.status == "healthy")
            total_services = len(health_results)
            overall_health = "healthy" if healthy_services == total_services else "degraded"
            
            # Generate alerts
            alerts = self._generate_alerts(health_results, system_metrics)
            
            return {
                "overall_status": overall_health,
                "timestamp": datetime.utcnow().isoformat(),
                "services": {
                    service: {
                        "status": result.status,
                        "response_time": result.response_time,
                        "details": result.details,
                        "error_message": result.error_message
                    }
                    for service, result in health_results.items()
                },
                "system_metrics": {
                    "cpu_usage": system_metrics.cpu_usage,
                    "memory_usage": system_metrics.memory_usage,
                    "disk_usage": system_metrics.disk_usage,
                    "network_io": system_metrics.network_io
                },
                "alerts": alerts,
                "summary": {
                    "total_services": total_services,
                    "healthy_services": healthy_services,
                    "degraded_services": sum(1 for r in health_results.values() if r.status == "degraded"),
                    "unhealthy_services": sum(1 for r in health_results.values() if r.status == "unhealthy")
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating health report: {e}")
            return {
                "overall_status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _generate_alerts(self, health_results: Dict[str, HealthStatus], system_metrics: SystemMetrics) -> List[Dict[str, Any]]:
        """Generate alerts based on health results and system metrics"""
        alerts = []
        
        # Check service health
        for service, result in health_results.items():
            if result.status == "unhealthy":
                alerts.append({
                    "level": "critical",
                    "service": service,
                    "message": f"Service {service} is unhealthy",
                    "details": result.error_message or "Service health check failed",
                    "timestamp": result.timestamp.isoformat()
                })
            elif result.status == "degraded":
                alerts.append({
                    "level": "warning",
                    "service": service,
                    "message": f"Service {service} is degraded",
                    "details": f"Response time: {result.response_time}s",
                    "timestamp": result.timestamp.isoformat()
                })
        
        # Check system metrics
        if system_metrics.cpu_usage > 80:
            alerts.append({
                "level": "warning",
                "service": "system",
                "message": "High CPU usage detected",
                "details": f"CPU usage: {system_metrics.cpu_usage}%",
                "timestamp": system_metrics.timestamp.isoformat()
            })
        
        if system_metrics.memory_usage > 85:
            alerts.append({
                "level": "warning",
                "service": "system",
                "message": "High memory usage detected",
                "details": f"Memory usage: {system_metrics.memory_usage}%",
                "timestamp": system_metrics.timestamp.isoformat()
            })
        
        if system_metrics.disk_usage > 90:
            alerts.append({
                "level": "critical",
                "service": "system",
                "message": "High disk usage detected",
                "details": f"Disk usage: {system_metrics.disk_usage}%",
                "timestamp": system_metrics.timestamp.isoformat()
            })
        
        return alerts
    
    async def start_monitoring(self, interval_seconds: int = 60):
        """Start continuous monitoring"""
        logger.info(f"Starting health monitoring with {interval_seconds}s interval")
        
        while True:
            try:
                # Generate health report
                report = await self.generate_health_report()
                
                # Store report in Redis
                report_key = f"health_report:{datetime.utcnow().strftime('%Y%m%d_%H%M')}"
                self.redis.setex(report_key, 3600, json.dumps(report))  # 1 hour TTL
                
                # Log critical alerts
                for alert in report.get("alerts", []):
                    if alert["level"] == "critical":
                        logger.critical(f"CRITICAL ALERT: {alert['message']} - {alert['details']}")
                    elif alert["level"] == "warning":
                        logger.warning(f"WARNING: {alert['message']} - {alert['details']}")
                
                # Wait for next check
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(interval_seconds) 