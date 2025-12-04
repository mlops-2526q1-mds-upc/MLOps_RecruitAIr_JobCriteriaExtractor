from contextlib import asynccontextmanager
import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_model
from .model import BaseEvaluatorModel
from .schemas import EvalRequest, EvalResponse

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Preloading prompt at startup...")
    _get_model = app.dependency_overrides.get(get_model, get_model)
    model: BaseEvaluatorModel = _get_model()
    logger.info("Loaded prompt version: %s", getattr(model, "version", "unknown"))
    yield


app = FastAPI(title="Job Criteria Extractor API", version="v1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.post("/eval", response_model=EvalResponse)
def evaluate(request: EvalRequest, model: BaseEvaluatorModel = Depends(get_model)):
    """Evaluate a job offer to extract the key criteria."""
    try:
        response = model.evaluate(request.offer_text)
    except Exception as exc:
        logger.exception("Model evaluation failed: %s", exc)
        raise HTTPException(status_code=500, detail="Model prediction failed")

    output_criteria = []
    for criteria in response.key_criteria:
        item = EvalResponse.CriteriaItem(
            description=criteria.description,
            importance=criteria.importance / 100,
        )
        output_criteria.append(item)
    return EvalResponse(
        criteria=output_criteria
    )


@app.get("/health")
def health():
    return {"status": "ok"}
