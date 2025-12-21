import json
from datetime import datetime

class AgentPrompts:
    """Ultra-strict prompts to prevent false positives"""
    
    @staticmethod
    def scanner_prompt(code: str, language: str, request_id: str) -> str:
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        return f"""Analyze this {language} code for Syntax Errors AND Runtime Errors.

Code:
```
{code}
```

Rules:
1. Syntax Errors: Missing brackets, unclosed strings, etc.
2. Runtime Errors: Undefined variables (e.g. random text), invalid operations.
3. Warnings: Unused imports, unused variables, bare exceptions, etc.

Examples:
- `console.log("h")` -> VALID
- `rfjeoe` -> ERROR (NameError)
- `import os` (unused) -> WARNING
- `try: ... except:` -> WARNING

If code is valid, return total_errors: 0.
If code looks like random gibberish or undefined variables, report it as an ERROR.

Return JSON:
{{"agent_name":"Scanner","request_id":"{request_id}","status":"completed","errors":[],"warnings":[],"code_quality_score":10,"total_errors":0,"total_warnings":0,"timestamp":"{timestamp}"}}"""

    @staticmethod
    def fixer_prompt(original_code: str, language: str, scanner_output: dict, request_id: str) -> str:
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        escaped_code = json.dumps(original_code)
        
        return f"""You are a smart code repair agent. Detect and FIX the logic errors.
Output STRICT JSON. No markdown.

Code: {escaped_code}
Errors: {json.dumps(scanner_output.get("errors", []))}

INSTRUCTIONS:
1. Fix the error so the code RUNS.
2. If a variable is undefined (NameError), you must either:
   - Define it (e.g. `b = 0`)
   - OR Add it as a parameter (e.g. `def func(a, b):`)
3. DO NOT CHANGE CODE THAT IS ALREADY CORRECT. Be surgical.
4. Only fix the specific reported errors.
5. If the code is nonsense, rewrite it to be valid.

Return EXACTLY this JSON format (include diff details):
{{
    "agent_name": "Fixer",
    "request_id": "{request_id}",
    "status": "completed",
    "fixed_code": "<FULL_FIXED_CODE_STRING>",
    "changes": [
        {{
            "change_id": "FIX-1",
            "type": "correction",
            "line_number": 1,
            "original_line": "<ORIGINAL_LINE_CONTENT>",
            "fixed_line": "<NEW_LINE_CONTENT>",
            "reason": "<WHY_IT_WAS_CHANGED>"
        }}
    ],
    "explanation": "<SUMMARY_OF_FIXES>",
    "total_changes": 1,
    "timestamp": "{timestamp}"
}}"""

    @staticmethod
    def validator_prompt(original_code: str, fixed_code: str, language: str, 
                        scanner_output: dict, fixer_output: dict, request_id: str) -> str:
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        return f"""Validate the fix. Output STRICT JSON.
Original: {json.dumps(original_code)}
Fixed: {json.dumps(fixed_code)}

Return EXACTLY this JSON format:
{{
    "agent_name": "Validator",
    "request_id": "{request_id}",
    "status": "completed",
    "validation_status": "approved",
    "confidence_score": 1.0,
    "final_verdict": "approved",
    "approval_reason": "Fix validation successful",
    "requires_revision": false,
    "timestamp": "{timestamp}"
}}"""
