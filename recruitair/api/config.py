from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RECRUITAIR_")
    # Don't forget to set MLFLOW_TRACKING_URI in your environment variables
    prompt: str = Field(
        "one-shot-long-descriptions", description="default MLflow prompt URI; override via env"
    )
    prompt_version: str = Field("2", description="Prompt version to load")

    model: str = Field("dolphin3", description="OLlama model name")
    model_version: str = Field("8b", description="OLlama model version")


settings = Settings()
