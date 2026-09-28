Fraud Streaming Project - Docker / Compose / CI-CD Overlay v2
==============================================================

هذه الحزمة محدثة حسب المشروع الفعلي:

FastAPI 0.141.1
Uvicorn 0.53.0
MLflow 3.16.1
PySpark 3.5.9
Python 3.12
MLflow data:
  fraud_streaming_project/mlflow_data/

مهم:
-----
لا تشغل Docker الآن.
الحزمة فقط لنسخ ملفات الإعداد داخل المشروع.

ما سيتم نسخه:
--------------
fastapi_service/Dockerfile
fastapi_service/.dockerignore

streamlit_app/Dockerfile
streamlit_app/.dockerignore

docker-compose.app.yml
docker-compose.full.yml
.env.docker.example

monitoring/prometheus-docker.yml

.github/workflows/ci.yml
.github/workflows/cd-template.yml

ملاحظة Streamlit:
-----------------
كود Streamlit الحالي عندك موجود على Windows.
قبل أي Docker build لاحقاً، انسخ ملفات Streamlit الفعلية إلى:
~/fraud_streaming_project/streamlit_app/

المطلوب عادة:
app.py
api_client.py
config.py
requirements.txt
.env.example

ملاحظة MLflow:
--------------
الـ MLflow الحالي يحتوي الـ Registry والـ champion model.
في الـ Full Compose تم إعداد MLflow لاستخدام مجلد:
./mlflow_data

لكن لا تشغل الـ Full Compose الآن.
قبل التشغيل الفعلي سنأخذ Backup ونراجع Artifact paths.

ملاحظة Spark Streaming:
-----------------------
هذه الحزمة تجهز Infrastructure + API/UI + Monitoring.
لم نضع 10_realtime_fraud_scoring.py و consumers داخل Containers حتى الآن،
لأننا سننشئ لهم Worker Image منفصل بعد مراجعة Dependencies وSpark packages/JARs.
هذا أفضل من وضع Container ناقص أو غير مطابق للمشروع.
