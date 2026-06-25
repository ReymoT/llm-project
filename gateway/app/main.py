from fastapi import Depends, FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest, Gauge
from fastapi.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.auth import require_api_key
from app.router import backend_router
from app.schemas import ChatCompletionRequest

app = FastAPI(title="OpenServe Gateway")

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

REQUESTS = Counter(
    "openserve_requests_total", "Total gateway requests", ["endpoint", "backend"]
)

LATENCY = Histogram(
    "openserve_request_latency_seconds",
    "Gateway request latency",
    ["endpoint", "backend"],
)

BACKEND_HEALTH = Gauge(
    "openserve_backend_health",
    "Backend health status, 1 means healthy and 0 means unhealthy",
    ["backend"],
)

BACKEND_ERRORS = Counter(
    "openserve_backend_errors_total", "Total backend errors", ["backend"]
)

BACKEND_SELECTIONS = Counter(
    "openserve_backend_selections_total",
    "Total times a backend was selected",
    ["backend"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/backend/status")
async def backend_status():
    status_map = await backend_router.backend_status()

    for backend, healthy in status_map.items():
        BACKEND_HEALTH.labels(backend=backend).set(1 if healthy else 0)

    return status_map


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")


@app.post("/v1/chat/completions", dependencies=[Depends(require_api_key)])
@limiter.limit("60/minute")
async def chat_completions(request: Request, body: ChatCompletionRequest):
    backend = await backend_router.select_backend()
    endpoint = "/v1/chat/completions"

    BACKEND_SELECTIONS.labels(backend=backend.name).inc()
    REQUESTS.labels(endpoint=endpoint, backend=backend.name).inc()

    try:
        with LATENCY.labels(endpoint=endpoint, backend=backend.name).time():
            payload = body.model_dump(exclude_none=True)
            return await backend.chat_completions(payload)

    except Exception:
        BACKEND_ERRORS.labels(backend=backend.name).inc()
        raise
