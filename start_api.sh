#!/bin/bash
# Script to start the FastAPI backend server

echo "Starting PDF Chatbot API..."
cd "$(dirname "$0")"
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

