from functools import lru_cache
import logging
import os

import mlflow

from .config import settings
from .model import BaseEvaluatorModel, OLlamaEvaluator

logger = logging.getLogger("uvicorn.error")


@lru_cache()
def get_model() -> BaseEvaluatorModel:
    """Get the evaluator model and prompt, loading it if necessary."""
    if os.getenv("MLFLOW_TRACKING_URI") is None:
        raise EnvironmentError("Please set the MLFLOW_TRACKING_URI environment variable.")
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

    logger.info(
        "Loading OLlamaEvaluator model for model=%s, version=%s base_uri=%s, for prompt=%s/%s"
        % (settings.model, settings.model_version, settings.ollama_base_url, settings.prompt, settings.prompt_version)
    )

    return OLlamaEvaluator(
        model=settings.model,
        version=settings.model_version,
        prompt_uri=f"prompts:/{settings.prompt}/{settings.prompt_version}",
        ollama_base_url=settings.ollama_base_url,
    )
