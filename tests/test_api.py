# /tests/test_api.py
from fastapi.testclient import TestClient
import pytest

from recruitair.api.dependencies import get_model
from recruitair.api.main import app
from recruitair.api.model import BaseEvaluatorModel
from recruitair.job_offers.models import KeyCriteriaResponse, KeyCriterion


class MockModel(BaseEvaluatorModel):
    def __init__(self):
        self._version = "mock-1"

    @property
    def version(self):
        return self._version

    def evaluate(self, job_offer: str) -> KeyCriteriaResponse:
        return KeyCriteriaResponse(key_criteria=[KeyCriterion(description="Python programming", importance=80)])


app.dependency_overrides[get_model] = lambda: MockModel()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_eval_python_match(client: TestClient):
    req = {
        "offer_text": "Looking for a developer with experience with Python and ML",
    }
    r = client.post("/eval", json=req)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["criteria"][0]["importance"] == 0.8
    assert data["criteria"][0]["description"] == "Python programming"


def test_eval_empty_job_offer(client: TestClient):
    req1 = {"offer_text": ""}
    r1 = client.post("/eval", json=req1)
    assert r1.status_code == 422


def test_health(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
