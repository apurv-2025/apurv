import subprocess
import sys
import os


def start_dev():
    """Start the development server with hot reload"""
    try:
        # Set environment variables
        os.environ["ENVIRONMENT"] = "development"
        os.environ["DEBUG"] = "True"
        
        # Start uvicorn with reload
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "debug"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Development server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")


if __name__ == "__main__":
    start_dev()

