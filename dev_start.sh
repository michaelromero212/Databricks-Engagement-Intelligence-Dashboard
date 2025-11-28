#!/bin/bash

# Databricks Engagement Intelligence - Dev Start Script

echo "Starting Backend..."
# Check if venv exists, else create
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r backend/requirements.txt

# Start backend in background
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Starting Frontend..."
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!

echo "Services started!"
echo "Backend: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"
echo "Press CTRL+C to stop both."

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT

wait
