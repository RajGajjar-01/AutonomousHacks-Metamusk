"""
Node functions for the LangGraph debugging workflow.

Each node is an async function that:
1. Receives the current state
2. Performs its specific task using actual agents
3. Returns a dict with updated state fields
"""

from typing import Dict, Any
from datetime import datetime
from app.graphs.states import DebugState
from app.core.logger import get_logger

# Import simplified function-based agents
from app.agents import (
    scanner_agent,
    fixer_agent,
    validator_agent
)

logger = get_logger()


async def scanner_node(state: DebugState) -> Dict[str, Any]:
    """
    Scanner Agent Node - Analyzes code for errors and issues.
    
    This node:
    1. Receives code from state
    2. Uses ScannerAgent to analyze for syntax errors, runtime errors, warnings
    3. Returns error details and quality score
    
    Args:
        state: Current workflow state
        
    Returns:
        Dict with scanner results to merge into state
    """
    logger.info(f"Scanner Node - Processing request {state['request_id']}")
    
    try:
        # Extract input from state
        code = state["code"]
        language = state["language"]
        context = state.get("context", "")
        request_id = state["request_id"]
        
        # Execute simplified scanner agent (function-based)
        scanner_output = await scanner_agent({
            "request_id": request_id,
            "code": code,
            "language": language,
            "context": context
        })
        
        # Extract results
        errors = scanner_output.get("errors", [])
        warnings = scanner_output.get("warnings", [])
        total_errors = scanner_output.get("total_errors", 0)
        total_warnings = scanner_output.get("total_warnings", 0)
        code_quality_score = scanner_output.get("code_quality_score", 5.0)
        
        # Create event for trackin
        event = {
            "agent": "Scanner",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "scan_complete",
            "details": {
                "errors_found": total_errors,
                "warnings_found": total_warnings,
                "quality_score": code_quality_score,
                "is_runnable": scanner_output.get("is_runnable", total_errors == 0)
            }
        }
        
        logger.info(f"Scanner - Found {total_errors} errors, {total_warnings} warnings")
        
        # Return state updates
        return {
            "errors": errors,
            "warnings": warnings,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "code_quality_score": code_quality_score,
            "events": [event],
            "metadata": {
                **(state.get("metadata") or {}),
                "current_agent": "Scanner",
                "agents_involved": (state.get("metadata") or {}).get("agents_involved", []) + ["Scanner"]
            }
        }
        
    except Exception as e:
        logger.error(f"Scanner Node - Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "workflow_status": "failed",
            "success": False,
            "message": f"Scanner failed: {str(e)}",
            "events": [{
                "agent": "Scanner",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "action": "error",
                "details": {"error": str(e)}
            }]
        }


async def fixer_node(state: DebugState) -> Dict[str, Any]:
    """
    Fixer Agent Node - Generates fixes for detected errors.
    
    This node:
    1. Receives errors from scanner
    2. Uses FixerAgent to generate code fixes
    3. Returns fixed code and change details
    
    Args:
        state: Current workflow state
        
    Returns:
        Dict with fixer results to merge into state
    """
    logger.info(f"Fixer Node - Processing request {state['request_id']}")
    
    try:
        # Extract input from state
        code = state["code"]
        errors = state.get("errors", [])
        language = state["language"]
        request_id = state["request_id"]
        context = state.get("context", "")
        
        # Prepare scanner output for fixer
        scanner_output = {
            "errors": errors,
            "warnings": state.get("warnings", []),
            "total_errors": state.get("total_errors", 0),
            "total_warnings": state.get("total_warnings", 0)
        }
        
        # Execute simplified fixer agent (function-based)
        fixer_output = await fixer_agent({
            "request_id": request_id,
            "original_code": code,
            "language": language,
            "scanner_output": scanner_output,
            "context": context
        })
        
        # Extract results
        fixed_code = fixer_output.get("fixed_code", code)
        fixes = fixer_output.get("changes", [])
        total_changes = fixer_output.get("total_changes", 0)
        explanation = fixer_output.get("explanation", "")
        
        # Create event
        event = {
            "agent": "Fixer",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "fix_complete",
            "details": {
                "changes_made": total_changes,
                "explanation": explanation,
                "confidence": fixer_output.get("confidence_score", 0.8)
            }
        }
        
        logger.info(f"Fixer - Applied {total_changes} changes")
        
        # Return state updates
        return {
            "fixed_code": fixed_code,
            "fixes": fixes,
            "explanation": explanation,
            "total_changes": total_changes,
            "events": [event],
            "metadata": {
                **(state.get("metadata") or {}),
                "current_agent": "Fixer",
                "agents_involved": (state.get("metadata") or {}).get("agents_involved", []) + ["Fixer"]
            }
        }
        
    except Exception as e:
        logger.error(f"Fixer Node - Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "workflow_status": "failed",
            "success": False,
            "message": f"Fixer failed: {str(e)}",
            "events": [{
                "agent": "Fixer",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "action": "error",
                "details": {"error": str(e)}
            }]
        }


