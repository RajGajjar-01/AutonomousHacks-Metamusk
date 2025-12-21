"""Utilities for SSE streaming"""
import json
from typing import Dict, Any

def create_sse_event(event_type: str, data: Dict[str, Any]) -> str:
    """
    Create a Server-Sent Event (SSE) formatted string
    
    Args:
        event_type: Type of event (e.g., 'agent_start', 'agent_complete')
        data: Event data dictionary
        
    Returns:
        SSE formatted string
    """
    event_data = {'type': event_type, **data}
    return f"data: {json.dumps(event_data)}\n\n"

def create_error_event(message: str, request_id: str = None) -> str:
    """
    Create an error SSE event
    
    Args:
        message: Error message
        request_id: Optional request ID
        
    Returns:
        SSE formatted error event
    """
    data = {"message": message}
    if request_id:
        data["request_id"] = request_id
    return create_sse_event("error", data)

def create_progress_event(agent: str, message: str, iteration: int = None) -> str:
    """
    Create a progress SSE event
    
    Args:
        agent: Agent name
        message: Progress message
        iteration: Optional iteration number
        
    Returns:
        SSE formatted progress event
    """
    data = {"agent": agent, "message": message}
    if iteration is not None:
        data["iteration"] = iteration
    return create_sse_event("agent_start", data)
