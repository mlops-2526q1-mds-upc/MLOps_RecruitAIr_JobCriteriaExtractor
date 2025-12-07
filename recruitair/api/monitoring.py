"""
Shared Prometheus metrics for the RecruitAIr Job Criteria Extractor.

Import these metrics from API / training code and update them there.
"""

from prometheus_client import Counter, Histogram

# --- API-level metrics ---

EVAL_REQUESTS_TOTAL = Counter(
    "recruitair_eval_requests_total",
    "Total number of /eval requests received",
)

EVAL_REQUESTS_FAILED_TOTAL = Counter(
    "recruitair_eval_requests_failed_total",
    "Total number of /eval requests that resulted in an error",
)

EVAL_REQUEST_LATENCY_SECONDS = Histogram(
    "recruitair_eval_request_latency_seconds",
    "Latency of /eval endpoint, in seconds",
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10),
)

# --- Model-level metrics ---

MODEL_EVALUATION_LATENCY_SECONDS = Histogram(
    "recruitair_model_evaluation_latency_seconds",
    "Time spent calling model.evaluate(), in seconds",
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10),
)

MODEL_EVALUATION_ERRORS_TOTAL = Counter(
    "recruitair_model_evaluation_errors_total",
    "Total number of exceptions raised by model.evaluate()",
)

# --- Payload / business metrics (optional but useful) ---

OFFER_TEXT_LENGTH = Histogram(
    "recruitair_offer_text_length_chars",
    "Length of offer_text passed to /eval (in characters)",
    buckets=(128, 256, 512, 1024, 2048, 4096, 8192),
)
