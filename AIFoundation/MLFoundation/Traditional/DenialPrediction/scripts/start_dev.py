#!/usr/bin/env python3
"""
Development startup script
Starts the healthcare denial prediction system in development mode
"""

import os
import sys
import subprocess
import time
import requests
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    logger.info("Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import streamlit
        import pandas
        import numpy
        import xgboost
        import mlflow
        logger.info("✅ All Python dependencies are installed")
    except ImportError as e:
        logger.error(f"❌ Missing dependency: {e}")
        logger.info("Please install dependencies with: pip install -r requirements.txt")
        return False
    
    return True

def check_services():
    """Check if required services are running"""
    logger.info("Checking services...")
    
    services = {
        "PostgreSQL": ("localhost", 5432),
        "Redis": ("localhost", 6379),
        "MLflow": ("localhost", 5000)
    }
    
    for service_name, (host, port) in services.items():
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                logger.info(f"✅ {service_name} is running on {host}:{port}")
            else:
                logger.warning(f"⚠️ {service_name} is not running on {host}:{port}")
                logger.info(f"Start with: docker-compose up {service_name.lower()}")
        except Exception as e:
            logger.error(f"❌ Error checking {service_name}: {e}")
    
    return True

def start_api_server():
    """Start the FastAPI server"""
    logger.info("Starting API server...")
    
    try:
        # Change to project root
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        
        # Start API server
        cmd = [
            sys.executable, "-m", "uvicorn",
            "api.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        
        logger.info(f"Running: {' '.join(cmd)}")
        
        # Start in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for server to start
        time.sleep(5)
        
        # Check if server is running
        try:
            response = requests.get("http://localhost:8000/health", timeout=10)
            if response.status_code == 200:
                logger.info("✅ API server is running on http://localhost:8000")
                return process
            else:
                logger.error("❌ API server failed to start properly")
                return None
        except requests.exceptions.RequestException:
            logger.error("❌ API server is not responding")
            return None
            
    except Exception as e:
        logger.error(f"❌ Failed to start API server: {e}")
        return None

def start_dashboard():
    """Start the Streamlit dashboard"""
    logger.info("Starting Streamlit dashboard...")
    
    try:
        # Change to project root
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        
        # Start Streamlit
        cmd = [
            sys.executable, "-m", "streamlit",
            "run", "dashboard/app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ]
        
        logger.info(f"Running: {' '.join(cmd)}")
        
        # Start in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for dashboard to start
        time.sleep(10)
        
        logger.info("✅ Streamlit dashboard is running on http://localhost:8501")
        return process
        
    except Exception as e:
        logger.error(f"❌ Failed to start dashboard: {e}")
        return None

def initialize_database():
    """Initialize the database with sample data"""
    logger.info("Initializing database...")
    
    try:
        # Change to project root
        project_root = Path(__file__).parent.parent
        os.chdir(project_root)
        
        # Run database initialization
        cmd = [sys.executable, "scripts/init_db.py"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ Database initialized successfully")
            return True
        else:
            logger.error(f"❌ Database initialization failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        return False

def main():
    """Main startup function"""
    logger.info("🚀 Starting Healthcare Denial Prediction System...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check services
    check_services()
    
    # Initialize database
    if not initialize_database():
        logger.warning("⚠️ Database initialization failed, continuing anyway...")
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        logger.error("❌ Failed to start API server")
        sys.exit(1)
    
    # Start dashboard
    dashboard_process = start_dashboard()
    if not dashboard_process:
        logger.error("❌ Failed to start dashboard")
        api_process.terminate()
        sys.exit(1)
    
    logger.info("🎉 System started successfully!")
    logger.info("📊 Dashboard: http://localhost:8501")
    logger.info("🔌 API: http://localhost:8000")
    logger.info("📚 API Docs: http://localhost:8000/docs")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if api_process.poll() is not None:
                logger.error("❌ API server stopped unexpectedly")
                break
                
            if dashboard_process.poll() is not None:
                logger.error("❌ Dashboard stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down...")
        
        # Terminate processes
        if api_process:
            api_process.terminate()
        if dashboard_process:
            dashboard_process.terminate()
        
        logger.info("✅ System shut down successfully")

if __name__ == "__main__":
    main() 