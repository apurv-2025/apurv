#!/usr/bin/env python3
"""
Demo Runner for Claims Anomaly Detection System

This script runs the complete anomaly detection system demonstration.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import main

if __name__ == "__main__":
    print("🚀 Starting Claims Anomaly Detection System Demo")
    print("=" * 60)
    main()
    print("\n✅ Demo completed successfully!") 