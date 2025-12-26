from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Load .env file

class Settings(BaseSettings):
    hf_token: str = ""
    tavily_api_key: str
    github_token: str
    groq_api_key: str = ""
    gemini_api_key: str = ""  # Optional for future use
    database_url: str = "sqlite:///./goabroadai.db"  # For future use

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra vars in .env

# Singleton instance
settings = Settings()

# Test (remove in production)
if __name__ == "__main__":
    print("Config loaded successfully!")
    print(f"HF token: {'Yes' if settings.hf_token else 'No'}")
    print(f"Tavily key: {'Yes' if settings.tavily_api_key else 'No'}")
    print(f"Gemini key: {'Yes' if settings.gemini_api_key else 'No'}")
    print(f"DB URL: {settings.database_url}")