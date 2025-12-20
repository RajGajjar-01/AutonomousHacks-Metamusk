from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # AI Model Configuration
    gemini_model: str = "models/gemini-2.5-pro"
    groq_model: str = "llama-3.3-70b-versatile"
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    
    # Workflow Configuration
    max_iterations: int = 3
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra fields like old GROQ_API_KEY

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
