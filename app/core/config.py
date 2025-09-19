"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List, Union


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/ai_business_assistant"
    
    # TigerData (Time-series Analytics)
    TIGERDATA_SERVICE_URL: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # API Keys
    GLADIA_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    BRIGHT_DATA_API_KEY: str = ""
    
    # Application
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALLOWED_HOSTS: Union[str, List[str]] = "localhost,127.0.0.1"
    
    # Vector Search
    VECTOR_DIMENSION: int = 384
    SIMILARITY_THRESHOLD: float = 0.7
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Convert ALLOWED_HOSTS to list if it's a string
        if isinstance(self.ALLOWED_HOSTS, str):
            self.ALLOWED_HOSTS = [host.strip() for host in self.ALLOWED_HOSTS.split(',')]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
