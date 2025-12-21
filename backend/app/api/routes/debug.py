"""Debug endpoints"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional
import uuid
import json

from app.graphs.debug_graph import invoke_debug_workflow, stream_debug_workflow
from app.core.logger import get_logger

logger = get_logger()
router = APIRouter(tags=["debug"])

# Request Model
class DebugRequest(BaseModel):
    code: str
    language: str = "python"
    context: Optional[str] = None
    max_iterations: Optional[int] = 3

@router.post("/debug")
async def debug_code(request: DebugRequest):
    """
    Main endpoint for code debugging using LangGraph workflow.
    
    This endpoint:
    1. Invokes the LangGraph debugging workflow
    2. Returns complete results after workflow completion
    
    The workflow includes:
    - Scanner: Analyzes code for errors
    - Fixer: Generates fixes for detected issues
    - Validator: Validates the fixes
    - Automatic retry logic with max iterations
    """
    request_id = str(uuid.uuid4())
    logger.info(f"API - Debug request: {request_id}")
    logger.info(f"API - Code length: {len(request.code)} chars")
    
    try:
        # Invoke LangGraph workflow
        result = await invoke_debug_workflow(
            request_id=request_id,
            code=request.code,
            language=request.language,
            context=request.context,
            max_iterations=request.max_iterations
        )
        
        logger.info(f"API - Completed: {result.get('workflow_status')}")
        
        # Format response
        response = {
            "request_id": result["request_id"],
            "workflow_status": result["workflow_status"],
            "success": result["success"],
            "message": result["message"],
            "original_code": result["code"],
            "final_code": result.get("final_code"),
            "language": result["language"],
            "context": result.get("context"),
            
            # Agent results
            "scanner_result": {
                "errors": result.get("errors"),
                "warnings": result.get("warnings"),
                "total_errors": result.get("total_errors"),
                "total_warnings": result.get("total_warnings"),
                "code_quality_score": result.get("code_quality_score")
            } if result.get("errors") is not None else None,
            
            "fixer_result": {
                "fixed_code": result.get("fixed_code"),
                "changes": result.get("fixes"),
                "explanation": result.get("explanation"),
                "total_changes": result.get("total_changes")
            } if result.get("fixed_code") is not None else None,
            
            "validator_result": result.get("validation_result"),
            
            # Metadata
            "metadata": result.get("metadata"),
            "events": result.get("events", []),
            
            # Summary
            "summary": {
                "errors_found": result.get("total_errors", 0),
                "errors_fixed": result.get("total_changes", 0),
                "warnings_found": result.get("total_warnings", 0),
                "validation_score": result.get("validation_result", {}).get("confidence_score", 0) if result.get("validation_result") else 0,
                "code_quality_before": result.get("code_quality_score", 0),
                "final_status": result["workflow_status"]
            }
        }
        
        return JSONResponse(content=response, status_code=200)
        
    except Exception as e:
        logger.error(f"API - Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/debug/stream")
async def debug_code_stream(request: DebugRequest):
    """
    Streaming endpoint for real-time debugging updates using LangGraph.
    
    This endpoint:
    1. Streams LangGraph workflow execution
    2. Sends SSE events as each node completes
    3. Provides real-time progress updates
    """
    request_id = str(uuid.uuid4())
    logger.info(f"API - Streaming request received: {request_id}")
    logger.info(f"API - Code length: {len(request.code)} chars")
    
    async def generate():
        logger.info(f"API - Starting stream for {request_id}")
        
        # Initialize accumulated state
        full_state = {
            "request_id": request_id,
            "code": request.code,
            "language": request.language,
            "context": request.context,
            "events": [],
            "metadata": {}
        }
        
        try:
            # Send initial connection event
            yield f"data: {json.dumps({'type': 'connected', 'request_id': request_id})}\n\n"
            
            # Stream LangGraph workflow
            async for state_update in stream_debug_workflow(
                request_id=request_id,
                code=request.code,
                language=request.language,
                context=request.context,
                max_iterations=request.max_iterations
            ):
                for node_name, node_update in state_update.items():
                    # Update full_state with new information
                    # Handle events accumulation
                    if "events" in node_update:
                        full_state["events"] = full_state.get("events", []) + node_update["events"]
                    
                    # Update other fields (excluding events which we handled)
                    update_dict = {k: v for k, v in node_update.items() if k != "events"}
                    full_state.update(update_dict)
                    
                    # Use full_state for constructing response
                    state = full_state # Reassign for downstream logic

                    # Map node name to agent name
                    agent_map = {
                        "scanner": "Scanner",
                        "fixer": "Fixer",
                        "validator": "Validator"
                    }
                    
                    agent_name = agent_map.get(node_name)
                    
                    # If this is an agent node, send agent_complete
                    if agent_name:
                        # Construct agent result based on node type
                        agent_result = {}
                        
                        if node_name == "scanner":
                            agent_result = {
                                "errors": state.get("errors"),
                                "warnings": state.get("warnings"),
                                "total_errors": state.get("total_errors"),
                                "total_warnings": state.get("total_warnings"),
                                "code_quality_score": state.get("code_quality_score")
                            }
                        elif node_name == "fixer":
                            agent_result = {
                                "fixed_code": state.get("fixed_code"),
                                "changes": state.get("fixes"),
                                "explanation": state.get("explanation"),
                                "total_changes": state.get("total_changes")
                            }
                        elif node_name == "validator":
                            agent_result = state.get("validation_result")
                        
                        # Send completion event
                        event_data = {
                            "type": "agent_complete",
                            "agent": agent_name,
                            "result": agent_result,
                            "message": f"{agent_name} analysis complete"
                        }
                        yield f"data: {json.dumps(event_data)}\n\n"
                    
                    # Check if workflow is complete (either finalize node or status completed)
                    if node_name == "finalize" or state.get("workflow_status") == "completed":
                        # Calculate total time if metadata is available
                        metadata = state.get("metadata", {})
                        total_time = metadata.get("total_time", 0)
                        iterations = metadata.get("iterations", state.get("iteration", 0))
                        
                        final_event = {
                            "type": "workflow_complete",
                            "result": {
                                "request_id": state.get("request_id"),
                                "success": state.get("success"),
                                "message": state.get("message"),
                                "final_code": state.get("final_code") or state.get("fixed_code") or state.get("code"),
                                "workflow_metadata": {
                                    "total_time": total_time,
                                    "iterations": iterations,
                                    "agents_involved": metadata.get("agents_involved", [])
                                },
                                "summary": {
                                    "errors_found": state.get("total_errors", 0),
                                    "errors_fixed": state.get("total_changes", 0),
                                    "validation_score": state.get("validation_result", {}).get("confidence_score", 0) if state.get("validation_result") else 0
                                },
                                "scanner_result": {
                                    "errors": state.get("errors", []),
                                    "warnings": state.get("warnings", []),
                                    "total_errors": state.get("total_errors", 0),
                                    "total_warnings": state.get("total_warnings", 0),
                                    "code_quality_score": state.get("code_quality_score")
                                } if state.get("total_errors") is not None else None,
                                "fixer_result": {
                                    "fixed_code": state.get("fixed_code"),
                                    "changes": state.get("fixes"),
                                    "explanation": state.get("explanation"),
                                    "total_changes": state.get("total_changes")
                                } if state.get("fixed_code") is not None else None,
                                "validator_result": state.get("validation_result")
                            }
                        }
                        yield f"data: {json.dumps(final_event)}\n\n"
            
            logger.info(f"API - Stream completed for {request_id}")
            
        except Exception as e:
            logger.error(f"API - Stream error: {str(e)}")
            error_event = {
                "type": "error",
                "message": str(e),
                "request_id": request_id
            }
            yield f"data: {json.dumps(error_event)}\n\n"
    
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
