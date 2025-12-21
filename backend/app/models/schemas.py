"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# ========== API Request/Response Schemas ==========

class DebugRequest(BaseModel):
    """Request schema for debug endpoint"""
    code: str = Field(..., description="Code to debug")
    language: str = Field(default="python", description="Programming language")
    context: Optional[str] = Field(None, description="Additional context")
    max_iterations: Optional[int] = Field(default=3, description="Maximum retry iterations")


# ========== Scanner Agent Schemas ==========

class ErrorDetail(BaseModel):
    """Schema for individual error details"""
    error_id: str = Field(description="Unique error identifier (e.g., ERR-001)")
    type: str = Field(description="Error type (e.g., SyntaxError, NameError, TypeError)")
    severity: str = Field(description="Severity level: critical, high, medium, low")
    line_number: int = Field(description="Line number where error occurs")
    column: Optional[int] = Field(default=None, description="Column number if available")
    message: str = Field(description="Clear error message")
    suggestion: Optional[str] = Field(default=None, description="Suggested fix")


class WarningDetail(BaseModel):
    """Schema for individual warning details"""
    warning_id: str = Field(description="Unique warning identifier (e.g., WARN-001)")
    type: str = Field(description="Warning type (e.g., UnusedImport, BareExcept)")
    line_number: int = Field(description="Line number where warning occurs")
    message: str = Field(description="Warning message")
    suggestion: Optional[str] = Field(default=None, description="Suggested improvement")


class ScannerAnalysisOutput(BaseModel):
    """Structured output for complete scanner analysis"""
    errors: List[ErrorDetail] = Field(default_factory=list, description="List of errors found")
    warnings: List[WarningDetail] = Field(default_factory=list, description="List of warnings found")
    code_quality_score: float = Field(description="Code quality score from 0-10", ge=0, le=10)
    analysis_summary: str = Field(description="Brief summary of the analysis")
    is_runnable: bool = Field(description="Whether the code can run without errors")


# ========== Fixer Agent Schemas ==========

class ChangeDetail(BaseModel):
    """Schema for individual code change"""
    change_id: str = Field(description="Unique change identifier (e.g., FIX-001)")
    type: str = Field(description="Change type: correction, addition, removal, refactor")
    line_number: int = Field(description="Line number of the change")
    original_line: str = Field(description="Original line of code")
    fixed_line: str = Field(description="Fixed line of code")
    reason: str = Field(description="Explanation of why this change was made")


class FixerAnalysisOutput(BaseModel):
    """Structured output for complete fixer analysis"""
    fixed_code: str = Field(description="Complete fixed code")
    changes: List[ChangeDetail] = Field(default_factory=list, description="List of changes made")
    explanation: str = Field(description="Overall explanation of all fixes")
    confidence_score: float = Field(description="Confidence in fixes (0-1)", ge=0, le=1)
    alternative_approaches: List[str] = Field(default_factory=list, description="Alternative fix approaches considered")


# ========== Validator Agent Schemas ==========

class ValidationCheck(BaseModel):
    """Schema for individual validation check"""
    check_name: str = Field(description="Name of the validation check")
    passed: bool = Field(description="Whether the check passed")
    details: str = Field(description="Details about the check result")
    severity: str = Field(description="Severity if failed: critical, high, medium, low")


class ValidatorAnalysisOutput(BaseModel):
    """Structured output for complete validator analysis"""
    validation_status: str = Field(description="Status: approved, needs_revision, rejected")
    confidence_score: float = Field(description="Confidence in validation (0-1)", ge=0, le=1)
    checks_performed: List[ValidationCheck] = Field(default_factory=list, description="List of validation checks")
    issues_found: List[str] = Field(default_factory=list, description="List of issues found")
    recommendations: List[str] = Field(default_factory=list, description="List of recommendations")
    final_verdict: str = Field(description="Final verdict explanation")
    requires_revision: bool = Field(description="Whether code needs revision")
    improvement_summary: str = Field(description="Summary of improvements made")


# ========== Legacy Schemas (for backward compatibility) ==========

class WarningDetailLegacy(BaseModel):
    """Legacy schema for warning details"""
    warning_id: str
    type: str
    line_number: int
    message: str
    suggestion: Optional[str] = None

class ScannerOutput(BaseModel):
    """Schema for scanner agent output"""
    agent_name: str = "Scanner"
    request_id: str
    status: str
    errors: List[ErrorDetail] = []
    warnings: List[WarningDetail] = []
    total_errors: int = 0
    total_warnings: int = 0
    code_quality_score: float = 10.0
    timestamp: str
    execution_time: Optional[float] = None

class ChangeDetail(BaseModel):
    """Schema for code change details"""
    change_id: str
    type: str
    line_number: int
    original_line: str
    fixed_line: str
    reason: str

class FixerOutput(BaseModel):
    """Schema for fixer agent output"""
    agent_name: str = "Fixer"
    request_id: str
    status: str
    fixed_code: str
    changes: List[ChangeDetail] = []
    explanation: str
    total_changes: int = 0
    timestamp: str
    execution_time: Optional[float] = None

class ValidatorOutput(BaseModel):
    """Schema for validator agent output"""
    agent_name: str = "Validator"
    request_id: str
    status: str
    validation_status: str
    confidence_score: float
    final_verdict: str
    approval_reason: str
    requires_revision: bool
    timestamp: str
    execution_time: Optional[float] = None

class WorkflowMetadata(BaseModel):
    """Schema for workflow metadata"""
    iterations: int
    agents_involved: List[str]
    start_time: str
    end_time: Optional[str] = None
    total_time: Optional[float] = None

class WorkflowSummary(BaseModel):
    """Schema for workflow summary"""
    errors_found: int
    errors_fixed: int
    warnings_found: int
    validation_score: float
    code_quality_before: float
    improvement_percentage: float
    final_status: str

class DebugResponse(BaseModel):
    """Response schema for debug endpoint"""
    request_id: str
    workflow_status: str
    success: bool
    message: str
    original_code: str
    final_code: Optional[str] = None
    language: str
    context: Optional[str] = None
    scanner_result: Optional[Dict[str, Any]] = None
    fixer_result: Optional[Dict[str, Any]] = None
    validator_result: Optional[Dict[str, Any]] = None
    workflow_metadata: WorkflowMetadata
    summary: WorkflowSummary
