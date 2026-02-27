@echo off
REM ============================================
REM Quick Start Script - Windows
REM AI Image & Document Metadata Application
REM ============================================

echo.
echo ============================================
echo AI Metadata Application - Quick Start
echo ============================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not running.
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo [1/4] Stopping any existing containers...
docker-compose down

echo.
echo [2/4] Building the application (this may take a few minutes)...
docker-compose build

echo.
echo [3/4] Starting MongoDB and the application...
docker-compose up -d

echo.
echo [4/4] Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo ============================================
echo READY!
echo ============================================
echo.
echo Open your browser and go to:
echo http://127.0.0.1:5000
echo.
echo To stop the application, run: STOP_WINDOWS.bat
echo.
echo To view logs, run: docker-compose logs -f
echo.
pause
