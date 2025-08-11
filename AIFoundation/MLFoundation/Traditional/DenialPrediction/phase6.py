# Phase 6: Performance Optimization
# Caching, model optimization, feature store optimization, and scalability

import asyncio
import time
import json
import pickle
import hashlib
import threading
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np
import pandas as pd
import redis
import logging
from abc import ABC, abstractmethod
import psutil
import gc
from functools import wraps, lru_cache
import multiprocessing as mp
from contextlib import asynccontextmanager
import aiofiles
import aiocache
from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer
import onnxruntime as ort
import joblib
from sklearn.base import BaseEstimator
import mlflow

# Configure logging
logger = logging.getLogger('performance')
logger.setLevel(logging.INFO)

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
                cpu_usage_percent=cpu_usage
            )
    
    async def store_metrics(self, metrics: PerformanceMetrics):
        """Store metrics in Redis for monitoring dashboard"""
        metrics_data = {
            'latency_p50': metrics.latency_p50,
            'latency_p95': metrics.latency_p95,
            'latency_p99': metrics.latency_p99,
            'throughput_rps': metrics.throughput_rps,
            'memory_usage_mb': metrics.memory_usage_mb,
            'cpu_usage_percent': metrics.cpu_usage_percent,
            'timestamp': metrics.timestamp.isoformat()
        }
        
        # Store with timestamp key
        key = f"metrics:{int(time.time())}"
        self.redis_client.setex(key, 3600, json.dumps(metrics_data))
        
        # Also store in a time series for real-time monitoring
        self.redis_client.lpush("metrics_stream", json.dumps(metrics_data))
        self.redis_client.ltrim("metrics_stream", 0, 999)  # Keep last 1000 entries

def performance_timer(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.3f}s")
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.3f}s")
    
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

