from typing import Dict, Any, List
import json
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.logger import get_logger
from app.agents.base import GroqChatModel, get_fallback_model
from app.agents.prompts import get_fixer_prompt, get_fixer_user_message
from langchain.agents import create_agent

logger = get_logger()

# Define structured output schema
class CodeChange(BaseModel):
    """Represents a single code change"""
    line_number: int = Field(description="Line number where the change was made")
    original: str = Field(description="Original line content")
    fixed: str = Field(description="Fixed line content")
    reason: str = Field(description="Reason for the fix")

class FixerOutput(BaseModel):
    """Structured output for the fixer agent"""
    fixed_code: str = Field(description="The complete fixed code")
    changes: List[CodeChange] = Field(description="List of changes made")
    explanation: str = Field(description="Summary of all fixes applied")
    confidence_score: float = Field(description="Confidence in the fixes (0.0 to 1.0)")

async def fixer_agent(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fixer Agent - Fixes code errors using LangChain agent with structured output.
    """
    request_id = input_data.get("request_id")
    code = input_data.get("original_code")
    scanner_output = input_data.get("scanner_output", {})
    language = input_data.get("language", "python")

    errors = scanner_output.get("errors", [])
    if not errors:
        return {
            "fixed_code": code, 
            "changes": [], 
            "explanation": "No errors found to fix.", 
            "total_changes": 0,
            "confidence_score": 1.0
        }

    model = GroqChatModel()
    
    # Get system prompt
    instruction = get_fixer_prompt(language)
    
    try:
        error_context = json.dumps(errors, indent=2)
        
        # Get user message
        user_msg = get_fixer_user_message(language, code, error_context)
        
        logger.info(f"Creating Fixer agent using create_agent with structured output")
        
        # Use create_agent with response_format for structured output
        agent_graph = create_agent(
            model=model,
            tools=[],
            system_prompt=instruction,
            response_format=FixerOutput
        )
        
        try:
            result = await agent_graph.ainvoke({
                "messages": [{"role": "user", "content": user_msg}]
            })
        except Exception as e:
            if "429" in str(e) or "Rate limit" in str(e):
                logger.warning(f"Fixer - Rate limit hit, switching to fallback model. Error: {e}")
                
                # Retry with fallback model
                fallback_model = get_fallback_model()
                agent_graph = create_agent(
                    model=fallback_model,
                    tools=[],
                    system_prompt=instruction,
                    response_format=FixerOutput
                )
                
                result = await agent_graph.ainvoke({
                    "messages": [{"role": "user", "content": user_msg}]
                })
            else:
                raise e
        
        # Extract structured response
        structured_response = result.get("structured_response")
        
        if structured_response:
            # Convert Pydantic model to dict
            data = structured_response.model_dump() if hasattr(structured_response, 'model_dump') else structured_response.dict()
        else:
            # Fallback to parsing from messages
            messages = result.get("messages", [])
            if not messages:
                raise ValueError("No response from agent")
                
            last_message = messages[-1]
            response_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
            
            if "```json" in response_content:
                json_text = response_content.split("```json")[1].split("```")[0].strip()
            elif "```" in response_content:
                 json_text = response_content.split("```")[1].split("```")[0].strip()
            else:
                json_text = response_content.strip()
                
            data = json.loads(json_text)
        
        return {
            "agent_name": "Fixer",
            "request_id": request_id,
            "status": "completed",
            **data,
            "total_changes": len(data.get("changes", [])),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Fixer Agent failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            "fixed_code": code, 
            "changes": [], 
            "explanation": f"Failed: {e}",
            "total_changes": 0,
            "confidence_score": 0.0
        }
