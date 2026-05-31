from fastapi import Depends, FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from app.auth import require_api_key
from app.backend import vllm_backend
from slowapi.errors import RateLimitExceeded

app = FastAPI(title = "OpenServe Gateway")

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

limiter = Limiter(key_func = get_remote_address)
app.state.limiter = limiter

REQUESTS = Counter(
    "openserve_requests_total",
    "Total gateway requests",
    ["endpoint"]
)

LATENCY = Histogram(
    "openserve_request_latency_seconds",
    "Gateway request latency",
    ["endpoint"]
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type = "text/plain")


@app.post("/v1/chat/completions", dependencies = [Depends(require_api_key)])
@limiter.limit("60/minute")
async def chat_completions(request: Request):
    REQUESTS.labels(endpoint = "/v1/chat/completions").inc()

    with LATENCY.labels(endpoint = "/v1/chat/completions").time():
        payload = await request.json()
        return await vllm_backend.chat_completions(payload)