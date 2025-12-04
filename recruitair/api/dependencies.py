import os
from functools import lru_cache

import mlflow

from .config import settings
from .model import BaseEvaluatorModel, OLlamaEvaluator


@lru_cache()
def get_model() -> BaseEvaluatorModel:
    """Get the evaluator model and prompt, loading it if necessary."""
    if os.getenv("MLFLOW_TRACKING_URI") is None:
        raise EnvironmentError("Please set the MLFLOW_TRACKING_URI environment variable.")
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

    return OLlamaEvaluator(
        model=settings.model,
        version=settings.model_version,
        prompt_uri=f"prompts:/{settings.prompt}/{settings.prompt_version}"
    )
