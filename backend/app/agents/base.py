from typing import Any, List
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from app.config import get_settings
from app.core.logger import get_logger

logger = get_logger()
settings = get_settings()

# ============================================================================
# LLM WRAPPER
# ============================================================================

def GroqChatModel():
    """
    Returns a configured ChatGroq instance.
    Compatible with LangChain tool binding.
    """
    if not settings.groq_api_key:
        logger.warning("Groq API key missing!")
        
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0.2
    )

# ============================================================================
# BASE AGENT FACTORY
# ============================================================================

def create_base_agent(name: str, instruction: str, tools: List[Any], model):
    """
    Base function to create any agent using langchain.agents.create_agent
    
    Args:
        name: Name of the agent for logging
        instruction: System prompt for the agent
        tools: List of tools the agent can use
        model: LangChain chat model instance
        
    Returns:
        CompiledStateGraph: The compiled agent graph
    """
    logger.info(f"Creating {name} agent using create_agent")
    
    # create_agent returns a CompiledStateGraph
    # It expects: model, tools, system_prompt
    agent_graph = create_agent(
        model=model,
        tools=tools,
        system_prompt=instruction
    )
    
    return agent_graph
