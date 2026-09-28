import requests
from config import FASTAPI_BASE_URL, REQUEST_TIMEOUT

class FraudAPIClient:
    def __init__(self): self.base_url=FASTAPI_BASE_URL.rstrip("/")
    def health(self):
        r=requests.get(f"{self.base_url}/api/v1/health", timeout=REQUEST_TIMEOUT); r.raise_for_status(); return r.json()
    def ready(self):
        r=requests.get(f"{self.base_url}/api/v1/ready", timeout=REQUEST_TIMEOUT); r.raise_for_status(); return r.json()
    def model_info(self):
        r=requests.get(f"{self.base_url}/api/v1/model-info", timeout=REQUEST_TIMEOUT); r.raise_for_status(); return r.json()
    def predict(self,payload):
        r=requests.post(f"{self.base_url}/api/v1/predict", json=payload, timeout=REQUEST_TIMEOUT); r.raise_for_status(); return r.json()
