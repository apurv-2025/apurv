#!/usr/bin/env python3
"""
Test Runner for Claims Anomaly Detection System

This script runs all unit tests for the system.
"""

import sys
import os
import subprocess

def run_tests():
    """Run all tests using pytest"""
    print("🧪 Running Claims Anomaly Detection System Tests")
    print("=" * 60)
    
    # Add src to path for imports
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        # Run pytest
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', '-v', '--tb=short'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Some tests failed (exit code: {result.returncode})")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 