from fastapi import APIRouter, HTTPException, Request, status
from app.core.config import get_settings
from app.schemas.prediction import (
    HealthResponse, ModelInfoResponse, PredictionRequest,
    PredictionResponse, ReadinessResponse
)

router = APIRouter()
settings = get_settings()

@router.get("/health", response_model=HealthResponse, tags=["System"])
def health():
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )

@router.get("/ready", response_model=ReadinessResponse, tags=["System"])
def ready(request: Request):
    service = request.app.state.model_service

    if not service.is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "spark_ready": service.spark is not None,
                "preprocessing_loaded":
                    service.preprocessing_model is not None,
                "fraud_model_loaded":
                    service.fraud_model is not None,
                "error": service.load_error,
            },
        )

    return ReadinessResponse(
        status="ready",
        spark_ready=True,
        preprocessing_loaded=True,
        fraud_model_loaded=True,
        error=None,
    )

@router.get("/model-info", response_model=ModelInfoResponse, tags=["Model"])
def model_info(request: Request):
    service = request.app.state.model_service
    return ModelInfoResponse(
        model_name=settings.mlflow_registered_model,
        alias=settings.mlflow_model_alias,
        version=service.model_version,
        run_id=service.model_run_id,
        preprocessing_uri=service.preprocessing_uri,
        fraud_model_uri=settings.fraud_model_uri,
        loaded=service.is_ready,
    )

@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(payload: PredictionRequest, request: Request):
    service = request.app.state.model_service

    if not service.is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Fraud model service is not ready",
        )

    try:
        result = service.predict(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {exc}",
        ) from exc

    return PredictionResponse(
        trans_num=payload.trans_num,
        prediction=result["prediction"],
        prediction_label=result["prediction_label"],
        fraud_probability=result["fraud_probability"],
        model_name=settings.mlflow_registered_model,
        model_alias=settings.mlflow_model_alias,
        model_version=service.model_version,
        model_run_id=service.model_run_id,
    )
