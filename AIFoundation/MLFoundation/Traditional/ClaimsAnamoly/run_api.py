#!/usr/bin/env python3
"""
API Server Runner for Claims Anomaly Detection System

This script starts the REST API server for the anomaly detection system.
"""

import sys
import os

# Add api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from api.app import app, load_model

if __name__ == "__main__":
    print("🚀 Starting Claims Anomaly Detection API Server")
    print("=" * 60)
    
    # Load model
    if load_model():
        print("✅ Model loaded successfully")
        print("🌐 API server starting on http://localhost:5001")
        print("📚 Available endpoints:")
        print("   GET  /health                    - Health check")
        print("   POST /api/v1/score              - Score single claim")
        print("   POST /api/v1/score/batch        - Score multiple claims")
        print("   GET  /api/v1/model/info         - Get model information")
        print("   GET  /api/v1/example            - Get example claim structure")
        print("\nPress Ctrl+C to stop the server")
        print("-" * 60)
        
        # Start the server
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to load model. Make sure to run the demo first:")
        print("   python3 run_demo.py")
        sys.exit(1) 