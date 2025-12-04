from functools import lru_cache

from .config import settings
from .model import BaseEvaluatorModel, OLlamaEvaluator


@lru_cache()
def get_model() -> BaseEvaluatorModel:
    """Get the evaluator model and prompt, loading it if necessary."""

    return OLlamaEvaluator(
        model=settings.model,
        version=settings.model_version,
        prompt_uri=f"models:/{settings.prompt}/{settings.prompt_version}"
    )
