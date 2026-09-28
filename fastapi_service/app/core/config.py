from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Fraud Detection API"
    app_version: str = "2.0.0"
    environment: str = "local"
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"

    mlflow_tracking_uri: str = "http://127.0.0.1:5000"
    mlflow_registered_model: str = "FraudLogisticRegression"
    mlflow_model_alias: str = "champion"

    spark_app_name: str = "fraud-fastapi-serving"
    spark_master: str = "local[*]"
    spark_ui_enabled: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def fraud_model_uri(self) -> str:
        return f"models:/{self.mlflow_registered_model}@{self.mlflow_model_alias}"

@lru_cache
def get_settings() -> Settings:
    return Settings()
