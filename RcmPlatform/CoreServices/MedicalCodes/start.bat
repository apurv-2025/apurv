@echo off
REM Medical Codes Application Startup Script for Windows

echo 🚀 Starting Medical Codes Application...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not installed. Please install it first.
    pause
    exit /b 1
)

echo 📦 Starting services with Docker Compose...
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

echo 🔍 Testing application...
python test_app.py

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Application started successfully!
    echo.
    echo Access the application at:
    echo   Frontend: http://localhost:3000
    echo   Backend API: http://localhost:8000
    echo   API Documentation: http://localhost:8000/docs
    echo.
    echo To stop the application, run: docker-compose down
) else (
    echo.
    echo ❌ Application failed to start properly.
    echo Check the logs with: docker-compose logs
    pause
    exit /b 1
)

pause 