@echo off
REM One-click setup for FaceMood on Windows.
REM Creates a virtualenv, installs dependencies, runs migrations, and starts the dev server.

setlocal

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed or not on PATH.
    echo Install Python 3.10+ from https://www.python.org/downloads/ and re-run setup.bat
    exit /b 1
)

if not exist .venv (
    echo [1/4] Creating virtual environment...
    python -m venv .venv
)

echo [2/4] Activating virtualenv and installing dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency install failed.
    exit /b 1
)

echo [3/4] Running database migrations...
python manage.py migrate

echo [4/4] Starting development server at http://127.0.0.1:8000/
echo Press Ctrl+C to stop.
python manage.py runserver

endlocal
