"""
Fixer Agent Tools - Reusable tools for code fixing
"""
import json
import ast
from langchain_core.tools import tool


@tool
def validate_python_syntax(code: str) -> str:
    """
    Validate Python code syntax.
    
    Args:
        code: The Python code to validate
    
    Returns:
        JSON string with validation result
    """
    try:
        ast.parse(code)
        return json.dumps({
            "valid": True,
            "message": "Syntax is valid"
        })
    except SyntaxError as e:
        return json.dumps({
            "valid": False,
            "error": str(e.msg),
            "line": e.lineno
        })


@tool
def apply_line_fix(code: str, line_number: int, new_line: str) -> str:
    """
    Apply a fix to a specific line in the code.
    
    Args:
        code: The original code
        line_number: Line number to fix (1-indexed)
        new_line: The new line content
    
    Returns:
        JSON string with the updated code
    """
    lines = code.split('\n')
    if 1 <= line_number <= len(lines):
        lines[line_number - 1] = new_line
        return json.dumps({
            "success": True,
            "fixed_code": '\n'.join(lines)
        })
    return json.dumps({
        "success": False,
        "error": "Invalid line number"
    })


@tool
def insert_code_line(code: str, line_number: int, new_line: str) -> str:
    """
    Insert a new line at a specific position.
    
    Args:
        code: The original code
        line_number: Position to insert (1-indexed)
        new_line: The line to insert
    
    Returns:
        JSON string with the updated code
    """
    lines = code.split('\n')
    if 0 <= line_number <= len(lines):
        lines.insert(line_number, new_line)
        return json.dumps({
            "success": True,
            "fixed_code": '\n'.join(lines)
        })
    return json.dumps({
        "success": False,
        "error": "Invalid line number"
    })


@tool
def remove_code_line(code: str, line_number: int) -> str:
    """
    Remove a specific line from the code.
    
    Args:
        code: The original code
        line_number: Line number to remove (1-indexed)
    
    Returns:
        JSON string with the updated code
    """
    lines = code.split('\n')
    if 1 <= line_number <= len(lines):
        lines.pop(line_number - 1)
        return json.dumps({
            "success": True,
            "fixed_code": '\n'.join(lines)
        })
    return json.dumps({
        "success": False,
        "error": "Invalid line number"
    })