class AdvancedFeatureCache:
    """Advanced caching system for features with smart invalidation"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379)
        self.local_cache = {}
        self.cache_stats = {'hits': 0, 'misses': 0, 'size': 0}
        self.max_local_cache_size = 10000
        self.ttl_default = 3600  # 1 hour
        self.lock = threading.Lock()
        
        # Feature TTL mapping based on update frequency
        self.feature_ttls = {
            'static': 86400,      # 24 hours for static features
            'daily': 3600,        # 1 hour for daily updated features  
            'hourly': 300,        # 5 minutes for hourly features
            'real_time': 60       # 1 minute for real-time features
        }
    
    async def get_features(self, entity_key: str, feature_names: List[str], 
                          feature_types: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """Get features with multi-level caching"""
        
        # Try local cache first (L1)
        local_result = self._get_from_local_cache(entity_key, feature_names)
        if local_result is not None:
            self._update_cache_stats('hits')
            return local_result
        
        # Try Redis cache (L2)
        redis_result = await self._get_from_redis_cache(entity_key, feature_names)
        if redis_result is not None:
            # Store in local cache
            self._store_in_local_cache(entity_key, feature_names, redis_result)
            self._update_cache_stats('hits')
            return redis_result
        
        # Cache miss
        self._update_cache_stats('misses')
        return None
    
    async def store_features(self, entity_key: str, features: Dict[str, Any], 
                           feature_types: Dict[str, str] = None):
        """Store features in multi-level cache with appropriate TTLs"""
        
        # Store in Redis with feature-specific TTLs
        await self._store_in_redis_cache(entity_key, features, feature_types)
        
        # Store in local cache
        feature_names = list(features.keys())
        self._store_in_local_cache(entity_key, feature_names, features)
    
    def _get_from_local_cache(self, entity_key: str, feature_names: List[str]) -> Optional[Dict[str, Any]]:
        """Get from local in-memory cache"""
        cache_key = self._generate_cache_key(entity_key, feature_names)
        
        with self.lock:
            if cache_key in self.local_cache:
                entry = self.local_cache[cache_key]
                
                # Check if expired
                if time.time() < entry['expires_at']:
                    return entry['data']
                else:
                    # Remove expired entry
                    del self.local_cache[cache_key]
        
        return None
    
    def _store_in_local_cache(self, entity_key: str, feature_names: List[str], 
                            data: Dict[str, Any]):
        """Store in local cache with LRU eviction"""
        cache_key = self._generate_cache_key(entity_key, feature_names)
        
        with self.lock:
            # Implement LRU eviction if cache is full
            if len(self.local_cache) >= self.max_local_cache_size:
                # Remove oldest entry
                oldest_key = min(self.local_cache.keys(), 
                               key=lambda k: self.local_cache[k]['accessed_at'])
                del self.local_cache[oldest_key]
            
            self.local_cache[cache_key] = {
                'data': data,
                'expires_at': time.time() + self.ttl_default,
                'accessed_at': time.time()
            }
    
    async def _get_from_redis_cache(self, entity_key: str, 
                                   feature_names: List[str]) -> Optional[Dict[str, Any]]:
        """Get from Redis cache"""
        cache_key = self._generate_cache_key(entity_key, feature_names)
        
        try:
            cached_data = self.redis_client.get(f"features:{cache_key}")
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            logger.error(f"Redis cache error: {e}")
        
        return None
    
    async def _store_in_redis_cache(self, entity_key: str, features: Dict[str, Any], 
                                   feature_types: Dict[str, str] = None):
        """Store in Redis cache with feature-specific TTLs"""
        
        if not feature_types:
            feature_types = {name: 'daily' for name in features.keys()}
        
        # Group features by TTL
        ttl_groups = {}
        for feature_name, feature_value in features.items():
            feature_type = feature_types.get(feature_name, 'daily')
            ttl = self.feature_ttls.get(feature_type, self.ttl_default)
            
            if ttl not in ttl_groups:
                ttl_groups[ttl] = {}
            ttl_groups[ttl][feature_name] = feature_value
        
        # Store each TTL group separately
        for ttl, feature_group in ttl_groups.items():
            feature_names = list(feature_group.keys())
            cache_key = self._generate_cache_key(entity_key, feature_names)
            
            try:
                self.redis_client.setex(
                    f"features:{cache_key}",
                    ttl,
                    json.dumps(feature_group, default=str)
                )
            except Exception as e:
                logger.error(f"Redis store error: {e}")
    
    def _generate_cache_key(self, entity_key: str, feature_names: List[str]) -> str:
        """Generate consistent cache key"""
        feature_hash = hashlib.md5('|'.join(sorted(feature_names)).encode()).hexdigest()
        return f"{entity_key}:{feature_hash}"
    
    def _update_cache_stats(self, stat_type: str):
        """Update cache statistics"""
        with self.lock:
            self.cache_stats[stat_type] += 1
            self.cache_stats['size'] = len(self.local_cache)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        with self.lock:
            total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
            hit_rate = self.cache_stats['hits'] / total_requests if total_requests > 0 else 0
            
            return {
                'hit_rate': hit_rate,
                'total_hits': self.cache_stats['hits'],
                'total_misses': self.cache_stats['misses'],
                'cache_size': self.cache_stats['size'],
                'max_size': self.max_local_cache_size
            }
    
    async def invalidate_pattern(self, pattern: str):
        """Invalidate cache entries matching pattern"""
        # Invalidate Redis cache
        keys = self.redis_client.keys(f"features:{pattern}")
        if keys:
            self.redis_client.delete(*keys)
        
        # Invalidate local cache
        with self.lock:
            keys_to_remove = [k for k in self.local_cache.keys() if pattern in k]
            for key in keys_to_remove:
                del self.local_cache[key]

class ModelOptimizer:
    """Optimize ML models for production inference"""
    
    def __init__(self):
        self.optimization_techniques = {
            'quantization': self._apply_quantization,
            'pruning': self._apply_pruning,
            'onnx_conversion': self._convert_to_onnx,
            'feature_selection': self._optimize_features
        }
    
    async def optimize_model(self, model, X_test: pd.DataFrame, y_test: pd.Series,
                           techniques: List[str] = None) -> Dict[str, Any]:
        """Apply multiple optimization techniques to model"""
        
        if techniques is None:
            techniques = ['onnx_conversion', 'feature_selection']
        
        optimization_results = {
            'original_model': model,
            'optimized_models': {},
            'performance_comparison': {},
            'recommendations': []
        }
        
        # Baseline performance
        baseline_metrics = await self._benchmark_model(model, X_test, y_test)
        optimization_results['baseline'] = baseline_metrics
        
        # Apply each optimization technique
        for technique in techniques:
            if technique in self.optimization_techniques:
                logger.info(f"Applying {technique} optimization...")
                
                try:
                    optimized_model, metrics = await self.optimization_techniques[technique](
                        model, X_test, y_test
                    )
                    
                    optimization_results['optimized_models'][technique] = optimized_model
                    optimization_results['performance_comparison'][technique] = {
                        'original': baseline_metrics,
                        'optimized': metrics,
                        'improvement': self._calculate_improvement(baseline_metrics, metrics)
                    }
                    
                except Exception as e:
                    logger.error(f"Failed to apply {technique}: {e}")
                    optimization_results['performance_comparison'][technique] = {
                        'error': str(e)
                    }
        
        # Generate recommendations
        optimization_results['recommendations'] = self._generate_optimization_recommendations(
            optimization_results['performance_comparison']
        )
        
        return optimization_results
    
    async def _benchmark_model(self, model, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """Benchmark model performance"""
        start_time = time.time()
        
        # Inference time
        inference_start = time.time()
        predictions = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else model.predict(X_test)
        inference_time = time.time() - inference_start
        
        # Model size
        model_size = len(pickle.dumps(model)) / (1024 * 1024)  # MB
        
        # Memory usage
        import psutil
        process = psutil.Process()
        memory_before = process.memory_info().rss
        _ = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else model.predict(X_test)
        memory_after = process.memory_info().rss
        memory_usage = (memory_after - memory_before) / (1024 * 1024)  # MB
        
        # Accuracy metrics
        from sklearn.metrics import roc_auc_score, accuracy_score
        
        if hasattr(model, 'predict_proba'):
            auc = roc_auc_score(y_test, predictions)
            accuracy = accuracy_score(y_test, (predictions >= 0.5).astype(int))
        else:
            auc = 0.0
            accuracy = accuracy_score(y_test, predictions)
        
        return {
            'inference_time_ms': inference_time * 1000,
            'throughput_rps': len(X_test) / inference_time,
            'model_size_mb': model_size,
            'memory_usage_mb': memory_usage,
            'auc': auc,
            'accuracy': accuracy
        }
    
    async def _apply_quantization(self, model, X_test: pd.DataFrame, y_test: pd.Series) -> Tuple[Any, Dict]:
        """Apply model quantization for faster inference"""
        # This is a simplified example - actual implementation would depend on model type
        
        # For tree-based models, we can reduce precision of thresholds
        if hasattr(model, 'tree_'):
            quantized_model = self._quantize_tree_model(model)
        else:
            # For other models, use general quantization
            quantized_model = model  # Placeholder
        
        metrics = await self._benchmark_model(quantized_model, X_test, y_test)
        return quantized_model, metrics
    
    def _quantize_tree_model(self, model):
        """Quantize tree-based model by reducing threshold precision"""
        import copy
        quantized_model = copy.deepcopy(model)
        
        # Reduce precision of decision thresholds (simplified)
        if hasattr(quantized_model, 'tree_'):
            tree = quantized_model.tree_
            # Round thresholds to reduce precision
            tree.threshold = np.round(tree.threshold, decimals=2)
        
        return quantized_model
    
    async def _apply_pruning(self, model, X_test: pd.DataFrame, y_test: pd.Series) -> Tuple[Any, Dict]:
        """Apply model pruning to reduce complexity"""
        # For tree-based models, prune least important branches
        if hasattr(model, 'tree_'):
            pruned_model = self._prune_tree_model(model, X_test, y_test)
        else:
            # For other models, use feature-based pruning
            pruned_model = model  # Placeholder
        
        metrics = await self._benchmark_model(pruned_model, X_test, y_test)
        return pruned_model, metrics
    
    def _prune_tree_model(self, model, X_test: pd.DataFrame, y_test: pd.Series):
        """Prune tree-based model (simplified implementation)"""
        import copy
        from sklearn.tree import DecisionTreeClassifier
        
        if isinstance(model, DecisionTreeClassifier):
            # Create a pruned version with limited depth
            pruned_model = DecisionTreeClassifier(
                max_depth=min(model.get_depth() - 1, 10),
                random_state=42
            )
            # Would need training data to refit - this is simplified
            pruned_model = copy.deepcopy(model)
        else:
            pruned_model = copy.deepcopy(model)
        
        return pruned_model
    
    async def _convert_to_onnx(self, model, X_test: pd.DataFrame, y_test: pd.Series) -> Tuple[Any, Dict]:
        """Convert model to ONNX format for optimized inference"""
        try:
            from skl2onnx import convert_sklearn
            from skl2onnx.common.data_types import FloatTensorType
            
            # Define input shape
            initial_type = [('float_input', FloatTensorType([None, X_test.shape[1]]))]
            
            # Convert to ONNX
            onnx_model = convert_sklearn(model, initial_types=initial_type)
            
            # Create ONNX runtime session
            onnx_session = ort.InferenceSession(onnx_model.SerializeToString())
            
            # Benchmark ONNX model
            start_time = time.time()
            input_name = onnx_session.get_inputs()[0].name
            predictions = onnx_session.run(None, {input_name: X_test.values.astype(np.float32)})
            inference_time = time.time() - start_time
            
            # Calculate metrics
            if len(predictions) > 1:  # Classification with probabilities
                pred_proba = predictions[1][:, 1] if predictions[1].shape[1] > 1 else predictions[1][:, 0]
            else:
                pred_proba = predictions[0]
            
            from sklearn.metrics import roc_auc_score, accuracy_score
            auc = roc_auc_score(y_test, pred_proba)
            accuracy = accuracy_score(y_test, (pred_proba >= 0.5).astype(int))
            
            metrics = {
                'inference_time_ms': inference_time * 1000,
                'throughput_rps': len(X_test) / inference_time,
                'model_size_mb': len(onnx_model.SerializeToString()) / (1024 * 1024),
                'memory_usage_mb': 0,  # Would need more detailed measurement
                'auc': auc,
                'accuracy': accuracy
            }
            
            return onnx_session, metrics
            
        except Exception as e:
            logger.error(f"ONNX conversion failed: {e}")
            # Fall back to original model
            metrics = await self._benchmark_model(model, X_test, y_test)
            return model, metrics
    
    async def _optimize_features(self, model, X_test: pd.DataFrame, y_test: pd.Series) -> Tuple[Any, Dict]:
        """Optimize feature set for better performance"""
        from sklearn.feature_selection import SelectKBest, f_classif
        from sklearn.base import clone
        
        # Select top features based on statistical tests
        selector = SelectKBest(score_func=f_classif, k=min(20, X_test.shape[1] // 2))
        X_selected = selector.fit_transform(X_test, y_test)
        
        # Create new model with selected features
        optimized_model = clone(model)
        
        # Note: In practice, you'd need to retrain the model with selected features
        # This is a simplified example
        selected_features = selector.get_support()
        
        # Create wrapper that applies feature selection
        class FeatureOptimizedModel:
            def __init__(self, model, feature_mask):
                self.model = model
                self.feature_mask = feature_mask
            
            def predict(self, X):
                X_selected = X[:, self.feature_mask] if isinstance(X, np.ndarray) else X.iloc[:, self.feature_mask]
                return self.model.predict(X_selected)
            
            def predict_proba(self, X):
                X_selected = X[:, self.feature_mask] if isinstance(X, np.ndarray) else X.iloc[:, self.feature_mask]
                return self.model.predict_proba(X_selected)
        
        feature_optimized_model = FeatureOptimizedModel(model, selected_features)
        
        # Benchmark the optimized model
        metrics = await self._benchmark_model(feature_optimized_model, X_test, y_test)
        
        return feature_optimized_model, metrics
    
    def _calculate_improvement(self, baseline: Dict[str, float], optimized: Dict[str, float]) -> Dict[str, float]:
        """Calculate improvement metrics"""
        improvements = {}
        
        for metric in ['inference_time_ms', 'model_size_mb', 'memory_usage_mb']:
            if metric in baseline and metric in optimized:
                if baseline[metric] > 0:
                    improvement = (baseline[metric] - optimized[metric]) / baseline[metric] * 100
                    improvements[f"{metric}_improvement_pct"] = improvement
        
        for metric in ['throughput_rps', 'auc', 'accuracy']:
            if metric in baseline and metric in optimized:
                if baseline[metric] > 0:
                    improvement = (optimized[metric] - baseline[metric]) / baseline[metric] * 100
                    improvements[f"{metric}_improvement_pct"] = improvement
        
        return improvements
    
    def _generate_optimization_recommendations(self, comparison_results: Dict) -> List[str]:
        """Generate optimization recommendations based on results"""
        recommendations = []
        
        for technique, results in comparison_results.items():
            if 'error' in results:
                continue
            
            improvements = results['improvement']
            
            # Check for significant improvements
            if improvements.get('inference_time_ms_improvement_pct', 0) > 20:
                recommendations.append(f"Use {technique} for {improvements['inference_time_ms_improvement_pct']:.1f}% faster inference")
            
            if improvements.get('model_size_mb_improvement_pct', 0) > 30:
                recommendations.append(f"Use {technique} for {improvements['model_size_mb_improvement_pct']:.1f}% smaller model size")
            
            if improvements.get('memory_usage_mb_improvement_pct', 0) > 25:
                recommendations.append(f"Use {technique} for {improvements['memory_usage_mb_improvement_pct']:.1f}% lower memory usage")
        
        if not recommendations:
            recommendations.append("Current model is already well-optimized for production")
        
        return recommendations

class AsyncModelInference:
    """Asynchronous model inference with batching and pooling"""
    
    def __init__(self, model, batch_size: int = 32, max_workers: int = 4):
        self.model = model
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.request_queue = asyncio.Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.batch_processor = None
        self.running = False
    
    async def start(self):
        """Start the batch processing service"""
        self.running = True
        self.batch_processor = asyncio.create_task(self._batch_processor())
    
    async def stop(self):
        """Stop the batch processing service"""
        self.running = False
        if self.batch_processor:
            await self.batch_processor
        self.executor.shutdown(wait=True)
    
    async def predict(self, features: pd.DataFrame) -> np.ndarray:
        """Async prediction with automatic batching"""
        future = asyncio.Future()
        
        await self.request_queue.put({
            'features': features,
            'future': future
        })
        
        return await future
    
    async def _batch_processor(self):
        """Process requests in batches"""
        while self.running:
            batch = []
            
            try:
                # Collect requests for batch
                while len(batch) < self.batch_size:
                    try:
                        request = await asyncio.wait_for(self.request_queue.get(), timeout=0.1)
                        batch.append(request)
                    except asyncio.TimeoutError:
                        break
                
                if batch:
                    await self._process_batch(batch)
                    
            except Exception as e:
                logger.error(f"Batch processing error: {e}")
                # Set error for all requests in batch
                for request in batch:
                    request['future'].set_exception(e)
    
    async def _process_batch(self, batch: List[Dict]):
        """Process a batch of prediction requests"""
        try:
            # Combine all features
            all_features = pd.concat([req['features'] for req in batch], ignore_index=True)
            
            # Run inference in thread pool
            loop = asyncio.get_event_loop()
            predictions = await loop.run_in_executor(
                self.executor,
                self._run_inference,
                all_features
            )
            
            # Split predictions back to individual requests
            start_idx = 0
            for request in batch:
                end_idx = start_idx + len(request['features'])
                request_predictions = predictions[start_idx:end_idx]
                request['future'].set_result(request_predictions)
                start_idx = end_idx
                
        except Exception as e:
            # Set error for all requests
            for request in batch:
                request['future'].set_exception(e)
    
    def _run_inference(self, features: pd.DataFrame) -> np.ndarray:
        """Run model inference (blocking)"""
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(features)[:, 1]
        else:
            return self.model.predict(features)

class FeatureStoreOptimizer:
    """Optimize feature store for high-performance retrieval"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379)
        self.feature_cache = AdvancedFeatureCache(redis_client)
        
        # Feature computation pipelines
        self.precomputed_features = {}
        self.feature_pipelines = {}
        
    async def precompute_features(self, entity_ids: List[str], 
                                 feature_definitions: Dict[str, callable]):
        """Precompute features for faster retrieval"""
        logger.info(f"Precomputing features for {len(entity_ids)} entities")
        
        # Use multiprocessing for CPU-intensive feature computation
        with ProcessPoolExecutor() as executor:
            tasks = []
            
            for entity_id in entity_ids:
                task = asyncio.get_event_loop().run_in_executor(
                    executor,
                    self._compute_entity_features,
                    entity_id,
                    feature_definitions
                )
                tasks.append((entity_id, task))
            
            # Wait for all computations
            for entity_id, task in tasks:
                try:
                    features = await task
                    await self.feature_cache.store_features(
                        entity_id, 
                        features,
                        self._get_feature_types(features)
                    )
                except Exception as e:
                    logger.error(f"Failed to precompute features for {entity_id}: {e}")
    
    def _compute_entity_features(self, entity_id: str, 
                               feature_definitions: Dict[str, callable]) -> Dict[str, Any]:
        """Compute features for a single entity"""
        features = {}
        
        for feature_name, compute_func in feature_definitions.items():
            try:
                features[feature_name] = compute_func(entity_id)
            except Exception as e:
                logger.error(f"Failed to compute {feature_name} for {entity_id}: {e}")
                features[feature_name] = None
        
        return features
    
    def _get_feature_types(self, features: Dict[str, Any]) -> Dict[str, str]:
        """Determine feature types for TTL optimization"""
        # This would be more sophisticated in practice
        feature_types = {}
        
        for feature_name, value in features.items():
            if 'historical' in feature_name.lower():
                feature_types[feature_name] = 'static'
            elif 'daily' in feature_name.lower():
                feature_types[feature_name] = 'daily'
            elif 'real_time' in feature_name.lower():
                feature_types[feature_name] = 'real_time'
            else:
                feature_types[feature_name] = 'hourly'
        
        return feature_types
    
    async def warm_cache(self, popular_entities: List[str]):
        """Warm up cache with popular entities"""
        logger.info(f"Warming cache for {len(popular_entities)} popular entities")
        
        # Preload most frequently accessed features
        for entity_id in popular_entities:
            cached_features = await self.feature_cache.get_features(
                entity_id, 
                ['historical_denial_rate', 'avg_days_to_pay', 'provider_volume']
            )
            
            if cached_features is None:
                # Load from feature store and cache
                features = await self._load_from_feature_store(entity_id)
                if features:
                    await self.feature_cache.store_features(entity_id, features)
    
    async def _load_from_feature_store(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Load features from primary feature store"""
        # This would integrate with your actual feature store (Feast, Tecton, etc.)
        # Simplified implementation
        return {
            'historical_denial_rate': np.random.beta(2, 8),
            'avg_days_to_pay': np.random.normal(15, 5),
            'provider_volume': np.random.poisson(100)
        }

class ResourceManager:
    """Manage system resources for optimal performance"""
    
    def __init__(self):
        self.cpu_threshold = 80.0  # Percentage
        self.memory_threshold = 85.0  # Percentage
        self.monitoring_interval = 30  # Seconds
        self.running = False
        
    async def start_monitoring(self):
        """Start resource monitoring"""
        self.running = True
        while self.running:
            await self._check_resources()
            await asyncio.sleep(self.monitoring_interval)
    
    def stop_monitoring(self):
        """Stop resource monitoring"""
        self.running = False
    
    async def _check_resources(self):
        """Check system resources and take action if needed"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        logger.info(f"Resource usage - CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%")
        
        if cpu_percent > self.cpu_threshold:
            await self._handle_high_cpu()
        
        if memory_percent > self.memory_threshold:
            await self._handle_high_memory()
    
    async def _handle_high_cpu(self):
        """Handle high CPU usage"""
        logger.warning("High CPU usage detected - implementing throttling")
        
        # Reduce batch sizes
        # Increase request timeouts
        # Scale down non-essential processes
        
    async def _handle_high_memory(self):
        """Handle high memory usage"""
        logger.warning("High memory usage detected - cleaning up")
        
        # Clear caches
        gc.collect()
        
        # Reduce cache sizes
        # Implement memory-efficient algorithms

# Example integration and testing
async def optimize_system_performance():
    """Example of system-wide performance optimization"""
    
    # Initialize components
    performance_monitor = PerformanceMonitor()
    feature_cache = AdvancedFeatureCache()
    model_optimizer = ModelOptimizer()
    resource_manager = ResourceManager()
    
    # Start monitoring
    await resource_manager.start_monitoring()
    
    # Simulate model optimization
    logger.info("Starting model optimization...")
    
    # Create dummy model and data for testing
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification
    
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_df, y)
    
    # Optimize model
    optimization_results = await model_optimizer.optimize_model(
        model, X_df, pd.Series(y), 
        techniques=['onnx_conversion', 'feature_selection']
    )
    
    print("Optimization Results:")
    for technique, results in optimization_results['performance_comparison'].items():
        if 'improvement' in results:
            print(f"\n{technique}:")
            for metric, improvement in results['improvement'].items():
                print(f"  {metric}: {improvement:.2f}%")
    
    print("\nRecommendations:")
    for rec in optimization_results['recommendations']:
        print(f"- {rec}")
    
    # Test cache performance
    print(f"\nCache Performance:")
    cache_stats = feature_cache.get_cache_stats()
    for stat, value in cache_stats.items():
        print(f"  {stat}: {value}")
    
    # Stop monitoring
    resource_manager.stop_monitoring()

if __name__ == "__main__":
    asyncio.run(optimize_system_performance())
