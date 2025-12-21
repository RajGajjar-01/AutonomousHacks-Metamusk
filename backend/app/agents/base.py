from typing import Any, List
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

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

def get_huggingface_model():
    """
    Returns a configured ChatHuggingFace instance using Qwen2.5-Coder.
    """
    if not settings.huggingfacehub_api_token:
        logger.warning("HuggingFace API token missing!")
        return None
    
    try:
        llm = HuggingFaceEndpoint(
            repo_id="Qwen/Qwen2.5-Coder-32B-Instruct",
            huggingfacehub_api_token=settings.huggingfacehub_api_token,
            task="text-generation",
            temperature=0.1,
            max_new_tokens=2048
        )
        return ChatHuggingFace(llm=llm)
    except Exception as e:
        logger.error(f"Failed to create HuggingFace model: {e}")
        return None

def get_fallback_model():
    """
    Returns a fallback model (Hugging Face or smaller Groq model)
    to use when the primary model hits rate limits.
    """
    # 1. Try Hugging Face first (True fallback provider)
    if settings.huggingfacehub_api_token:
        hf_model = get_huggingface_model()
        if hf_model:
            logger.info("Using HuggingFace Qwen2.5-Coder as fallback model")
            return hf_model

    # 2. Fallback to smaller Groq model if HF not available
    if not settings.groq_api_key:
        logger.warning("Groq API key missing!")
        return None
        
    try:
        logger.info("Using Groq Llama-3.1-8b as fallback model")
        return ChatGroq(
            api_key=settings.groq_api_key,
            model="llama-3.1-8b-instant",
            temperature=0.2
        )
    except Exception as e:
        logger.error(f"Failed to create Groq fallback model: {e}")
        return None

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
