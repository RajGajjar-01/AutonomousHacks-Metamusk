"""
Agent Tools Package - Reusable LangChain tools for all agents
"""

# Scanner tools
from app.agents.tools.scanner_tools import (
    analyze_python_syntax,
    find_undefined_variables,
    check_code_quality_issues,
    count_code_lines
)

# Fixer tools
from app.agents.tools.fixer_tools import (
    validate_python_syntax,
    apply_line_fix,
    insert_code_line,
    remove_code_line
)

# Validator tools
from app.agents.tools.validator_tools import (
    compare_code_syntax,
    check_undefined_variables_in_code,
    calculate_improvement_score,
    compare_code_structure
)

__all__ = [
    # Scanner tools
    "analyze_python_syntax",
    "find_undefined_variables",
    "check_code_quality_issues",
    "count_code_lines",
    # Fixer tools
    "validate_python_syntax",
    "apply_line_fix",
    "insert_code_line",
    "remove_code_line",
    # Validator tools
    "compare_code_syntax",
    "check_undefined_variables_in_code",
    "calculate_improvement_score",
    "compare_code_structure",
]
