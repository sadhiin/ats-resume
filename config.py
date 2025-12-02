from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Backend environment settings for cRag application."""

    model_config = SettingsConfigDict(env_file=".env", extra="forbid")
    OPENAI_API_KEY: SecretStr


settings = Settings()
