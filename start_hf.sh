#!/bin/bash
# Startup script for Hugging Face Spaces deployment
# Runs both FastAPI backend and Streamlit frontend

set -e

# Function to handle cleanup
cleanup() {
    echo "Shutting down services..."
    kill $API_PID 2>/dev/null || true
    kill $STREAMLIT_PID 2>/dev/null || true
    exit
}

# Trap signals for graceful shutdown
trap cleanup SIGTERM SIGINT

# Start FastAPI backend in the background
echo "Starting FastAPI backend on port 8000..."
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Wait a moment for API to start
echo "Waiting for API to initialize..."
sleep 5

# Verify API is running
if ! kill -0 $API_PID 2>/dev/null; then
    echo "ERROR: FastAPI backend failed to start"
    exit 1
fi

echo "FastAPI backend is running (PID: $API_PID)"

# Start Streamlit frontend on port 7860 (Hugging Face Spaces default)
echo "Starting Streamlit frontend on port 7860..."
streamlit run frontend/app.py \
    --server.port=7860 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false &
STREAMLIT_PID=$!

# Wait for Streamlit to start
sleep 2

# Verify Streamlit is running
if ! kill -0 $STREAMLIT_PID 2>/dev/null; then
    echo "ERROR: Streamlit frontend failed to start"
    kill $API_PID 2>/dev/null || true
    exit 1
fi

echo "Streamlit frontend is running (PID: $STREAMLIT_PID)"
echo "Application is ready! Access it on port 7860"

# Wait for Streamlit (main process)
wait $STREAMLIT_PID
STREAMLIT_EXIT=$?

# If Streamlit exits, kill API and exit
kill $API_PID 2>/dev/null || true
exit $STREAMLIT_EXIT

