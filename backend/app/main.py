from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import debug, health
from app.core.logger import get_logger
from app.config import get_settings

settings = get_settings()
logger = get_logger()

app = FastAPI(
    title="Multi-Agent Debugger API",
    description="AI-powered multi-agent code debugging system with real-time streaming",
    version="2.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(health.router)
app.include_router(debug.router)

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
