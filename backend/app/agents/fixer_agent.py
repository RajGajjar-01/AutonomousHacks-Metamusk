from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from app.utils.ai_clients import groq_client
from app.utils.prompts import AgentPrompts
import time
from app.utils.logger import get_logger

logger = get_logger()

class FixerAgent(BaseAgent):
    """Agent for fixing code errors"""
    
    def __init__(self):
        super().__init__("Fixer")
        self.ai_client = groq_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute fixer agent
        
        Input JSON:
        {
            "request_id": "uuid",
            "original_code": "buggy code",
            "language": "python",
            "scanner_output": { ... complete scanner JSON ... }
        }
        
        Output JSON: Complete fixer output as per schema
        """
        logger.info(f"Fixer - Processing request {input_data.get('request_id')}")
        
        # Extract input
        request_id = input_data.get("request_id")
        original_code = input_data.get("original_code")
        language = input_data.get("language", "python")
        scanner_output = input_data.get("scanner_output", {})
        
        # Generate prompt with scanner output
        prompt = AgentPrompts.fixer_prompt(
            original_code, 
            language, 
            scanner_output,
            request_id
        )
        
        # Call AI model
        logger.debug("Fixer - Calling AI API")
        response = await self.ai_client.generate(prompt, temperature=0.5)
        
        # Parse JSON response
        fixer_output = self.parse_json_response(response)
        
        # Validate and set defaults for required fields
        fixer_output.setdefault("agent_name", "Fixer")
        fixer_output.setdefault("request_id", request_id)
        fixer_output.setdefault("status", "completed")
        fixer_output.setdefault("fixed_code", original_code)
        fixer_output.setdefault("changes", [])
        fixer_output.setdefault("diff", {"additions": [], "deletions": [], "modifications": []})
        fixer_output.setdefault("alternative_fixes", [])
        fixer_output.setdefault("explanation", "No changes needed")
        fixer_output.setdefault("total_changes", len(fixer_output.get("changes", [])))
        fixer_output.setdefault("fix_time", 0)
        
        logger.info(f"Fixer - Made {fixer_output.get('total_changes', 0)} changes")
        return fixer_output
