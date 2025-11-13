# from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import Response

# REQ_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
# REQ_LAT = Histogram("http_request_latency_seconds", "Latency", ["method", "path"])


# class MetricsMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         path = request.url.path
#         method = request.method
#         with REQ_LAT.labels(method, path).time():
#             resp: Response = await call_next(request)
#         REQ_COUNT.labels(method, path, str(resp.status_code)).inc()
#         return resp


# async def metrics_endpoint():
#     data = generate_latest()
#     return Response(content=data, media_type=CONTENT_TYPE_LATEST)

# server/src/app/metrics.py
import time

from fastapi import APIRouter, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

router = APIRouter()


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware thu thập metrics cho mọi request (trừ /metrics)."""

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/metrics":
            return await call_next(request)

        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start

        REQUEST_COUNT.labels(
            method=request.method,
            path=request.url.path,
            status_code=str(response.status_code),
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            path=request.url.path,
        ).observe(elapsed)

        return response


@router.get("/metrics")
def metrics() -> Response:
    """Endpoint Prometheus scrape."""
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
