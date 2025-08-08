import subprocess
import sys


def run_tests():
    """Run pytest with coverage"""
    try:
        # Run tests with coverage
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing"
        ], check=True)
        
        print("✅ All tests passed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with exit code {e.returncode}")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
