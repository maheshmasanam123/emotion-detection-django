#!/usr/bin/env bash
# One-click setup for FaceMood on macOS / Linux.
set -e

if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] python3 is not installed. Install Python 3.10+ first."
    exit 1
fi

if [ ! -d .venv ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv .venv
fi

echo "[2/4] Activating virtualenv and installing dependencies..."
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "[3/4] Running database migrations..."
python manage.py migrate

echo "[4/4] Starting development server at http://127.0.0.1:8000/"
echo "Press Ctrl+C to stop."
python manage.py runserver
