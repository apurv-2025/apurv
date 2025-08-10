#!/usr/bin/env python3
"""
FastAPI Server Runner for Claims Anomaly Detection System

This script starts the FastAPI server for the anomaly detection system.
"""

import sys
import os
import uvicorn

# Add api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from api.fastapi_app import app, load_model

if __name__ == "__main__":
    print("🚀 Starting Claims Anomaly Detection FastAPI Server")
    print("=" * 60)
    
    # Load model
    if load_model():
        print("✅ Model loaded successfully")
        print("🌐 API server starting on http://localhost:8000")
        print("📚 Available endpoints:")
        print("   GET  /                           - API information")
        print("   GET  /health                     - Health check")
        print("   POST /api/v1/score               - Score single claim")
        print("   POST /api/v1/score/batch         - Score multiple claims")
        print("   GET  /api/v1/model/info          - Get model information")
        print("   GET  /api/v1/example             - Get example claim structure")
        print("   GET  /docs                       - Interactive API documentation")
        print("   GET  /redoc                      - Alternative API documentation")
        print("\nPress Ctrl+C to stop the server")
        print("-" * 60)
        
        # Start the server
        uvicorn.run(
            "api.fastapi_app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    else:
        print("❌ Failed to load model. Make sure to run the demo first:")
        print("   python3 run_demo.py")
        sys.exit(1) 