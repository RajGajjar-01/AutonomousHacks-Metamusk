# Multi-Agent Code Debugger

An AI-powered code debugging system that uses multiple specialized agents to analyze, fix, and validate code automatically.

## Features

- 🔍 **Automatic Bug Detection** - Scanner agent identifies issues in your code
- 🔧 **Smart Code Fixes** - Fixer agent generates solutions
- ✅ **Validation & Testing** - Validator agent ensures fixes work correctly
- 🎨 **Modern UI** - Beautiful React frontend with DaisyUI
- ⚡ **Real-time Streaming** - Live updates as agents work
- 🌓 **Dark/Light Mode** - Theme switching support

## Quick Start

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

4. Verify setup:
   ```bash
   uv run python check_setup.py
   ```

5. Start the server:
   ```bash
   ./start.sh
   ```
   The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`

## Usage

1. Open the frontend in your browser
2. Select your programming language (Python, JavaScript, Java, C++, Go)
3. Paste or write your code in the editor
4. Optionally add context about what the code should do
5. Click "Debug Code" and watch the agents work!

## Architecture

### Backend (FastAPI)
- **Scanner Agent** - Analyzes code for bugs and issues
- **Fixer Agent** - Generates fixes for identified problems
- **Validator Agent** - Tests and validates the fixes
- **Orchestrator** - Coordinates agent workflow with streaming support

### Frontend (React + Vite)
- Monaco Editor for code editing
- Real-time SSE streaming for live updates
- DaisyUI components for beautiful UI
- Theme switching (dark/light mode)

## Tech Stack

**Backend:**
- FastAPI
- Google Gemini AI
- Groq (optional)
- Python 3.13+

**Frontend:**
- React 19
- Vite
- TailwindCSS 4
- DaisyUI
- Monaco Editor

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /debug` - Debug code (complete JSON response)
- `POST /debug/stream` - Debug code with streaming (SSE)

## License

MIT
