from abc import ABC, abstractmethod
from typing import Optional
import httpx
from app.config import get_settings
from app.core.logger import get_logger

settings = get_settings()
logger = get_logger()

class BaseAIClient(ABC):
    """Abstract base class for AI clients"""
    
    @abstractmethod
    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate response from AI model"""
        pass

import groq
import google.generativeai as genai
from google.api_core import retry

class GroqClient(BaseAIClient):
    """Groq API client"""
    
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.model = settings.groq_model
        if self.api_key:
            self.client = groq.AsyncGroq(api_key=self.api_key)
            logger.info(f"GroqClient initialized with model: {self.model}")
        else:
            self.client = None
            logger.warning("GroqClient initialized without API key")
            
    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        if not self.client:
             raise ValueError("Groq API key not configured")
             
        try:
            logger.debug(f"Groq - Sending request (temp={temperature})")
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=temperature,
                response_format={"type": "json_object"},
            )
            text = chat_completion.choices[0].message.content
            logger.debug(f"Groq - Received response ({len(text)} chars)")
            return text
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise

class GeminiClient(BaseAIClient):
    """Google Gemini API client using official SDK"""
    
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model_name = settings.gemini_model
        
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"GeminiClient initialized with model: {self.model_name}")
        else:
            self.model = None
            logger.warning("GeminiClient initialized without valid API key")
    
    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate response using Gemini SDK"""
        if not self.model:
            raise ValueError("Gemini API key not configured. Please add GEMINI_API_KEY to .env")
        
        try:
            logger.debug(f"Gemini - Sending request (temp={temperature})")
            
            # Use async generation
            response = await self.model.generate_content_async(
                contents=prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=8192,
                    response_mime_type="application/json"
                )
            )
            
            text = response.text
            logger.debug(f"Gemini - Received response ({len(text)} chars)")
            return text
                
        except Exception as e:
            logger.error(f"Gemini SDK error: {str(e)}")
            raise

# Singleton instances
gemini_client = GeminiClient()
groq_client = GroqClient()
