"""FastAPI middleware for collecting and exposing Prometheus metrics."""
import functools
import os
import time
import typing as t

import prometheus_client as prom
from fastapi import FastAPI, Request
from prometheus_client.multiprocess import MultiProcessCollector
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class MetricsMiddleware(BaseHTTPMiddleware):
    """Metrics middleware collecting prometheus metrics for each request."""

    def __init__(
        self,
        app: FastAPI,
        prefix: str = "fw_",
        buckets: t.Tuple[float, ...] = (0.002, 0.05, 0.1, prom.utils.INF),
    ) -> None:
        """Initialize a new MetricsMiddleware instance.

        Args:
            app (FastAPI): The FastAPI app instance to add metrics to.
            prefix (str, optional): String to prefix metrics with. Default: "fw_"
            buckets (tuple[int...], optional): Request duration buckets.
        """
        super().__init__(app)
        self.request_count = request_count(prefix)
        self.request_time = request_time(prefix, buckets)

    async def dispatch(self, request: Request, call_next: t.Callable):
        """Record request method, path and status when dispatching."""
        method = request.method
        path = request.url.path
        status = 500
        begin = time.time()
        try:
            response = await call_next(request)
            status = response.status_code
        finally:
            # track urls w/ params grouped, eg. /items/123 -> /items/{id}
            router = request.scope.get("router")
            endpoint = request.scope.get("endpoint")
            if router and endpoint:
                for route in router.routes:
                    route_app = getattr(route, "app", None)
                    route_endpoint = getattr(route, "endpoint", None)
                    if endpoint in (route_app, route_endpoint):
                        path = route.path
                        break
            end = time.time()
            labels = [method, path, status]
            self.request_count.labels(*labels).inc()
            self.request_time.labels(*labels).observe(end - begin)
        return response


@functools.lru_cache()
def request_count(prefix: str) -> prom.Counter:
    """Return request count metric for the app prefix (cached/singleton)."""
    return prom.Counter(
        f"{prefix}requests_total",
        "Total HTTP requests",
        ("method", "path", "status"),
        registry=get_registry(),
    )


@functools.lru_cache()
def request_time(prefix: str, buckets: t.Tuple[float, ...]) -> prom.Histogram:
    """Return request time metric for the app prefix (cached/singleton)."""
    return prom.Histogram(
        f"{prefix}request_duration_seconds",
        "HTTP request duration in seconds",
        ("method", "path", "status"),
        buckets=buckets,
        registry=get_registry(),
    )


@functools.lru_cache()
def get_registry() -> prom.registry.CollectorRegistry:
    """Get the metrics collector registry."""
    registry = prom.CollectorRegistry()
    if "prometheus_multiproc_dir" in os.environ:
        MultiProcessCollector(registry)
    return registry


def get_metrics(_: Request) -> Response:
    """Handler exposing the prometheus metrics."""
    metrics = prom.generate_latest(get_registry())
    return Response(metrics, media_type=prom.CONTENT_TYPE_LATEST)
