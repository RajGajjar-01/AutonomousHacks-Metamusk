#!/bin/bash

# Start the FastAPI server using uv
echo "Starting Multi-Agent Debugger API..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
