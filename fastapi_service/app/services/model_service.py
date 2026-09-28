import logging
import threading

import mlflow
from mlflow import MlflowClient
from pyspark.ml.functions import vector_to_array
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DateType, DoubleType, LongType, StringType,
    StructField, StructType, TimestampType
)

from app.core.config import Settings
from app.schemas.prediction import PredictionRequest
from app.services.feature_engineering import add_training_features

logger = logging.getLogger("fraud_api.model_service")

INPUT_SCHEMA = StructType([
    StructField("trans_num", StringType(), True),
    StructField("trans_date_trans_time", TimestampType(), False),
    StructField("dob", DateType(), False),
    StructField("amt", DoubleType(), False),
    StructField("city_pop", LongType(), False),
    StructField("lat", DoubleType(), False),
    StructField("long", DoubleType(), False),
    StructField("merch_lat", DoubleType(), False),
    StructField("merch_long", DoubleType(), False),
    StructField("category", StringType(), False),
    StructField("gender", StringType(), False),
    StructField("state", StringType(), False),
])

class ModelService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.spark = None
        self.preprocessing_model = None
        self.fraud_model = None
        self.model_version = None
        self.model_run_id = None
        self.preprocessing_uri = None
        self.load_error = None
        self._load_lock = threading.Lock()
        self._predict_lock = threading.Lock()

    @property
    def is_ready(self) -> bool:
        return all([
            self.spark is not None,
            self.preprocessing_model is not None,
            self.fraud_model is not None,
            self.model_version is not None,
            self.model_run_id is not None,
        ])

    def start(self) -> None:
        with self._load_lock:
            try:
                self.spark = (
                    SparkSession.builder
                    .appName(self.settings.spark_app_name)
                    .master(self.settings.spark_master)
                    .config(
                        "spark.ui.enabled",
                        str(self.settings.spark_ui_enabled).lower()
                    )
                    .getOrCreate()
                )
                self.spark.sparkContext.setLogLevel("WARN")

                mlflow.set_tracking_uri(self.settings.mlflow_tracking_uri)
                client = MlflowClient(
                    tracking_uri=self.settings.mlflow_tracking_uri
                )

                mv = client.get_model_version_by_alias(
                    name=self.settings.mlflow_registered_model,
                    alias=self.settings.mlflow_model_alias,
                )

                self.model_version = str(mv.version)
                self.model_run_id = mv.run_id
                self.preprocessing_uri = (
                    f"runs:/{self.model_run_id}/preprocessing_model"
                )

                self.preprocessing_model = mlflow.spark.load_model(
                    self.preprocessing_uri
                )
                self.fraud_model = mlflow.spark.load_model(
                    self.settings.fraud_model_uri
                )

                self.load_error = None
                logger.info(
                    "Spark preprocessing and fraud model loaded successfully"
                )

            except Exception as exc:
                self.load_error = str(exc)
                logger.exception(
                    "Failed to initialize fraud model service"
                )

    def stop(self) -> None:
        if self.spark is not None:
            try:
                self.spark.stop()
            finally:
                self.spark = None

    def predict(self, payload: PredictionRequest) -> dict:
        if not self.is_ready:
            raise RuntimeError(
                f"Model service is not ready. Reason: {self.load_error}"
            )

        with self._predict_lock:
            row = {
                "trans_num": payload.trans_num,
                "trans_date_trans_time": payload.trans_date_trans_time,
                "dob": payload.dob,
                "amt": float(payload.amt),
                "city_pop": int(payload.city_pop),
                "lat": float(payload.lat),
                "long": float(payload.long),
                "merch_lat": float(payload.merch_lat),
                "merch_long": float(payload.merch_long),
                "category": payload.category,
                "gender": payload.gender,
                "state": payload.state,
            }

            raw_df = self.spark.createDataFrame([row], schema=INPUT_SCHEMA)
            features_df = add_training_features(raw_df)
            prepared_df = self.preprocessing_model.transform(features_df)
            scored_df = self.fraud_model.transform(prepared_df)

            scored_df = (
                scored_df
                .withColumn(
                    "fraud_probability",
                    vector_to_array(F.col("probability"))[1]
                )
                .withColumn(
                    "prediction_label",
                    F.when(
                        F.col("prediction") == 1.0,
                        F.lit("FRAUD")
                    ).otherwise(F.lit("NORMAL"))
                )
            )

            result = (
                scored_df
                .select(
                    "prediction",
                    "prediction_label",
                    "fraud_probability",
                )
                .first()
            )

            if result is None:
                raise RuntimeError("Spark model returned no prediction")

            return {
                "prediction": float(result["prediction"]),
                "prediction_label": str(result["prediction_label"]),
                "fraud_probability": float(result["fraud_probability"]),
            }
