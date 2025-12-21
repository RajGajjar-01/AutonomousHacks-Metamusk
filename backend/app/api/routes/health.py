"""Health check endpoints"""
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Multi-Agent Debugger API",
        "version": "2.0.0",
        "endpoints": {
            "debug": "POST /debug - Submit code for debugging (returns JSON)",
            "debug_stream": "POST /debug/stream - Submit code with real-time streaming (SSE)",
            "health": "GET /health - Health check"
        }
    }

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "multi-agent-debugger", "version": "2.0.0"}
