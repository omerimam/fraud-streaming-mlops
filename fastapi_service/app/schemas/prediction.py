from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field

class PredictionRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "trans_num": "API_TEST_001",
                "trans_date_trans_time": "2026-09-26T21:30:00",
                "dob": "1985-06-15",
                "amt": 950.50,
                "city_pop": 120000,
                "lat": 24.7136,
                "long": 46.6753,
                "merch_lat": 25.1972,
                "merch_long": 55.2744,
                "category": "shopping_net",
                "gender": "M",
                "state": "CA"
            }
        }
    )

    trans_num: str | None = Field(default=None, max_length=128)
    trans_date_trans_time: datetime
    dob: date
    amt: float = Field(gt=0)
    city_pop: int = Field(gt=0)
    lat: float = Field(ge=-90, le=90)
    long: float = Field(ge=-180, le=180)
    merch_lat: float = Field(ge=-90, le=90)
    merch_long: float = Field(ge=-180, le=180)
    category: str = Field(min_length=1, max_length=100)
    gender: str = Field(min_length=1, max_length=20)
    state: str = Field(min_length=1, max_length=50)

class PredictionResponse(BaseModel):
    trans_num: str | None = None
    prediction: float
    prediction_label: str
    fraud_probability: float
    model_name: str
    model_alias: str
    model_version: str
    model_run_id: str

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str

class ReadinessResponse(BaseModel):
    status: str
    spark_ready: bool
    preprocessing_loaded: bool
    fraud_model_loaded: bool
    error: str | None = None

class ModelInfoResponse(BaseModel):
    model_name: str
    alias: str
    version: str | None = None
    run_id: str | None = None
    preprocessing_uri: str | None = None
    fraud_model_uri: str
    loaded: bool
