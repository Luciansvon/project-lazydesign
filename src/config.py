"""
Konfigurasi aplikasi
"""
import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Bot Configuration
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    discord_bot_token: str = os.getenv("DISCORD_BOT_TOKEN", "")
    
    # AI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///finance_assistant.db")
    
    # Admin
    admin_user_id: str = os.getenv("ADMIN_USER_ID", "")
    
    # General
    default_currency: str = os.getenv("DEFAULT_CURRENCY", "IDR")
    
    class Config:
        env_file = ".env"

settings = Settings()
