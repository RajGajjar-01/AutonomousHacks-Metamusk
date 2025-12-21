"""
State definitions for LangGraph debugging workflow.

This module defines the state schema using TypedDict with Annotated types
and reducer patterns following LangGraph 0.2.x best practices.
"""

from typing import TypedDict, Annotated, Optional, List, Dict, Any
from operator import add
from datetime import datetime


def add_messages(left: List[Dict[str, Any]], right: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Reducer function for accumulating messages/events.
    
    This follows the LangGraph pattern for state reducers, allowing
    multiple nodes to append to the same list without overwriting.
    
    Args:
        left: Existing list of messages
        right: New messages to add
        
    Returns:
        Combined list of messages
    """
    if not left:
        return right
    if not right:
        return left
    return left + right


def increment_counter(left: int, right: int) -> int:
    """
    Reducer function for incrementing counters.
    
    Args:
        left: Current counter value
        right: Value to add
        
    Returns:
        Sum of left and right
    """
    return (left or 0) + (right or 0)


class ErrorDetail(TypedDict):
    """Schema for individual error details."""
    error_id: str
    type: str
    severity: str
    line_number: int
    column: Optional[int]
    message: str
    suggestion: Optional[str]


class FixDetail(TypedDict):
    """Schema for individual fix details."""
    change_id: str
    type: str
    line_number: int
    original_line: str
    fixed_line: str
    reason: str


class ValidationResult(TypedDict):
    """Schema for validation results."""
    status: str  # "approved", "needs_revision", "rejected"
    confidence_score: float
    issues_found: List[str]
    recommendations: List[str]
    final_verdict: str


class WorkflowMetadata(TypedDict):
    """Schema for workflow execution metadata."""
    start_time: str
    end_time: Optional[str]
    total_time: Optional[float]
    iterations: int
    agents_involved: List[str]
    current_agent: Optional[str]


class DebugState(TypedDict):
    """
    Main state schema for the debugging workflow.
    
    This TypedDict defines all state fields that flow through the LangGraph.
    Uses Annotated types with reducers for fields that accumulate values.
    
    Key LangGraph Patterns:
    - Annotated[List, add_messages]: Accumulates messages without overwriting
    - Annotated[int, increment_counter]: Increments iteration counter
    - Optional fields: Allow nodes to selectively update state
    
    State Flow:
    1. Scanner populates: errors, warnings, code_quality_score
    2. Fixer populates: fixed_code, fixes, explanation
    3. Validator populates: validation_result, requires_revision
    """
    
    # ========== Input Fields ==========
    request_id: str
    code: str
    language: str
    context: Optional[str]
    
    # ========== Scanner Output ==========
    errors: Optional[List[ErrorDetail]]
    warnings: Optional[List[Dict[str, Any]]]
    total_errors: Optional[int]
    total_warnings: Optional[int]
    code_quality_score: Optional[float]
    
    # ========== Fixer Output ==========
    fixed_code: Optional[str]
    fixes: Optional[List[FixDetail]]
    explanation: Optional[str]
    total_changes: Optional[int]
    
    # ========== Validator Output ==========
    validation_result: Optional[ValidationResult]
    requires_revision: Optional[bool]
    
    # ========== Workflow Control ==========
    # Using Annotated with increment_counter reducer for iteration tracking
    iteration: Annotated[int, increment_counter]
    max_iterations: int
    workflow_status: str  # "in_progress", "completed", "failed"
    
    # ========== Accumulated Events ==========
    # Using Annotated with add_messages reducer to accumulate events
    events: Annotated[List[Dict[str, Any]], add_messages]
    
    # ========== Metadata ==========
    metadata: WorkflowMetadata
    
    # ========== Final Output ==========
    success: bool
    message: str
    final_code: Optional[str]


class DebugStateInput(TypedDict):
    """
    Input state schema for starting the workflow.
    
    This is a minimal schema containing only the required fields
    to initialize the workflow. The graph will populate other fields.
    """
    request_id: str
    code: str
    language: str
    context: Optional[str]


class DebugStateOutput(TypedDict):
    """
    Output state schema for the completed workflow.
    
    This defines the final state structure returned to the API.
    """
    request_id: str
    workflow_status: str
    success: bool
    message: str
    original_code: str
    final_code: Optional[str]
    language: str
    
    # Agent results
    scanner_result: Optional[Dict[str, Any]]
    fixer_result: Optional[Dict[str, Any]]
    validator_result: Optional[Dict[str, Any]]
    
    # Metadata
    metadata: WorkflowMetadata
    events: List[Dict[str, Any]]
    
    # Summary
    summary: Dict[str, Any]
