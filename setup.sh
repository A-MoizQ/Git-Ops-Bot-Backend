#!/bin/bash

# Exit on error
set -e

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found"
    exit 1
fi

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Setup complete! Virtual environment is activated."
echo "To run the FastAPI server, use: uvicorn main:app --reload"
