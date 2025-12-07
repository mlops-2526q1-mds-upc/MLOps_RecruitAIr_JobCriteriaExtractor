from contextlib import asynccontextmanager
import logging
import time

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest

from .config import settings
from .dependencies import get_model
from .model import BaseEvaluatorModel
from .monitoring import (
    EVAL_REQUEST_LATENCY_SECONDS,
    EVAL_REQUESTS_FAILED_TOTAL,
    EVAL_REQUESTS_TOTAL,
    MODEL_EVALUATION_ERRORS_TOTAL,
    MODEL_EVALUATION_LATENCY_SECONDS,
    OFFER_TEXT_LENGTH,
)
from .schemas import EvalRequest, EvalResponse

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan hook used to warm up the model once at startup
    and log the loaded prompt/version.
    """
    logger.info("Preloading prompt at startup...")
    _get_model = app.dependency_overrides.get(get_model, get_model)
    model: BaseEvaluatorModel = _get_model()
    logger.info("Loaded prompt version: %s", getattr(model, "version", "unknown"))
    yield


app = FastAPI(
    title="Job Criteria Extractor API",
    version="v1",
    lifespan=lifespan,
    root_path=settings.api_root_path,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.post("/eval", response_model=EvalResponse)
def evaluate(
    request: EvalRequest,
    model: BaseEvaluatorModel = Depends(get_model),
) -> EvalResponse:
    """
    Evaluate a job offer to extract the key criteria.

    This endpoint is instrumented with Prometheus metrics:
    - request count
    - request latency
    - model evaluation latency
    - failures
    - input length distribution
    """
    EVAL_REQUESTS_TOTAL.inc()
    OFFER_TEXT_LENGTH.observe(len(request.offer_text or ""))

    start_request = time.perf_counter()

    try:
        # Measure only the model evaluation part separately
        start_model = time.perf_counter()
        try:
            response = model.evaluate(request.offer_text)
        except Exception as exc:  # noqa: BLE001
            MODEL_EVALUATION_ERRORS_TOTAL.inc()
            logger.exception("Model evaluation failed: %s", exc)
            raise
        finally:
            MODEL_EVALUATION_LATENCY_SECONDS.observe(time.perf_counter() - start_model)

    except Exception:
        # Any error that bubbles up to here is an inference failure
        EVAL_REQUESTS_FAILED_TOTAL.inc()
        # Still let FastAPI handle it as 500
        raise HTTPException(status_code=500, detail="Model prediction failed")

    finally:
        EVAL_REQUEST_LATENCY_SECONDS.observe(time.perf_counter() - start_request)

    # Normal successful path
    output_criteria: list[EvalResponse.CriteriaItem] = []
    for criteria in response.key_criteria:
        item = EvalResponse.CriteriaItem(
            description=criteria.description,
            # model returns importance in 0–100; API exposes 0–1
            importance=criteria.importance / 100,
        )
        output_criteria.append(item)

    return EvalResponse(criteria=output_criteria)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> Response:
    """
    Expose Prometheus metrics in the OpenMetrics / Prometheus text format.

    Prometheus will scrape this endpoint at /metrics.
    """
    # Using default global registry here; if you ever need a custom registry
    # you can wire it up via CollectorRegistry().
    registry = CollectorRegistry()
    # In simple setups generate_latest() uses the default REGISTRY implicitly,
    # so we can just call it without passing registry.
    data = generate_latest()  # type: ignore[arg-type]
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
