"""
Scanner Agent Tools - Reusable tools for code analysis
"""
import json
import ast
from langchain_core.tools import tool

class ScopeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.scopes = [set()]  # Stack of scopes (Global is index 0)
        self.undefined_vars = set()
        self.builtins = set(dir(__builtins__))
        self.used_vars = set()
        
    def visit_FunctionDef(self, node):
        self.scopes.append(set()) # New local scope
        # Add args to local scope
        for arg in node.args.args:
            self.scopes[-1].add(arg.arg)
        self.generic_visit(node)
        self.scopes.pop()
        # Function name is defined in enclosing scope
        self.scopes[-1].add(node.name)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.scopes.append(set()) # Class scope
        self.generic_visit(node)
        self.scopes.pop()
        # Class name is defined in enclosing scope
        self.scopes[-1].add(node.name)

    def visit_Import(self, node):
        for name in node.names:
            alias = name.asname or name.name.split('.')[0]
            self.scopes[-1].add(alias)

    def visit_ImportFrom(self, node):
        for name in node.names:
            alias = name.asname or name.name
            self.scopes[-1].add(alias)

    def visit_Global(self, node):
        # Variables declared global should be treated as writing to global scope (index 0)
        # But for 'defined' check, we just check global scope.
        pass

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.scopes[-1].add(node.id)
        elif isinstance(node.ctx, ast.Load):
            # Check LEGB rule (reverse iterate scopes)
            is_defined = False
            for scope in reversed(self.scopes):
                if node.id in scope:
                    is_defined = True
                    break
            
            if not is_defined and node.id not in self.builtins:
                self.undefined_vars.add(node.id)

@tool
def analyze_python_syntax(code: str) -> str:
    """
    Analyze Python code for syntax errors using AST parsing.
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
    Find undefined variables in Python code using scope-aware analysis.
    Safely handles local scopes, function arguments, and imports.
    """
    try:
        tree = ast.parse(code)
        visitor = ScopeVisitor()
        visitor.visit(tree)
        
        return json.dumps({
            "undefined_variables": list(visitor.undefined_vars)
        })
    except Exception as e:
        return json.dumps({"undefined_variables": [], "error": str(e)})

@tool
def check_code_quality_issues(code: str) -> str:
    """
    Check for code quality issues: unused imports, bare excepts, mutable default args.
    """
    warnings = []
    
    try:
        tree = ast.parse(code)
        
        # 1. Unused Imports Loop
        imports = {} # name -> lineno
        used_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname or alias.name
                    imports[name] = node.lineno
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname or alias.name
                    imports[name] = node.lineno
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
                
        unused = set(imports.keys()) - used_names
        for imp in unused:
            warnings.append({
                "type": "UnusedImport",
                "message": f"Import '{imp}' is unused",
                "line_number": imports[imp],
                "suggestion": "Remove unused import"
            })
            
        # 2. Other issues (Mutable defaults, Bare except)
        for node in ast.walk(tree):
            # Bare Except
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    warnings.append({
                        "type": "BareExcept",
                        "line_number": node.lineno,
                        "message": "Bare except clause used",
                        "suggestion": "Specify exception type (e.g. Exception)"
                    })
            
            # Mutable Default Args
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        warnings.append({
                            "type": "MutableDefaultArg",
                            "line_number": node.lineno,
                            "message": f"Mutable default argument in function '{node.name}'",
                            "suggestion": "Use None as default and initialize inside function"
                        })

    except Exception as e:
        pass
    
    return json.dumps({"warnings": warnings})

@tool
def count_code_lines(code: str) -> str:
    """Count code lines statistics."""
    lines = code.split('\n')
    return json.dumps({
        "total": len(lines),
        "non_empty": len([l for l in lines if l.strip()]),
        "comments": len([l for l in lines if l.strip().startswith('#')])
    })
