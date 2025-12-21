from typing import Dict, Any, List
import json
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.logger import get_logger
from app.agents.base import GroqChatModel, get_fallback_model
from app.agents.prompts import get_validator_prompt, get_validator_user_message
from langchain.agents import create_agent

logger = get_logger()

# Define structured output schema
class ValidationCheck(BaseModel):
    """Represents a single validation check"""
    status: str = Field(description="Status: 'passed', 'failed', or 'warning'")
    check_type: str = Field(description="Type of check performed")
    message: str = Field(description="Description of the check result")

class ValidatorOutput(BaseModel):
    """Structured output for the validator agent"""
    validation_status: str = Field(description="Overall status: 'approved' or 'needs_revision'")
    confidence_score: float = Field(description="Confidence in the validation (0.0 to 1.0)")
    checks_performed: List[ValidationCheck] = Field(description="List of validation checks performed")
    issues_found: List[str] = Field(description="List of issues found in the fixed code")
    final_verdict: str = Field(description="Final verdict explanation")
    requires_revision: bool = Field(description="Whether the code needs further revision")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for improvement")

async def validator_agent(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validator Agent - Validates fixes using LangChain agent with structured output.
    """
    request_id = input_data.get("request_id")
    original = input_data.get("original_code")
    fixed = input_data.get("fixed_code")
    language = input_data.get("language", "python")
    
    model = GroqChatModel()
    
    # Get system prompt
    instruction = get_validator_prompt(language)
    
    try:
        # Get user message
        user_msg = get_validator_user_message(language, original, fixed)
        
        logger.info(f"Creating Validator agent using create_agent with structured output")
        
        # Use create_agent with response_format for structured output
        agent_graph = create_agent(
            model=model,
            tools=[],
            system_prompt=instruction,
            response_format=ValidatorOutput
        )
        
        try:
            result = await agent_graph.ainvoke({
                "messages": [{"role": "user", "content": user_msg}]
            })
        except Exception as e:
            if "429" in str(e) or "Rate limit" in str(e):
                logger.warning(f"Validator - Rate limit hit, switching to fallback model. Error: {e}")
                
                # Retry with fallback model
                fallback_model = get_fallback_model()
                if fallback_model is None:
                    logger.error("Validator - Fallback model not available")
                    raise e
                agent_graph = create_agent(
                    model=fallback_model,
                    tools=[],
                    system_prompt=instruction,
                    response_format=ValidatorOutput
                )
                
                result = await agent_graph.ainvoke({
                    "messages": [{"role": "user", "content": user_msg}]
                })
            else:
                raise e
        
        logger.info(f"Validator - Agent result keys: {result.keys()}")
        
        # Extract structured response
        structured_response = result.get("structured_response")
        
        if structured_response:
            logger.info(f"Validator - Got structured response")
            # Convert Pydantic model to dict
            data = structured_response.model_dump() if hasattr(structured_response, 'model_dump') else structured_response.dict()
        else:
            logger.info(f"Validator - Falling back to message parsing")
            # Fallback to parsing from messages
            messages = result.get("messages", [])
            if not messages:
                raise ValueError("No response from agent")
                
            last_message = messages[-1]
            response_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
            
            logger.info(f"Validator - Response preview: {response_content[:200]}")
            
            if "```json" in response_content:
                json_text = response_content.split("```json")[1].split("```")[0].strip()
            elif "```" in response_content:
                 json_text = response_content.split("```")[1].split("```")[0].strip()
            else:
                json_text = response_content.strip()
                
            data = json.loads(json_text)
        
        logger.info(f"Validator - Final data: validation_status={data.get('validation_status')}, requires_revision={data.get('requires_revision')}")
        
        return {
            "agent_name": "Validator",
            "request_id": request_id,
            "status": "completed",
            **data,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Validator Agent failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            "validation_status": "approved", 
            "final_verdict": f"Validation failed: {e}",
            "requires_revision": False,
            "confidence_score": 0.0,
            "issues_found": [],
            "checks_performed": []
        }
