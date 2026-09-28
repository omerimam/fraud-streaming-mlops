Fraud Detection Streamlit Frontend - Windows
=============================================

Streamlit يعمل على Windows كواجهة فقط.
لا يقرأ ملفات مشروع Linux ولا يحمل Spark/MLflow.
هو يتصل بـ FastAPI داخل WSL عبر HTTP.

المسار:
Windows Streamlit -> FastAPI in WSL -> Spark/MLflow -> Prediction

1) شغّل FastAPI داخل WSL:
cd ~/fraud_streaming_project/fastapi_service
source ~/venvs/fraud-spark/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000

2) من Windows اختبر الاتصال:
test_fastapi_connection.bat

3) ثبت المكتبات مرة واحدة:
install_windows.bat

4) شغّل Streamlit:
run_streamlit_windows.bat

الرابط غالباً:
http://localhost:8501

إذا لم يعمل localhost من Windows إلى WSL، نستخدم IP الخاص بـ WSL في ملف .env.
