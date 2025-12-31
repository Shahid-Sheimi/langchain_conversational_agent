#!/bin/bash
# Script to start the Streamlit frontend

echo "Starting PDF Chatbot Frontend..."
cd "$(dirname "$0")"
streamlit run frontend/app.py

