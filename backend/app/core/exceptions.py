"""Custom exceptions for the application"""

class DebuggerException(Exception):
    """Base exception for debugger errors"""
    pass

class AIClientException(DebuggerException):
    """Exception for AI client errors"""
    pass

class AgentExecutionException(DebuggerException):
    """Exception for agent execution errors"""
    pass

class ValidationException(DebuggerException):
    """Exception for validation errors"""
    pass

class WorkflowException(DebuggerException):
    """Exception for workflow orchestration errors"""
    pass
