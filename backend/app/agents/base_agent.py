from abc import ABC, abstractmethod
from typing import Dict, Any
import json
import time
from app.utils.logger import get_logger

logger = get_logger()

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        logger.info(f"Initialized {self.name} agent")
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic"""
        pass
    
    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate JSON response from AI model"""
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
            logger.debug(f"{self.name} - Successfully parsed JSON response")
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"{self.name} - JSON parse error: {str(e)}")
            logger.error(f"Response was: {response[:500]}")
            raise ValueError(f"Invalid JSON response from {self.name}: {str(e)}")
    
    async def execute_with_timing(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent with timing"""
        start_time = time.time()
        logger.info(f"{self.name} - Starting execution")
        
        try:
            result = await self.execute(input_data)
            execution_time = time.time() - start_time
            
            # Add timing info
            if isinstance(result, dict):
                result['execution_time'] = round(execution_time, 2)
            
            logger.info(f"{self.name} - Completed in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{self.name} - Failed after {execution_time:.2f}s: {str(e)}")
            raise
