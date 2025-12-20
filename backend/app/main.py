from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional
import uuid
from app.orchestrator import WorkflowOrchestrator, StreamingOrchestrator
from app.utils.logger import get_logger
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

orchestrator = WorkflowOrchestrator()
streaming_orchestrator = StreamingOrchestrator()

# Request Model
class DebugRequest(BaseModel):
    code: str
    language: str = "python"
    context: Optional[str] = None

@app.get("/")
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "multi-agent-debugger", "version": "2.0.0"}

@app.post("/debug")
async def debug_code(request: DebugRequest):
    """
    Main endpoint for code debugging (non-streaming)
    Returns complete JSON with all agent outputs
    """
    request_id = str(uuid.uuid4())
    logger.info(f"API - Debug request: {request_id}")
    logger.info(f"API - Code: {request.code[:100]}...")
    
    try:
        result = await orchestrator.execute_workflow(
            request_id=request_id,
            code=request.code,
            language=request.language,
            context=request.context
        )
        logger.info(f"API - Completed: {result.get('workflow_status')}")
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"API - Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/debug/stream")
async def debug_code_stream(request: DebugRequest):
    """
    Streaming endpoint for real-time debugging updates (SSE)
    """
    request_id = str(uuid.uuid4())
    logger.info(f"API - Streaming request received: {request_id}")
    logger.info(f"API - Code length: {len(request.code)} chars")
    
    async def generate():
        logger.info(f"API - Starting stream for {request_id}")
        try:
            async for event in streaming_orchestrator.execute_workflow_streaming(
                request_id=request_id,
                code=request.code,
                language=request.language,
                context=request.context
            ):
                logger.debug(f"API - Yielding event: {event[:100]}...")
                yield event
            logger.info(f"API - Stream completed for {request_id}")
        except Exception as e:
            logger.error(f"API - Stream error: {str(e)}")
            yield f"data: {{\"type\":\"error\",\"message\":\"{str(e)}\"}}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*"
        }
    )

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
