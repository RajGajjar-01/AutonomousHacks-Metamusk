from typing import Dict, Any
import json
from app.agents.base_agent import BaseAgent
from app.utils.ai_clients import groq_client
from app.utils.prompts import AgentPrompts
from app.utils.logger import get_logger

logger = get_logger()

class ScannerAgent(BaseAgent):
    """Scanner Agent - Identifies syntax and runtime errors"""
    
    def __init__(self):
        super().__init__("Scanner")
        self.ai_client = groq_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute scanner agent
        
        Input JSON:
        {
            "request_id": "uuid",
            "code": "code string",
            "language": "python",
            "context": "optional context"
        }
        
        Output JSON: Complete scanner output as per schema
        """
        logger.info(f"Scanner - Processing request {input_data.get('request_id')}")
        
        # Extract input
        request_id = input_data.get("request_id")
        code = input_data.get("code")
        language = input_data.get("language", "python")
        
        # Generate prompt
        prompt = AgentPrompts.scanner_prompt(code, language, request_id)
        
        # Call AI model
        logger.debug("Scanner - Calling AI API")
        response = await self.ai_client.generate(prompt, temperature=0.3)
        
        # Parse JSON response
        scanner_output = self.parse_json_response(response)
        
        # Validate and set defaults for required fields
        scanner_output.setdefault("agent_name", "Scanner")
        scanner_output.setdefault("request_id", request_id)
        scanner_output.setdefault("status", "completed")
        scanner_output.setdefault("errors", [])
        scanner_output.setdefault("warnings", [])
        scanner_output.setdefault("total_errors", len(scanner_output.get("errors", [])))
        scanner_output.setdefault("total_warnings", len(scanner_output.get("warnings", [])))
        scanner_output.setdefault("code_quality_score", 5.0)
        scanner_output.setdefault("scan_time", 0)
        
        logger.info(f"Scanner - Found {scanner_output.get('total_errors', 0)} errors, {scanner_output.get('total_warnings', 0)} warnings")
        return scanner_output
