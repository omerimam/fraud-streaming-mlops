import os
from dotenv import load_dotenv
load_dotenv()
FASTAPI_BASE_URL=os.getenv("FASTAPI_BASE_URL","http://127.0.0.1:8000")
REQUEST_TIMEOUT=int(os.getenv("REQUEST_TIMEOUT","30"))
