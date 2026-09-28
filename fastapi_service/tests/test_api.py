from unittest.mock import patch
from fastapi.testclient import TestClient

def test_root_and_health():
    with patch(
        "app.main.ModelService.start",
        return_value=None,
    ):
        from app.main import app
        with TestClient(app) as client:
            r = client.get("/")
            assert r.status_code == 200
            assert r.json()["service"] == "Fraud Detection API"

            h = client.get("/api/v1/health")
            assert h.status_code == 200
            assert h.json()["status"] == "ok"

def test_invalid_prediction_request():
    with patch(
        "app.main.ModelService.start",
        return_value=None,
    ):
        from app.main import app
        with TestClient(app) as client:
            r = client.post(
                "/api/v1/predict",
                json={"trans_num": "INVALID_ONLY"},
            )
            assert r.status_code == 422