async def validator_node(state: DebugState) -> Dict[str, Any]:
    """
    Validator Agent Node - Validates fixed code.
    
    This node:
    1. Receives original and fixed code
    2. Uses ValidatorAgent to validate the fixes
    3. Determines if revision is needed
    4. Returns validation results
    
    Args:
        state: Current workflow state
        
    Returns:
        Dict with validator results to merge into state
    """
    logger.info(f"Validator Node - Processing request {state['request_id']}")
    
    try:
        # Extract input from state
        original_code = state["code"]
        fixed_code = state.get("fixed_code", original_code)
        fixes = state.get("fixes", [])
        language = state["language"]
        request_id = state["request_id"]
        iteration = state.get("iteration", 0)
        max_iterations = state.get("max_iterations", 3)
        
        # Prepare scanner and fixer outputs
        scanner_output = {
            "errors": state.get("errors", []),
            "warnings": state.get("warnings", []),
            "total_errors": state.get("total_errors", 0),
            "total_warnings": state.get("total_warnings", 0)
        }
        
        fixer_output = {
            "fixed_code": fixed_code,
            "changes": fixes,
            "total_changes": state.get("total_changes", 0),
            "explanation": state.get("explanation", "")
        }
        
        # Execute simplified validator agent (function-based)
        validator_output = await validator_agent({
            "request_id": request_id,
            "original_code": original_code,
            "fixed_code": fixed_code,
            "language": language,
            "scanner_output": scanner_output,
            "fixer_output": fixer_output
        })
        
        # Extract results
        validation_status = validator_output.get("validation_status", "approved")
        confidence_score = validator_output.get("confidence_score", 0.8)
        requires_revision = validator_output.get("requires_revision", False)
        
        # Override requires_revision if max iterations reached
        if iteration >= max_iterations:
            requires_revision = False
            validation_status = "approved_with_warnings"
        
        validation_result = {
            "status": validation_status,
            "confidence_score": confidence_score,
            "issues_found": validator_output.get("issues_found", []),
            "recommendations": validator_output.get("recommendations", []),
            "final_verdict": validator_output.get("final_verdict", "")
        }
        
        # Create event
        event = {
            "agent": "Validator",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "validation_complete",
            "details": {
                "status": validation_status,
                "confidence": confidence_score,
                "requires_revision": requires_revision,
                "iteration": iteration
            }
        }
        
        logger.info(f"Validator - Status: {validation_status}, Confidence: {confidence_score}")
        
        # Return state updates
        return {
            "validation_result": validation_result,
            "requires_revision": requires_revision,
            "events": [event],
            "metadata": {
                **(state.get("metadata") or {}),
                "current_agent": "Validator",
                "agents_involved": (state.get("metadata") or {}).get("agents_involved", []) + ["Validator"]
            }
        }
        
    except Exception as e:
        logger.error(f"Validator Node - Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "workflow_status": "failed",
            "success": False,
            "message": f"Validator failed: {str(e)}",
            "events": [{
                "agent": "Validator",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "action": "error",
                "details": {"error": str(e)}
            }]
        }


async def finalize_node(state: DebugState) -> Dict[str, Any]:
    """
    Finalize Node - Prepares final output.
    
    This node:
    1. Aggregates all results
    2. Generates summary
    3. Sets final status
    
    Args:
        state: Current workflow state
        
    Returns:
        Dict with final state updates
    """
    logger.info(f"Finalize Node - Processing request {state['request_id']}")
    
    try:
        # Determine final code
        final_code = state.get("fixed_code") or state["code"]
        
        # Determine success
        total_errors = state.get("total_errors") or 0
        validation_result = state.get("validation_result") or {}
        validation_status = validation_result.get("status", "unknown")
        
        success = (
            total_errors == 0 or 
            validation_status in ["approved", "approved_with_warnings"]
        )
        
        # Generate message
        if total_errors == 0:
            message = "No errors found in code!"
        elif success:
            message = "Code successfully debugged and validated!"
        else:
            message = "Debugging completed with warnings"
        
        # Update metadata
        end_time = datetime.utcnow().isoformat() + "Z"
        current_metadata = state.get("metadata") or {}
        start_time_str = current_metadata.get("start_time", end_time)
        
        # Calculate total time
        try:
            start_dt = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            total_time = round((end_dt - start_dt).total_seconds(), 2)
        except Exception as e:
            logger.warning(f"Failed to calculate total_time: {e}")
            total_time = 0.0
        
        metadata = {
            **current_metadata,
            "end_time": end_time,
            "total_time": total_time,
            "iterations": state.get("iteration", 0),
            "current_agent": None
        }
        
        # Create final event
        event = {
            "agent": "System",
            "timestamp": end_time,
            "action": "workflow_complete",
            "details": {
                "success": success,
                "message": message
            }
        }
        
        logger.info(f"Finalize - Workflow complete: {message}")
        
        return {
            "workflow_status": "completed",
            "success": success,
            "message": message,
            "final_code": final_code,
            "metadata": metadata,
            "events": [event]
        }
        
    except Exception as e:
        logger.error(f"Finalize Node - Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "workflow_status": "failed",
            "success": False,
            "message": f"Finalization failed: {str(e)}",
            "events": [{
                "agent": "System",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "action": "error",
                "details": {"error": str(e)}
            }]
        }
