# Multi-Agent Code Debugger - Backend

A FastAPI-based backend service that uses multiple AI agents to analyze, fix, and validate code.

## Setup

1. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Add your API keys:
     - `GEMINI_API_KEY` - Your Google Gemini API key
     - `GROQ_API_KEY` - Your Groq API key (optional)

3. **Verify setup:**
   ```bash
   uv run python check_setup.py
   ```

4. **Start the server:**
   ```bash
   ./start.sh
   ```
   
   The backend will run on `http://localhost:8000`

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /debug` - Debug code (returns complete JSON)
- `POST /debug/stream` - Debug code with streaming updates (SSE)

## Architecture

The system uses three specialized agents:
- **Scanner Agent** - Detects bugs and issues
- **Fixer Agent** - Generates code fixes
- **Validator Agent** - Validates the fixed code

All agents are orchestrated through a workflow system with real-time streaming support.
