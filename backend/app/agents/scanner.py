from typing import Dict, Any
import json
from datetime import datetime

from app.core.logger import get_logger
from app.agents.base import create_base_agent, GroqChatModel, get_fallback_model
from app.agents.prompts import get_scanner_prompt, get_scanner_user_message
from app.agents.tools.scanner_tools import (
    analyze_python_syntax, 
    find_undefined_variables, 
    check_code_quality_issues
)

logger = get_logger()

async def scanner_agent(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scanner Agent - Analyzes code for errors using LangChain agent.
    """
    request_id = input_data.get("request_id")
    code = input_data.get("code")
    language = input_data.get("language", "python")
    context = input_data.get("context")
    
    logger.info(f"Scanner Agent - Processing request {request_id}")
    
    # 1. Setup Tools and Model
    tools = [
        analyze_python_syntax,
        find_undefined_variables,
        check_code_quality_issues
    ]
    
    # 2. Get System Prompt
    instruction = get_scanner_prompt(language)

    # 3. Create Agent (initial attempt with primary model)
    model = GroqChatModel()
    agent_graph = create_base_agent("Scanner", instruction, tools, model)
    
    # 4. Invoke Agent
    try:
        # Get user message
        user_msg = get_scanner_user_message(language, code, context)
        
        try:
            # Invoke the graph with messages
            result = await agent_graph.ainvoke({
                "messages": [{"role": "user", "content": user_msg}]
            })
        except Exception as e:
            if "429" in str(e) or "Rate limit" in str(e):
                logger.warning(f"Scanner - Rate limit hit, switching to fallback model. Error: {e}")
                
                # Retry with fallback model
                fallback_model = get_fallback_model()
                agent_graph = create_base_agent("Scanner (Fallback)", instruction, tools, fallback_model)
                
                result = await agent_graph.ainvoke({
                    "messages": [{"role": "user", "content": user_msg}]
                })
            else:
                raise e
        
        logger.info(f"Scanner - Agent result keys: {result.keys()}")
        
        # Extract the last message from the result
        messages = result.get("messages", [])
        if not messages:
            raise ValueError("No messages in agent response")
            
        last_message = messages[-1]
        response_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        logger.info(f"Scanner - Response content preview: {response_content[:200]}")
        
        # Parse JSON
        if "```json" in response_content:
            json_text = response_content.split("```json")[1].split("```")[0].strip()
        elif "```" in response_content:
             json_text = response_content.split("```")[1].split("```")[0].strip()
        else:
            json_text = response_content.strip()
            
        data = json.loads(json_text)
        
        return {
            "agent_name": "Scanner",
            "request_id": request_id,
            "status": "completed",
            **data,
            "total_errors": len(data.get("errors", [])),
            "total_warnings": len(data.get("warnings", [])),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(f"Scanner Agent failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            "agent_name": "Scanner", 
            "errors": [], 
            "warnings": [], 
            "total_errors": 0,
            "total_warnings": 0,
            "code_quality_score": 0,
            "analysis_summary": f"Failed: {str(e)}",
            "is_runnable": False
        }
