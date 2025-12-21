"""
LangGraph debugging workflow implementation.

This module implements a multi-agent debugging system using LangGraph 0.2.x
with the following architecture:

Architecture Choice: Sequential with Conditional Routing
- Justification: The debugging workflow has a natural linear flow
  (scan → fix → validate) with conditional branches:
  * Skip fixer if no errors found
  * Loop back from validator to fixer for revisions
  * Exit after max iterations
  
This is more appropriate than:
- Supervisor Pattern: Overkill for a fixed 3-agent pipeline
- Hierarchical: No need for multi-level coordination

Graph Flow:
START → Scanner → [Conditional] → Fixer → Validator → [Conditional] → END
                      ↓                                      ↓
                     END                                  Fixer (retry)
"""

from typing import Literal, Dict, Any
from datetime import datetime

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.graphs.states import DebugState
from app.graphs.nodes import scanner_node, fixer_node, validator_node, finalize_node
from app.core.logger import get_logger

logger = get_logger()


# ========== Conditional Edge Functions ==========

def should_fix(state: DebugState) -> Literal["fixer", "finalize"]:
    """
    Routing logic after scanner.
    
    Decision:
    - If errors found → route to fixer
    - If no errors → skip to finalize
    
    Args:
        state: Current workflow state
        
    Returns:
        Next node name: "fixer" or "finalize"
    """
    total_errors = state.get("total_errors") or 0
    
    if total_errors > 0:
        logger.info(f"Router - {total_errors} errors found, routing to Fixer")
        return "fixer"
    else:
        logger.info("Router - No errors found, skipping to Finalize")
        return "finalize"


def should_retry(state: DebugState) -> Literal["fixer", "finalize"]:
    """
    Routing logic after validator.
    
    Decision:
    - If requires_revision AND iteration < max_iterations → retry fixer
    - Otherwise → finalize
    
    This implements the retry mechanism with a maximum iteration limit.
    
    Args:
        state: Current workflow state
        
    Returns:
        Next node name: "fixer" or "finalize"
    """
    requires_revision = state.get("requires_revision", False)
    iteration = state.get("iteration") or 0
    max_iterations = state.get("max_iterations") or 3
    
    if requires_revision and iteration < max_iterations:
        logger.info(f"Router - Revision needed, retry {iteration + 1}/{max_iterations}")
        return "fixer"
    else:
        if iteration >= max_iterations:
            logger.info(f"Router - Max iterations ({max_iterations}) reached, finalizing")
        else:
            logger.info("Router - Validation passed, finalizing")
        return "finalize"


# ========== Graph Construction ==========

def create_debug_graph() -> StateGraph:
    """
    Create and compile the debugging workflow graph.
    
    Graph Structure:
    
    ```
    START
      ↓
    Scanner (analyze code)
      ↓
    [Conditional: should_fix]
      ↓                    ↓
    Fixer              Finalize
      ↓                    ↓
    Validator             END
      ↓
    [Conditional: should_retry]
      ↓                    ↓
    Fixer (retry)      Finalize
      ↑___________________|  ↓
                           END
    ```
    
    Key Features:
    - Conditional routing based on errors and validation
    - Retry loop with max iteration limit
    - State persistence with MemorySaver checkpointer
    - Async node execution
    
    Returns:
        Compiled StateGraph ready for invocation
    """
    logger.info("Creating debug workflow graph")
    
    # Initialize graph with state schema
    workflow = StateGraph(DebugState)
    
    # Add nodes
    workflow.add_node("scanner", scanner_node)
    workflow.add_node("fixer", fixer_node)
    workflow.add_node("validator", validator_node)
    workflow.add_node("finalize", finalize_node)
    
    # Add edges
    # START → Scanner (always start with scanning)
    workflow.add_edge(START, "scanner")
    
    # Scanner → [Conditional] → Fixer or Finalize
    workflow.add_conditional_edges(
        "scanner",
        should_fix,
        {
            "fixer": "fixer",
            "finalize": "finalize"
        }
    )
    
    # Fixer → Validator (always validate after fixing)
    workflow.add_edge("fixer", "validator")
    
    # Validator → [Conditional] → Fixer (retry) or Finalize
    workflow.add_conditional_edges(
        "validator",
        should_retry,
        {
            "fixer": "fixer",
            "finalize": "finalize"
        }
    )
    
    # Finalize → END (workflow complete)
    workflow.add_edge("finalize", END)
    
    # Compile graph with checkpointer for state persistence
    # MemorySaver: In-memory checkpointing (use SQLite/Postgres for production)
    checkpointer = MemorySaver()
    compiled_graph = workflow.compile(checkpointer=checkpointer)
    
    logger.info("Debug workflow graph compiled successfully")
    
    return compiled_graph


# ========== Graph Instance ==========

# Create singleton graph instance
debug_graph = create_debug_graph()


# ========== Helper Functions ==========

