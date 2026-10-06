from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application runtime configuration and environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_ENV: str = Field(default="development", description="development | test | production")
    LOG_LEVEL: str = Field(default="INFO", description="Standard logging level")

    # API
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    FRONTEND_URL: str = Field(default="http://localhost:5173")

    # LLM Configuration
    LLM_PROVIDER: str = Field(default="openai", description="openai | mock")
    LLM_MODEL: str = Field(default="gpt-4o-mini")
    LLM_BASE_URL: Optional[str] = Field(default=None)
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    LLM_TEMPERATURE: float = Field(default=0.2)

    # Search Configuration
    SEARCH_PROVIDER: str = Field(default="mock", description="mock | tavily")
    TAVILY_API_KEY: Optional[str] = Field(default=None)
    SEARCH_MAX_RESULTS: int = Field(default=5)

    # Workflow Safeguards
    MAX_RESEARCH_RETRIES: int = Field(default=2)
    MAX_SUBTASKS: int = Field(default=5)
    DEFAULT_RESEARCH_DEPTH: str = Field(default="standard")


settings = Settings()
