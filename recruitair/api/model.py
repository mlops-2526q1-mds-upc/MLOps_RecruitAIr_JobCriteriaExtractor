import logging
from typing import Optional

import mlflow
from langchain_ollama import ChatOllama

from recruitair.job_offers.models import KeyCriteriaResponse

logger = logging.getLogger(__name__)


class BaseEvaluatorModel:
    """Interface for evaluator models"""

    def evaluate(self, job_offer: str) -> KeyCriteriaResponse:
        raise NotImplementedError()

    @property
    def version(self) -> Optional[str]:
        return None


class DummyEvaluator(BaseEvaluatorModel):
    """Deterministic lightweight scorer for local dev & tests."""

    def __init__(self):
        self._version = "dummy-v1"

    @property
    def version(self) -> str:
        return self._version

    def evaluate(self, job_offer: str) -> KeyCriteriaResponse:
        return KeyCriteriaResponse(key_criteria=[])


class OLlamaEvaluator(BaseEvaluatorModel):

    def __init__(self, model: str, version: str, prompt_uri: str):
        self._model = model
        self._version = version
        self._prompt_uri = prompt_uri
        self._prompt = None
        self._llm = None
        self._load()

    def _load(self):
        self._llm = ChatOllama(model=f"{self._model}:{self._version}", temperature=0)
        self._prompt = mlflow.genai.load_prompt(self._prompt_uri)

    def evaluate(self, job_offer: str) -> KeyCriteriaResponse:
        response = self._llm.with_structured_output(
            self._prompt.response_format,
            method="json_schema",
        ).invoke(
            self._prompt.format(job_offer_text=job_offer)
        )
        return KeyCriteriaResponse.model_validate(response)
