#!/usr/bin/env python3
"""
Build script for Healthcare Denial Prediction System
Sets up the development environment and builds the system
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(cmd, description, check=True):
    """Run a command and log the result"""
    logger.info(f"Running: {description}")
    logger.info(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        if result.stdout:
            logger.info(f"Output: {result.stdout}")
        if result.stderr:
            logger.warning(f"Stderr: {result.stderr}")
        logger.info(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed: {e}")
        if e.stdout:
            logger.error(f"Stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"Stderr: {e.stderr}")
        if check:
            raise
        return e

def check_python_version():
    """Check Python version"""
    logger.info("Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        logger.error(f"❌ Python 3.9+ required, found {version.major}.{version.minor}")
        return False
    
    logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    logger.info("Installing Python dependencies...")
    
    cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    return run_command(cmd, "Installing dependencies")

def setup_database():
    """Set up the database"""
    logger.info("Setting up database...")
    
    # Check if PostgreSQL is running
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="healthcare_denials",
            user="user",
            password="password"
        )
        conn.close()
        logger.info("✅ Database connection successful")
    except Exception as e:
        logger.warning(f"⚠️ Database not available: {e}")
        logger.info("Please start PostgreSQL with: docker-compose up postgres")
        return False
    
    # Initialize database
    cmd = [sys.executable, "scripts/init_db.py"]
    return run_command(cmd, "Initializing database", check=False)

def build_docker_images():
    """Build Docker images"""
    logger.info("Building Docker images...")
    
    # Build API image
    cmd = ["docker", "build", "-t", "healthcare-denial-api:latest", "."]
    run_command(cmd, "Building API Docker image", check=False)
    
    # Build dashboard image
    cmd = ["docker", "build", "-t", "healthcare-denial-dashboard:latest", "-f", "dashboard/Dockerfile", "."]
    run_command(cmd, "Building dashboard Docker image", check=False)

def run_tests():
    """Run basic tests"""
    logger.info("Running tests...")
    
    cmd = [sys.executable, "tests/test_basic.py"]
    return run_command(cmd, "Running basic tests", check=False)

def main():
    """Main build function"""
    logger.info("🔨 Building Healthcare Denial Prediction System...")
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Setup database
    setup_database()
    
    # Build Docker images
    build_docker_images()
    
    # Run tests
    run_tests()
    
    logger.info("🎉 Build completed successfully!")
    logger.info("")
    logger.info("Next steps:")
    logger.info("1. Start services: docker-compose up -d")
    logger.info("2. Start development: python scripts/start_dev.py")
    logger.info("3. Access dashboard: http://localhost:8501")
    logger.info("4. Access API docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 