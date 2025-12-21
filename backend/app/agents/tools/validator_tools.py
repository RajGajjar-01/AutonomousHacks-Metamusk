"""
Validator Agent Tools - Reusable tools for code validation
"""
import json
import ast
from langchain_core.tools import tool


@tool
def compare_code_syntax(original_code: str, fixed_code: str) -> str:
    """
    Compare syntax validity between original and fixed code.
    
    Args:
        original_code: The original code
        fixed_code: The fixed code
    
    Returns:
        JSON string with comparison results
    """
    original_valid = True
    fixed_valid = True
    
    try:
        ast.parse(original_code)
    except SyntaxError:
        original_valid = False
    
    try:
        ast.parse(fixed_code)
    except SyntaxError:
        fixed_valid = False
    
    return json.dumps({
        "original_valid": original_valid,
        "fixed_valid": fixed_valid,
        "improvement": fixed_valid and not original_valid
    })


@tool
def check_undefined_variables_in_code(code: str) -> str:
    """
    Check for undefined variables in Python code.
    
    Args:
        code: The Python code to check
    
    Returns:
        JSON string with undefined variables count and list
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
        
        builtins = set(dir(__builtins__))
        undefined = list(used - defined - builtins)
        
        return json.dumps({
            "undefined_count": len(undefined),
            "undefined_variables": undefined
        })
    except:
        return json.dumps({
            "undefined_count": 0,
            "undefined_variables": []
        })


@tool
def calculate_improvement_score(original_errors: int, fixed_errors: int) -> str:
    """
    Calculate improvement percentage between original and fixed code.
    
    Args:
        original_errors: Number of errors in original code
        fixed_errors: Number of errors in fixed code
    
    Returns:
        JSON string with improvement score
    """
    if original_errors == 0:
        improvement = 100 if fixed_errors == 0 else 0
    else:
        improvement = ((original_errors - fixed_errors) / original_errors) * 100
    
    return json.dumps({
        "improvement_percentage": max(0, improvement),
        "errors_fixed": max(0, original_errors - fixed_errors)
    })


@tool
def compare_code_structure(original_code: str, fixed_code: str) -> str:
    """
    Compare the structure of original and fixed code.
    
    Args:
        original_code: The original code
        fixed_code: The fixed code
    
    Returns:
        JSON string with structure comparison
    """
    def get_structure(code):
        try:
            tree = ast.parse(code)
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
            
            return {"functions": functions, "classes": classes}
        except:
            return {"functions": [], "classes": []}
    
    original_structure = get_structure(original_code)
    fixed_structure = get_structure(fixed_code)
    
    return json.dumps({
        "original": original_structure,
        "fixed": fixed_structure,
        "structure_preserved": original_structure == fixed_structure
    })
