@echo off
REM ============================================
REM Stop Script - Windows
REM ============================================

echo.
echo Stopping the AI Metadata Application...
echo.

docker-compose down

echo.
echo Application stopped successfully.
echo.
echo To start again, run: START_WINDOWS.bat
echo.
pause
