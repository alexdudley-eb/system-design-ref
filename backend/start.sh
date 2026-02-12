#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

if [ ! -f "system_design_ref.db" ]; then
    echo "Database not found. Running importer..."
    python import_data.py
fi

echo "Starting FastAPI server..."
uvicorn main:app --reload --port 8000
