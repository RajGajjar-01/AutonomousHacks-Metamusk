from typing import Dict, Any
import json
from app.agents.base_agent import BaseAgent
from app.utils.ai_clients import groq_client
from app.utils.prompts import AgentPrompts
from app.utils.logger import get_logger

logger = get_logger()

class ValidatorAgent(BaseAgent):
    """Validator Agent - Verifies code fixes"""
    
    def __init__(self):
        super().__init__("Validator")
        self.ai_client = groq_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute validator agent
        
        Input JSON:
        {
            "request_id": "uuid",
            "original_code": "buggy code",
            "fixed_code": "fixed code",
            "language": "python",
            "scanner_output": { ... complete scanner JSON ... },
            "fixer_output": { ... complete fixer JSON ... }
        }
        
        Output JSON: Complete validator output as per schema
        """
        logger.info(f"Validator - Processing request {input_data.get('request_id')}")
        
        # Extract input
        request_id = input_data.get("request_id")
        original_code = input_data.get("original_code")
        fixed_code = input_data.get("fixed_code")
        language = input_data.get("language", "python")
        scanner_output = input_data.get("scanner_output", {})
        fixer_output = input_data.get("fixer_output", {})
        
        # Generate prompt with all previous outputs
        prompt = AgentPrompts.validator_prompt(
            original_code,
            fixed_code,
            language,
            scanner_output,
            fixer_output,
            request_id
        )
        
        # Call AI model
        logger.debug("Validator - Calling AI API")
        response = await self.ai_client.generate(prompt, temperature=0.3)
        
        # Parse JSON response
        validator_output = self.parse_json_response(response)
        
        # Validate and set defaults for required fields
        validator_output.setdefault("agent_name", "Validator")
        validator_output.setdefault("request_id", request_id)
        validator_output.setdefault("status", "completed")
        validator_output.setdefault("validation_status", "approved")
        validator_output.setdefault("confidence_score", 0.8)
        validator_output.setdefault("checks_performed", [])
        validator_output.setdefault("issues_found", [])
        validator_output.setdefault("warnings", [])
        validator_output.setdefault("recommendations", [])
        validator_output.setdefault("comparison", {
            "errors_fixed": 0,
            "warnings_addressed": 0,
            "new_issues": 0,
            "improvement_percentage": 100
        })
        validator_output.setdefault("final_verdict", validator_output.get("validation_status", "approved"))
        validator_output.setdefault("approval_reason", "Validation completed")
        validator_output.setdefault("requires_revision", False)
        validator_output.setdefault("revision_suggestions", [])
        validator_output.setdefault("validation_time", 0)
        
        logger.info(f"Validator - Status: {validator_output.get('validation_status')}")
        return validator_output
