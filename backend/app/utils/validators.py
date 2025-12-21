"""Validation utilities"""
import json
from typing import Dict, Any, Optional

def validate_json_response(response: str) -> Dict[str, Any]:
    """
    Validate and parse JSON response from AI models
    
    Args:
        response: Raw response string
        
    Returns:
        Parsed JSON dictionary
        
    Raises:
        ValueError: If JSON is invalid
    """
    try:
        # Remove markdown code blocks if present
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        
        response = response.strip()
        
        # Parse JSON
        parsed = json.loads(response)
        return parsed
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {str(e)}")

def validate_code_language(language: str) -> bool:
    """
    Validate if the programming language is supported
    
    Args:
        language: Programming language name
        
    Returns:
        True if supported, False otherwise
    """
    supported_languages = [
        "python", "javascript", "typescript", "java", 
        "cpp", "c", "go", "rust", "ruby", "php"
    ]
    return language.lower() in supported_languages

def sanitize_code_input(code: str, max_length: int = 50000) -> str:
    """
    Sanitize code input
    
    Args:
        code: Input code string
        max_length: Maximum allowed length
        
    Returns:
        Sanitized code string
        
    Raises:
        ValueError: If code exceeds max length
    """
    if len(code) > max_length:
        raise ValueError(f"Code exceeds maximum length of {max_length} characters")
    
    return code.strip()
