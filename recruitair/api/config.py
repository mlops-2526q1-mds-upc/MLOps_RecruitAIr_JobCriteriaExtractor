from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RECRUITAIR_")
    # Don't forget to set MLFLOW_TRACKING_URI in your environment variables
    prompt: str = Field("criteria-extraction", description="MLflow prompt URI; override via env")
    prompt_version: str = Field("1", description="Prompt version to load")

    model: str = Field("dolphin3", description="OLlama model name")
    model_version: str = Field("8b", description="OLlama model version")
    ollama_base_url: str | None = Field(None, description="Base URL for OLlama API; override via env")
    api_root_path: str = Field("", description="API root path; override via env")


settings = Settings()
