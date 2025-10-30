@echo off
REM Team Management Dashboard - Startup Script (Windows)

echo Starting Team Management Dashboard...

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo No .env file found. Copying from .env.example...
    copy .env.example .env
    echo Please edit .env file with your configuration
)

REM Run the application
echo Starting Flask application...
python app.py

pause
