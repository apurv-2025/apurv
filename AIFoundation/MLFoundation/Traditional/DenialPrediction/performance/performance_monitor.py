"""
Performance Monitor for Real-time System Monitoring
"""

import asyncio
import time
import json
import threading
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import numpy as np
import redis
import logging
import psutil

logger = logging.getLogger('performance')

@dataclass
class PerformanceMetrics:
    """Performance metrics tracking"""
    latency_p50: float = 0.0
    latency_p95: float = 0.0
    latency_p99: float = 0.0
    throughput_rps: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    cache_hit_rate: float = 0.0
    model_inference_time: float = 0.0
    feature_retrieval_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

class PerformanceMonitor:
    """Real-time performance monitoring"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379)
        self.metrics_history = []
        self.request_times = []
        self.lock = threading.Lock()
        
    def record_request(self, duration: float, endpoint: str = "default"):
        """Record request duration"""
        with self.lock:
            self.request_times.append({
                'duration': duration,
                'endpoint': endpoint,
                'timestamp': time.time()
            })
            
            # Keep only last 1000 requests
            if len(self.request_times) > 1000:
                self.request_times = self.request_times[-1000:]
    
    def get_current_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics"""
        with self.lock:
            if not self.request_times:
                return PerformanceMetrics()
            
            # Calculate latency percentiles
            recent_times = [r['duration'] for r in self.request_times[-100:]]
            recent_times.sort()
            
            n = len(recent_times)
            p50 = recent_times[int(n * 0.5)] if n > 0 else 0
            p95 = recent_times[int(n * 0.95)] if n > 0 else 0
            p99 = recent_times[int(n * 0.99)] if n > 0 else 0
            
            # Calculate throughput (requests per second)
            now = time.time()
            recent_requests = [r for r in self.request_times if now - r['timestamp'] < 60]
            throughput = len(recent_requests) / 60.0
            
            # System metrics
            memory_usage = psutil.virtual_memory().used / (1024 * 1024)  # MB
            cpu_usage = psutil.cpu_percent()
            
            return PerformanceMetrics(
                latency_p50=p50 * 1000,  # Convert to ms
                latency_p95=p95 * 1000,
                latency_p99=p99 * 1000,
                throughput_rps=throughput,
                memory_usage_mb=memory_usage,
                cpu_usage_percent=cpu_usage,
                timestamp=datetime.now()
            )
    
    async def store_metrics(self, metrics: PerformanceMetrics):
        """Store metrics in Redis for historical tracking"""
        try:
            # Store current metrics
            metrics_key = f"performance:metrics:{datetime.now().strftime('%Y%m%d:%H')}"
            metrics_data = {
                'latency_p50': metrics.latency_p50,
                'latency_p95': metrics.latency_p95,
                'latency_p99': metrics.latency_p99,
                'throughput_rps': metrics.throughput_rps,
                'memory_usage_mb': metrics.memory_usage_mb,
                'cpu_usage_percent': metrics.cpu_usage_percent,
                'cache_hit_rate': metrics.cache_hit_rate,
                'model_inference_time': metrics.model_inference_time,
                'feature_retrieval_time': metrics.feature_retrieval_time,
                'timestamp': metrics.timestamp.isoformat()
            }
            
            # Store in Redis with expiration (24 hours)
            self.redis_client.setex(
                metrics_key,
                86400,  # 24 hours
                json.dumps(metrics_data)
            )
            
            # Add to history
            self.metrics_history.append(metrics)
            
            # Keep only last 1000 metrics
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]
                
        except Exception as e:
            logger.error(f"Error storing metrics: {e}")
    
    def get_historical_metrics(self, hours: int = 24) -> List[PerformanceMetrics]:
        """Get historical metrics from Redis"""
        try:
            metrics = []
            now = datetime.now()
            
            for i in range(hours):
                time_key = (now - timedelta(hours=i)).strftime('%Y%m%d:%H')
                metrics_key = f"performance:metrics:{time_key}"
                
                data = self.redis_client.get(metrics_key)
                if data:
                    metrics_data = json.loads(data)
                    metrics.append(PerformanceMetrics(**metrics_data))
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error retrieving historical metrics: {e}")
            return []
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        current_metrics = self.get_current_metrics()
        historical_metrics = self.get_historical_metrics(24)
        
        if not historical_metrics:
            return {
                'current': current_metrics.__dict__,
                'trends': {},
                'alerts': []
            }
        
        # Calculate trends
        avg_latency = np.mean([m.latency_p50 for m in historical_metrics])
        avg_throughput = np.mean([m.throughput_rps for m in historical_metrics])
        avg_memory = np.mean([m.memory_usage_mb for m in historical_metrics])
        
        # Check for alerts
        alerts = []
        if current_metrics.latency_p95 > avg_latency * 2:
            alerts.append("High latency detected")
        
        if current_metrics.memory_usage_mb > 1024:  # 1GB
            alerts.append("High memory usage")
        
        if current_metrics.cpu_usage_percent > 80:
            alerts.append("High CPU usage")
        
        return {
            'current': current_metrics.__dict__,
            'trends': {
                'avg_latency_ms': avg_latency,
                'avg_throughput_rps': avg_throughput,
                'avg_memory_mb': avg_memory
            },
            'alerts': alerts
        }
    
    def record_model_inference(self, duration: float):
        """Record model inference time"""
        with self.lock:
            current_metrics = self.get_current_metrics()
            current_metrics.model_inference_time = duration * 1000  # Convert to ms
            current_metrics.timestamp = datetime.now()
    
    def record_feature_retrieval(self, duration: float):
        """Record feature retrieval time"""
        with self.lock:
            current_metrics = self.get_current_metrics()
            current_metrics.feature_retrieval_time = duration * 1000  # Convert to ms
            current_metrics.timestamp = datetime.now()
    
    def record_cache_hit(self, hit: bool):
        """Record cache hit/miss"""
        with self.lock:
            # Simple cache hit rate calculation
            if not hasattr(self, '_cache_hits'):
                self._cache_hits = 0
                self._cache_total = 0
            
            self._cache_total += 1
            if hit:
                self._cache_hits += 1
            
            # Update current metrics
            current_metrics = self.get_current_metrics()
            current_metrics.cache_hit_rate = self._cache_hits / self._cache_total if self._cache_total > 0 else 0
            current_metrics.timestamp = datetime.now() 