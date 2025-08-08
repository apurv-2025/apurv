# =============================================================================
# FILE: backend/app/agent/monitoring.py
# =============================================================================
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import time
import json

class AgentMonitoring:
    """Monitors agent performance and health"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.last_activity = datetime.now()
        self.task_completions: List[Dict[str, Any]] = []
        self.error_log: List[Dict[str, Any]] = []
        self.performance_metrics: Dict[str, List[float]] = {
            "processing_times": [],
            "success_rates": [],
            "error_rates": []
        }
        
        # Rolling window for metrics (last 100 tasks)
        self.max_metrics_history = 100
    
    def record_task_completion(
        self, 
        task_id: str, 
        task_type: str, 
        status: str, 
        processing_time: float, 
        success: bool
    ):
        """Record a task completion for monitoring"""
        self.last_activity = datetime.now()
        
        completion_record = {
            "task_id": task_id,
            "task_type": task_type,
            "status": status,
            "processing_time": processing_time,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        self.task_completions.append(completion_record)
        
        # Keep only recent completions for performance calculation
        if len(self.task_completions) > self.max_metrics_history:
            self.task_completions = self.task_completions[-self.max_metrics_history:]
        
        # Update performance metrics
        self._update_performance_metrics()
        
        # Log errors
        if not success:
            self.error_log.append({
                "task_id": task_id,
                "task_type": task_type,
                "error_time": datetime.now().isoformat(),
                "processing_time": processing_time
            })
    
    def record_error(self, error: str, context: Dict[str, Any] = None):
        """Record an error for monitoring"""
        self.last_activity = datetime.now()
        
        error_record = {
            "error": error,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }
        
        self.error_log.append(error_record)
        
        # Keep only recent errors
        if len(self.error_log) > 50:
            self.error_log = self.error_log[-50:]
    
    def get_uptime(self) -> Dict[str, Any]:
        """Get agent uptime information"""
        now = datetime.now()
        uptime_duration = now - self.start_time
        
        return {
            "start_time": self.start_time.isoformat(),
            "current_time": now.isoformat(),
            "uptime_seconds": uptime_duration.total_seconds(),
            "uptime_days": uptime_duration.days,
            "uptime_hours": uptime_duration.seconds // 3600,
            "uptime_minutes": (uptime_duration.seconds % 3600) // 60
        }
    
    def get_last_activity(self) -> Dict[str, Any]:
        """Get last activity information"""
        now = datetime.now()
        time_since_last = now - self.last_activity
        
        return {
            "last_activity": self.last_activity.isoformat(),
            "seconds_since_last": time_since_last.total_seconds(),
            "minutes_since_last": time_since_last.total_seconds() / 60,
            "is_active": time_since_last.total_seconds() < 300  # 5 minutes
        }
    
    def get_performance_metrics(self, window_minutes: int = 60) -> Dict[str, Any]:
        """Get performance metrics for the specified time window"""
        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        
        # Filter completions within the window
        recent_completions = [
            c for c in self.task_completions
            if datetime.fromisoformat(c["timestamp"]) > cutoff_time
        ]
        
        if not recent_completions:
            return {
                "total_tasks": 0,
                "success_rate": 0.0,
                "avg_processing_time": 0.0,
                "error_rate": 0.0,
                "tasks_per_minute": 0.0
            }
        
        total_tasks = len(recent_completions)
        successful_tasks = len([c for c in recent_completions if c["success"]])
        failed_tasks = total_tasks - successful_tasks
        
        success_rate = (successful_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        error_rate = (failed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        processing_times = [c["processing_time"] for c in recent_completions]
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
        
        tasks_per_minute = total_tasks / window_minutes if window_minutes > 0 else 0
        
        return {
            "total_tasks": total_tasks,
            "success_rate": round(success_rate, 2),
            "avg_processing_time": round(avg_processing_time, 2),
            "error_rate": round(error_rate, 2),
            "tasks_per_minute": round(tasks_per_minute, 2),
            "min_processing_time": min(processing_times) if processing_times else 0,
            "max_processing_time": max(processing_times) if processing_times else 0
        }
    
    def get_task_type_performance(self) -> Dict[str, Any]:
        """Get performance metrics by task type"""
        task_type_stats = {}
        
        for completion in self.task_completions:
            task_type = completion["task_type"]
            
            if task_type not in task_type_stats:
                task_type_stats[task_type] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "processing_times": []
                }
            
            stats = task_type_stats[task_type]
            stats["total"] += 1
            
            if completion["success"]:
                stats["successful"] += 1
            else:
                stats["failed"] += 1
            
            stats["processing_times"].append(completion["processing_time"])
        
        # Calculate metrics for each task type
        for task_type, stats in task_type_stats.items():
            total = stats["total"]
            successful = stats["successful"]
            
            stats["success_rate"] = round((successful / total) * 100, 2) if total > 0 else 0
            stats["avg_processing_time"] = round(
                sum(stats["processing_times"]) / len(stats["processing_times"]), 2
            ) if stats["processing_times"] else 0
            stats["min_processing_time"] = min(stats["processing_times"]) if stats["processing_times"] else 0
            stats["max_processing_time"] = max(stats["processing_times"]) if stats["processing_times"] else 0
            
            # Remove raw processing times to keep response clean
            del stats["processing_times"]
        
        return task_type_stats
    
    def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get error summary for the specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_errors = [
            e for e in self.error_log
            if datetime.fromisoformat(e["timestamp"]) > cutoff_time
        ]
        
        if not recent_errors:
            return {
                "total_errors": 0,
                "error_rate": 0.0,
                "common_errors": [],
                "recent_errors": []
            }
        
        # Count error types
        error_counts = {}
        for error in recent_errors:
            error_type = error.get("error", "Unknown error")
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        # Get most common errors
        common_errors = sorted(
            error_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        # Calculate error rate
        total_tasks = len([c for c in self.task_completions 
                          if datetime.fromisoformat(c["timestamp"]) > cutoff_time])
        error_rate = (len(recent_errors) / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "total_errors": len(recent_errors),
            "error_rate": round(error_rate, 2),
            "common_errors": [{"error": error, "count": count} for error, count in common_errors],
            "recent_errors": recent_errors[-10:]  # Last 10 errors
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status of the agent"""
        uptime = self.get_uptime()
        last_activity = self.get_last_activity()
        recent_metrics = self.get_performance_metrics(window_minutes=15)
        error_summary = self.get_error_summary(hours=1)
        
        # Determine health status
        health_status = "healthy"
        health_score = 100
        
        # Check if agent is active
        if not last_activity["is_active"]:
            health_status = "inactive"
            health_score -= 30
        
        # Check error rate
        if error_summary["error_rate"] > 10:
            health_status = "degraded"
            health_score -= 20
        elif error_summary["error_rate"] > 5:
            health_score -= 10
        
        # Check processing time
        if recent_metrics["avg_processing_time"] > 30:  # More than 30 seconds
            health_status = "slow"
            health_score -= 15
        
        # Check success rate
        if recent_metrics["success_rate"] < 80:
            health_status = "unreliable"
            health_score -= 25
        
        return {
            "status": health_status,
            "health_score": max(0, health_score),
            "uptime": uptime,
            "last_activity": last_activity,
            "recent_performance": recent_metrics,
            "error_summary": error_summary,
            "recommendations": self._generate_health_recommendations(
                health_status, recent_metrics, error_summary
            )
        }
    
    def _update_performance_metrics(self):
        """Update rolling performance metrics"""
        if len(self.task_completions) < 10:
            return
        
        # Calculate metrics for recent completions
        recent_completions = self.task_completions[-10:]
        
        processing_times = [c["processing_time"] for c in recent_completions]
        success_count = len([c for c in recent_completions if c["success"]])
        
        avg_processing_time = sum(processing_times) / len(processing_times)
        success_rate = (success_count / len(recent_completions)) * 100
        error_rate = 100 - success_rate
        
        # Add to rolling metrics
        self.performance_metrics["processing_times"].append(avg_processing_time)
        self.performance_metrics["success_rates"].append(success_rate)
        self.performance_metrics["error_rates"].append(error_rate)
        
        # Keep only recent metrics
        for key in self.performance_metrics:
            if len(self.performance_metrics[key]) > 20:
                self.performance_metrics[key] = self.performance_metrics[key][-20:]
    
    def _generate_health_recommendations(
        self, 
        health_status: str, 
        metrics: Dict[str, Any], 
        error_summary: Dict[str, Any]
    ) -> List[str]:
        """Generate health recommendations"""
        recommendations = []
        
        if health_status == "inactive":
            recommendations.append("Agent has been inactive for more than 5 minutes")
            recommendations.append("Check if the agent service is running properly")
        
        if error_summary["error_rate"] > 10:
            recommendations.append("High error rate detected - review recent errors")
            recommendations.append("Consider implementing better error handling")
        
        if metrics["avg_processing_time"] > 30:
            recommendations.append("Slow processing detected - optimize tool execution")
            recommendations.append("Consider caching frequently accessed data")
        
        if metrics["success_rate"] < 80:
            recommendations.append("Low success rate - review task execution logic")
            recommendations.append("Check tool availability and data integrity")
        
        if not recommendations:
            recommendations.append("Agent is performing well - no immediate action needed")
        
        return recommendations
    
    def reset_metrics(self):
        """Reset all monitoring metrics"""
        self.start_time = datetime.now()
        self.last_activity = datetime.now()
        self.task_completions = []
        self.error_log = []
        self.performance_metrics = {
            "processing_times": [],
            "success_rates": [],
            "error_rates": []
        }
    
    def export_metrics(self, format: str = "json") -> str:
        """Export monitoring metrics"""
        data = {
            "uptime": self.get_uptime(),
            "last_activity": self.get_last_activity(),
            "performance_metrics": self.get_performance_metrics(),
            "task_type_performance": self.get_task_type_performance(),
            "error_summary": self.get_error_summary(),
            "health_status": self.get_health_status()
        }
        
        if format.lower() == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format}") 