Fraud Streaming Project - Docker + CI/CD Complete v4
====================================================

هذه النسخة هي تحديث كامل لحزمة Docker السابقة.

أهم التعديلات
-------------
1) تصحيح مسار MLflow الحالي:
   قاعدة mlflow.db عندك تحفظ الـ artifacts بالمسار:
   /home/omer/fraud_streaming_project/mlflow_data/artifacts

   لذلك docker-compose.full.yml يركب:
   ./mlflow_data
   داخل Container على:
   /home/omer/fraud_streaming_project/mlflow_data

   حتى يبقى:
   FraudLogisticRegression
   alias = champion
   run_id = 5ff124fbd79c487f8b1988ce274d22b3
   قادراً على الوصول إلى artifacts القديمة.

2) CI أصبح جاهزاً لـ:
   - Python 3.12
   - Java 17
   - PySpark
   - pytest
   - Python syntax validation
   - docker compose config validation
   - FastAPI Docker image build
   - Streamlit Docker image build

3) docker-compose.app.yml:
   FastAPI + Streamlit فقط.
   مناسب لاحقاً كاختبار أخف.

4) docker-compose.full.yml:
   PostgreSQL
   Kafka
   Debezium Connect
   MySQL
   MongoDB
   MLflow
   FastAPI
   Streamlit
   Prometheus
   Grafana

مهم
----
لا تحتاج تشغيل Docker الآن.
ضع هذه الملفات مع المشروع الكامل على Windows.

الهيكل المتوقع لاحقاً:
fraud_streaming_project/
  fastapi_service/
  streamlit_app/
  mlflow_data/
  monitoring/
  .github/
  docker-compose.app.yml
  docker-compose.full.yml
  .env.docker.example

هذه الحزمة لا تستبدل كود مشروع Fraud نفسه؛
هي حزمة Docker / Compose / CI-CD كاملة تُدمج مع ملفات المشروع الحقيقية.
