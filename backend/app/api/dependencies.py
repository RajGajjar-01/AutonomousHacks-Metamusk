"""API dependencies and dependency injection"""
from functools import lru_cache
from app.config import get_settings
from app.core.logger import get_logger

logger = get_logger()

@lru_cache()
def get_app_settings():
    """Get application settings"""
    return get_settings()

def get_logger_instance():
    """Get logger instance"""
    return get_logger()
