"""Code analysis and manipulation tools for agents"""
import ast
import re
from typing import List, Dict, Any, Optional

class CodeAnalyzer:
    """Tools for analyzing code structure and patterns"""
    
    @staticmethod
    def extract_functions(code: str, language: str = "python") -> List[Dict[str, Any]]:
        """
        Extract function definitions from code
        
        Args:
            code: Source code string
            language: Programming language
            
        Returns:
            List of function metadata dictionaries
        """
        if language == "python":
            try:
                tree = ast.parse(code)
                functions = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions.append({
                            "name": node.name,
                            "line_number": node.lineno,
                            "args": [arg.arg for arg in node.args.args]
                        })
                return functions
            except SyntaxError:
                return []
        return []
    
    @staticmethod
    def extract_imports(code: str, language: str = "python") -> List[str]:
        """
        Extract import statements from code
        
        Args:
            code: Source code string
            language: Programming language
            
        Returns:
            List of imported module names
        """
        if language == "python":
            try:
                tree = ast.parse(code)
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
                return imports
            except SyntaxError:
                return []
        return []
    
    @staticmethod
    def count_lines(code: str) -> Dict[str, int]:
        """
        Count different types of lines in code
        
        Args:
            code: Source code string
            
        Returns:
            Dictionary with line counts
        """
        lines = code.split('\n')
        return {
            "total": len(lines),
            "non_empty": len([l for l in lines if l.strip()]),
            "comments": len([l for l in lines if l.strip().startswith('#')])
        }

class CodeFormatter:
    """Tools for formatting and cleaning code"""
    
    @staticmethod
    def remove_trailing_whitespace(code: str) -> str:
        """Remove trailing whitespace from each line"""
        lines = code.split('\n')
        return '\n'.join(line.rstrip() for line in lines)
    
    @staticmethod
    def normalize_indentation(code: str, spaces: int = 4) -> str:
        """
        Normalize indentation to use consistent spacing
        
        Args:
            code: Source code string
            spaces: Number of spaces per indentation level
            
        Returns:
            Code with normalized indentation
        """
        lines = code.split('\n')
        normalized = []
        
        for line in lines:
            if not line.strip():
                normalized.append('')
                continue
            
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip())
            indent_level = leading_spaces // spaces
            
            # Reconstruct with normalized indentation
            normalized.append(' ' * (indent_level * spaces) + line.lstrip())
        
        return '\n'.join(normalized)

class CodeValidator:
    """Tools for validating code syntax and structure"""
    
    @staticmethod
    def check_syntax(code: str, language: str = "python") -> Dict[str, Any]:
        """
        Check code syntax validity
        
        Args:
            code: Source code string
            language: Programming language
            
        Returns:
            Dictionary with validation results
        """
        if language == "python":
            try:
                ast.parse(code)
                return {
                    "valid": True,
                    "error": None
                }
            except SyntaxError as e:
                return {
                    "valid": False,
                    "error": {
                        "message": str(e.msg),
                        "line": e.lineno,
                        "offset": e.offset
                    }
                }
        
        return {"valid": True, "error": None}
    
    @staticmethod
    def find_undefined_variables(code: str, language: str = "python") -> List[str]:
        """
        Find potentially undefined variables
        
        Args:
            code: Source code string
            language: Programming language
            
        Returns:
            List of undefined variable names
        """
        if language == "python":
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
                undefined = used - defined - builtins
                
                return list(undefined)
            except SyntaxError:
                return []
        
        return []
