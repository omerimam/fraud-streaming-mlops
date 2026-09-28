import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
)

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.services.model_service import ModelService

configure_logging()
logger = logging.getLogger("fraud_api")
settings = get_settings()

REQUEST_COUNT = Counter(
    "fraud_api_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "fraud_api_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Fraud Detection API")
    service = ModelService(settings)
    app.state.model_service = service
    service.start()
    yield
    service.stop()
    logger.info("Stopping Fraud Detection API")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Fraud prediction API using the same Spark feature engineering, "
        "MLflow preprocessing model and champion fraud model as the "
        "streaming pipeline."
    ),
    lifespan=lifespan,
)

@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        duration = time.perf_counter() - start
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=str(status_code),
        ).inc()
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)
        logger.info(
            "HTTP request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_seconds": round(duration, 6),
            },
        )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled API exception",
        extra={"path": request.url.path, "method": request.method},
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.get("/", tags=["System"])
def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs",
        "health": "/api/v1/health",
        "ready": "/api/v1/ready",
        "model_info": "/api/v1/model-info",
        "predict": "/api/v1/predict",
        "metrics": "/metrics",
    }

@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )

app.include_router(router, prefix="/api/v1")
