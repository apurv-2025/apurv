# Performance optimization script
# scripts/optimize_performance.py
"""
Performance optimization script for FastAPI Task Management System
"""
import subprocess
import os
import sys
from pathlib import Path


def optimize_database():
    """Optimize database performance"""
    print("🔧 Optimizing database...")
    
    # Run VACUUM and ANALYZE
    commands = [
        "docker-compose exec -T postgres psql -U taskuser -d taskmanager -c 'VACUUM ANALYZE;'",
        "docker-compose exec -T postgres psql -U taskuser -d taskmanager -c 'REINDEX DATABASE taskmanager;'"
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"✅ Executed: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {cmd} - {e}")


def optimize_docker():
    """Optimize Docker containers"""
    print("🐳 Optimizing Docker containers...")
    
    commands = [
        "docker system prune -f",  # Remove unused containers, networks, images
        "docker volume prune -f",  # Remove unused volumes
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"✅ Executed: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {cmd} - {e}")


def check_system_resources():
    """Check system resource usage"""
    print("📊 Checking system resources...")
    
    commands = [
        "docker stats --no-stream",
        "df -h",
        "free -h"
    ]
    
    for cmd in commands:
        try:
            print(f"\n--- {cmd} ---")
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {cmd} - {e}")


def setup_monitoring():
    """Set up basic monitoring"""
    print("📈 Setting up monitoring...")
    
    # Create monitoring script
    monitoring_script = """#!/bin/bash
# Simple monitoring script for Task Management System

LOG_FILE="/var/log/taskmanager-monitor.log"

log() {
    echo "[$(date)] $1" >> $LOG_FILE
}

# Check if services are running
if ! curl -f http://localhost:8000/health >/dev/null 2>&1; then
    log "ERROR: API health check failed"
    # Restart services
    docker-compose restart backend
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 85 ]; then
    log "WARNING: Disk usage is $DISK_USAGE%"
fi

# Check memory usage
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.2f", $3*100/$2}')
if (( $(echo "$MEMORY_USAGE > 85" | bc -l) )); then
    log "WARNING: Memory usage is $MEMORY_USAGE%"
fi

log "Monitor check completed"
"""
    
    with open("/tmp/monitor.sh", "w") as f:
        f.write(monitoring_script)
    
    # Make executable
    os.chmod("/tmp/monitor.sh", 0o755)
    print("✅ Monitoring script created at /tmp/monitor.sh")
    print("💡 Add to crontab with: */5 * * * * /tmp/monitor.sh")


if __name__ == "__main__":
    print("🚀 FastAPI Task Management System - Performance Optimization")
    print("=" * 60)
    
    optimize_database()
    optimize_docker()
    check_system_resources()
    setup_monitoring()
    
    print("\n✅ Performance optimization completed!")
    print("\n📋 Recommendations:")
    print("1. Monitor logs regularly: docker-compose logs -f")
    print("2. Set up automated backups")
    print("3. Configure log rotation")
    print("4. Set up alerting for critical issues")
    print("5. Regular security updates")

