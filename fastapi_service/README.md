# Fraud Detection FastAPI Service v2

This version uses the same scoring logic as the Spark streaming job:

Raw transaction
→ Spark feature engineering
→ preprocessing model from the same MLflow run
→ FraudLogisticRegression@champion
→ probability + prediction label

Run locally:

```bash
cd ~/fraud_streaming_project/fastapi_service
source ~/venvs/fraud-spark/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Swagger:
http://127.0.0.1:8000/docs

Startup can take time because Spark and both MLflow Spark models are
loaded once before the service is ready.
