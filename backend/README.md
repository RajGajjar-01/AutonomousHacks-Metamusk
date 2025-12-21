# Multi-Agent Debugger Backend

AI-powered multi-agent code debugging system with real-time streaming capabilities.

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and settings
│   │
│   ├── api/                    # API layer
│   │   ├── __init__.py
│   │   ├── dependencies.py     # Dependency injection
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── debug.py        # Debug endpoints
│   │       └── health.py       # Health check endpoints
│   │
│   ├── agents/                 # AI Agents
│   │   ├── __init__.py
│   │   ├── base_agent.py       # Base agent class
│   │   ├── scanner_agent.py    # Code scanning agent
│   │   ├── fixer_agent.py      # Code fixing agent
│   │   ├── validator_agent.py  # Validation agent
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── code_tools.py   # Code analysis utilities
│   │
│   ├── graphs/                 # LangGraph workflows
│   │   ├── __init__.py
│   │   ├── states.py           # State definitions
│   │   ├── nodes.py            # Node functions
│   │   └── debug_graph.py      # Main workflow orchestration
│   │
│   ├── core/                   # Core utilities
│   │   ├── __init__.py
│   │   ├── ai_clients.py       # AI model clients (Gemini, Groq)
│   │   ├── prompts.py          # Agent prompts
│   │   ├── logger.py           # Logging configuration
│   │   └── exceptions.py       # Custom exceptions
│   │
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic schemas
│   │
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── streaming.py        # SSE streaming utilities
│       └── validators.py       # Validation utilities
│
├── scripts/                    # Utility scripts
│   ├── verify_setup.py         # Verify installation
│   ├── check_models.py         # Test AI model connectivity
│   └── test_agents.py          # Test individual agents
│
├── data/                       # Data storage
│   └── checkpoints/            # Workflow checkpoints
│       └── .gitkeep
│
├── logs/                       # Application logs
│   └── .gitkeep
│
├── .env                        # Environment variables (create from .env.example)
├── .env.example                # Example environment configuration
├── .gitignore
├── README.md
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project metadata
└── start.sh                   # Startup script
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using uv (recommended)
uv pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Required environment variables:
- `GEMINI_API_KEY` - Google Gemini API key
- `GROQ_API_KEY` - Groq API key

### 3. Verify Setup

```bash
# Run verification script
python scripts/verify_setup.py

# Test AI model connectivity
python scripts/check_models.py

# Test individual agents
python scripts/test_agents.py
```

### 4. Start Server

```bash
# Using the startup script
./start.sh

# Or directly with Python
python -m app.main

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Debug Code (Non-streaming)
```bash
POST /debug
Content-Type: application/json

{
  "code": "def add(a):\n    return a + b",
  "language": "python",
  "context": "optional context"
}
```

### Debug Code (Streaming)
```bash
POST /debug/stream
Content-Type: application/json

{
  "code": "def add(a):\n    return a + b",
  "language": "python"
}
```

Returns Server-Sent Events (SSE) with real-time updates.

## 🤖 Agent Architecture

### LangGraph Multi-Agent System

The system uses **LangGraph 0.2.x** for workflow orchestration with a sequential conditional routing pattern:

```
START → Scanner → [Conditional] → Fixer → Validator → [Conditional] → END
                      ↓                                      ↓
                     END                                  Fixer (retry)
```

**Key Features**:
- **State Management**: TypedDict with Annotated reducers for accumulating events
- **Conditional Routing**: Smart routing based on errors and validation results
- **Retry Logic**: Automatic retry with max iteration limits
- **Streaming Support**: Real-time updates via SSE
- **Checkpointing**: State persistence with MemorySaver

### Scanner Agent
- Analyzes code for syntax and runtime errors
- Identifies warnings and code quality issues
- Uses Groq API for fast analysis

### Fixer Agent
- Generates fixes for detected errors
- Provides detailed change explanations
- Uses Groq API for code generation

### Validator Agent
- Validates proposed fixes
- Ensures code correctness
- Provides confidence scores

## 🔧 Configuration

Edit `app/config.py` or set environment variables:

```python
# API Keys
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Models
GEMINI_MODEL=models/gemini-2.5-pro
GROQ_MODEL=llama-3.3-70b-versatile

# Workflow
MAX_ITERATIONS=3
```

## 🧪 Testing

```bash
# Test LangGraph workflow
python scripts/test_langgraph.py

# Quick test
python scripts/quick_test_graph.py

# Test all agents
python scripts/test_agents.py

# Test AI model connectivity
python scripts/check_models.py

# Verify complete setup
python scripts/verify_setup.py
```

## 📝 Development

### Adding New Agents

1. Create agent class in `app/agents/`
2. Inherit from `BaseAgent`
3. Implement `execute()` method
4. Add to workflow in `app/graphs/debug_graph.py`

### Adding New Endpoints

1. Create route file in `app/api/routes/`
2. Define router with `APIRouter()`
3. Include router in `app/main.py`

### Adding New Tools

1. Create tool functions in `app/agents/tools/`
2. Import and use in agent classes

## 🐛 Troubleshooting

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### API Key Issues
```bash
# Verify API keys are set
python scripts/check_models.py
```

### Port Already in Use
```bash
# Change port in .env
PORT=8001
```

## 📚 Documentation

- API Documentation: `http://localhost:8000/docs` (Swagger UI)
- ReDoc: `http://localhost:8000/redoc`

## 🔐 Security

- Never commit `.env` file
- Keep API keys secure
- Use environment variables for sensitive data
- Enable CORS only for trusted origins in production

## 📄 License

MIT License - See LICENSE file for details