async def invoke_debug_workflow(
    request_id: str,
    code: str,
    language: str = "python",
    context: str = None,
    max_iterations: int = 3
) -> Dict[str, Any]:
    """
    Invoke the debugging workflow with given inputs.
    
    This is a convenience function that:
    1. Prepares initial state
    2. Invokes the graph
    3. Returns final state
    
    Args:
        request_id: Unique request identifier
        code: Code to debug
        language: Programming language
        context: Optional context information
        max_iterations: Maximum retry iterations
        
    Returns:
        Final state dict with all results
        
    Example:
        ```python
        result = await invoke_debug_workflow(
            request_id="req-123",
            code="def add(a): return a + b",
            language="python"
        )
        print(result["success"])  # True/False
        print(result["final_code"])  # Fixed code
        ```
    """
    logger.info(f"Invoking debug workflow for request {request_id}")
    
    # Prepare initial state
    initial_state: DebugState = {
        "request_id": request_id,
        "code": code,
        "language": language,
        "context": context,
        
        # Initialize optional fields
        "errors": None,
        "warnings": None,
        "total_errors": None,
        "total_warnings": None,
        "code_quality_score": None,
        
        "fixed_code": None,
        "fixes": None,
        "explanation": None,
        "total_changes": None,
        
        "validation_result": None,
        "requires_revision": None,
        
        # Workflow control
        "iteration": 0,
        "max_iterations": max_iterations,
        "workflow_status": "in_progress",
        
        # Accumulated data
        "events": [],
        
        # Metadata
        "metadata": {
            "start_time": datetime.utcnow().isoformat() + "Z",
            "end_time": None,
            "total_time": None,
            "iterations": 0,
            "agents_involved": [],
            "current_agent": None
        },
        
        # Final output
        "success": False,
        "message": "",
        "final_code": None
    }
    
    # Configure graph execution
    config = {
        "configurable": {
            "thread_id": request_id  # Use request_id as thread_id for checkpointing
        }
    }
    
    try:
        # Invoke graph (async execution)
        final_state = await debug_graph.ainvoke(initial_state, config)
        
        logger.info(f"Workflow completed for request {request_id}: {final_state.get('workflow_status')}")
        
        return final_state
        
    except Exception as e:
        logger.error(f"Workflow failed for request {request_id}: {str(e)}")
        
        # Return error state
        return {
            **initial_state,
            "workflow_status": "failed",
            "success": False,
            "message": f"Workflow error: {str(e)}",
            "metadata": {
                **initial_state["metadata"],
                "end_time": datetime.utcnow().isoformat() + "Z"
            }
        }


async def stream_debug_workflow(
    request_id: str,
    code: str,
    language: str = "python",
    context: str = None,
    max_iterations: int = 3
):
    """
    Stream the debugging workflow with real-time updates.
    
    This function yields state updates as each node completes,
    enabling real-time progress tracking in the UI.
    
    Args:
        request_id: Unique request identifier
        code: Code to debug
        language: Programming language
        context: Optional context information
        max_iterations: Maximum retry iterations
        
    Yields:
        State dict after each node execution
        
    Example:
        ```python
        async for state in stream_debug_workflow(
            request_id="req-123",
            code="def add(a): return a + b"
        ):
            print(f"Current agent: {state['metadata']['current_agent']}")
            print(f"Events: {len(state['events'])}")
        ```
    """
    logger.info(f"Streaming debug workflow for request {request_id}")
    
    # Prepare initial state (same as invoke)
    initial_state: DebugState = {
        "request_id": request_id,
        "code": code,
        "language": language,
        "context": context,
        "errors": None,
        "warnings": None,
        "total_errors": None,
        "total_warnings": None,
        "code_quality_score": None,
        "fixed_code": None,
        "fixes": None,
        "explanation": None,
        "total_changes": None,
        "validation_result": None,
        "requires_revision": None,
        "iteration": 0,
        "max_iterations": max_iterations,
        "workflow_status": "in_progress",
        "events": [],
        "metadata": {
            "start_time": datetime.utcnow().isoformat() + "Z",
            "end_time": None,
            "total_time": None,
            "iterations": 0,
            "agents_involved": [],
            "current_agent": None
        },
        "success": False,
        "message": "",
        "final_code": None
    }
    
    config = {
        "configurable": {
            "thread_id": request_id
        }
    }
    
    try:
        # Stream graph execution
        async for state in debug_graph.astream(initial_state, config):
            # state is a dict with node name as key
            # e.g., {"scanner": {...updated_state...}}
            yield state
            
    except Exception as e:
        logger.error(f"Streaming workflow failed for request {request_id}: {str(e)}")
        yield {
            "error": {
                **initial_state,
                "workflow_status": "failed",
                "success": False,
                "message": f"Workflow error: {str(e)}"
            }
        }


# ========== Graph Visualization ==========

def get_graph_visualization() -> str:
    """
    Get Mermaid diagram of the graph structure.
    
    Returns:
        Mermaid diagram string
    """
    try:
        # LangGraph 0.2.x provides get_graph() method
        graph_repr = debug_graph.get_graph()
        return graph_repr.draw_mermaid()
    except Exception as e:
        logger.error(f"Failed to generate graph visualization: {str(e)}")
        return "Graph visualization not available"
