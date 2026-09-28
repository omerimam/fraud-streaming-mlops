# Fraud Streaming & MLOps Platform

End-to-end fraud detection project covering offline model training, CDC streaming, online inference, monitoring, Docker, and CI/CD.

## Architecture

```text
Historical PostgreSQL data
  → Spark JDBC
  → Cleaning + Feature Engineering
  → Chronological Train/Test
  → Logistic Regression
  → MLflow
  → FraudLogisticRegression@champion

New PostgreSQL INSERT/UPDATE
  → WAL
  → Debezium CDC
  → Kafka
  → Spark Structured Streaming
  → Same Feature Engineering
  → MLflow champion
  → Prediction
  → Kafka scored topic
  → MySQL / MongoDB

User
  → Streamlit
  → FastAPI
  → Spark preprocessing
  → MLflow champion
  → FRAUD/NORMAL + probability
```

## Stack

Python 3.12, PySpark 3.5.9, PostgreSQL, Debezium, Kafka, MySQL, MongoDB, MLflow 3.16.1, FastAPI, Streamlit, Evidently, Prometheus, Grafana, Docker Compose, GitHub Actions.

## CI

`.github/workflows/ci.yml` validates Python syntax, runs FastAPI tests, validates Compose files, and builds FastAPI and Streamlit images.

## CD

`.github/workflows/cd-template.yml` is intentionally a template until a real deployment target is selected.

## Security

Do not commit `.env`, passwords, tokens, production credentials, local MLflow state, Spark checkpoints, generated monitoring data, or local model artifacts.
