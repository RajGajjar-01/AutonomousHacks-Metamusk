"""
Scanner Agent Tools - Reusable tools for code analysis
"""
import json
import ast
from langchain_core.tools import tool


@tool
def analyze_python_syntax(code: str) -> str:
    """
    Analyze Python code for syntax errors using AST parsing.
    
    IMPORTANT: This ONLY checks if the code is syntactically valid (can be parsed).
    It does NOT check for runtime errors like IndexError, KeyError, TypeError, or logic errors.
    """
    try:
        ast.parse(code)
        return json.dumps({
            "valid": True,
            "errors": []
        })
    except SyntaxError as e:
        return json.dumps({
            "valid": False,
            "errors": [{
                "type": "SyntaxError",
                "message": str(e.msg),
                "line_number": e.lineno,
                "column": e.offset
            }]
        })


@tool
def find_undefined_variables(code: str) -> str:
    """
    Find undefined variables in Python code that may cause NameError at runtime.
    
    Args:
        code: The Python source code to analyze
    
    Returns:
        JSON string with list of undefined variable names
    """
    try:
        tree = ast.parse(code)
        defined = set()
        used = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    defined.add(node.id)
                elif isinstance(node.ctx, ast.Load):
                    used.add(node.id)
        
        # Filter out builtins
        builtins = set(dir(__builtins__))
        undefined = list(used - defined - builtins)
        
        return json.dumps({"undefined_variables": undefined})
    except:
        return json.dumps({"undefined_variables": []})


@tool
def check_code_quality_issues(code: str) -> str:
    """
    Check for code quality issues like unused imports and bare exceptions.
    
    Args:
        code: The Python source code to check
    
    Returns:
        JSON string with list of quality warnings
    """
    warnings = []
    
    try:
        tree = ast.parse(code)
        
        # Check for unused imports
        imports = set()
        used_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.asname or alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.add(alias.asname or alias.name)
            elif isinstance(node, ast.Name):
                used_names.add(node.id)
        
        unused = imports - used_names
        for imp in unused:
            warnings.append({
                "type": "UnusedImport",
                "message": f"Import '{imp}' is unused",
                "suggestion": "Remove unused import"
            })
        
        # Check for bare except
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    warnings.append({
                        "type": "BareExcept",
                        "line_number": node.lineno,
                        "message": "Bare except clause",
                        "suggestion": "Specify exception type"
                    })
    except:
        pass
    
    return json.dumps({"warnings": warnings})


@tool
def count_code_lines(code: str) -> str:
    """
    Count different types of lines in code.
    
    Args:
        code: The source code to analyze
    
    Returns:
        JSON string with line counts
    """
    lines = code.split('\n')
    return json.dumps({
        "total": len(lines),
        "non_empty": len([l for l in lines if l.strip()]),
        "comments": len([l for l in lines if l.strip().startswith('#')])
    })
