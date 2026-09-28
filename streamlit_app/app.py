from datetime import date, datetime, time
import requests
import streamlit as st
from api_client import FraudAPIClient
from config import FASTAPI_BASE_URL

st.set_page_config(page_title="Fraud Detection System", page_icon="🔍", layout="wide")
api = FraudAPIClient()
st.title("Fraud Detection System")
st.caption("Windows Streamlit Frontend → FastAPI in WSL → Spark → MLflow Champion Model")

st.sidebar.header("System Status")
st.sidebar.write(f"FastAPI: `{FASTAPI_BASE_URL}`")
try:
    health = api.health()
    st.sidebar.success("FastAPI: ONLINE")
    st.sidebar.write(f"Environment: `{health.get('environment','-')}`")
except Exception as exc:
    st.sidebar.error("FastAPI: OFFLINE")
    st.sidebar.caption(str(exc))

tab_predict, tab_model, tab_arch = st.tabs(["Fraud Prediction","Model / API Status","Architecture"])

with tab_predict:
    st.subheader("Single Transaction Prediction")
    with st.form("fraud_prediction_form"):
        c1,c2=st.columns(2)
        with c1:
            trans_num=st.text_input("Transaction ID", value="STREAMLIT_TEST_001")
            transaction_date=st.date_input("Transaction Date", value=date.today())
            transaction_time=st.time_input("Transaction Time", value=time(12,0))
            dob=st.date_input("Customer Date of Birth", value=date(1985,6,15))
            amt=st.number_input("Amount", min_value=0.01, value=950.50, step=10.0)
            city_pop=st.number_input("City Population", min_value=1, value=120000, step=1000)
        with c2:
            category=st.text_input("Category", value="shopping_net")
            gender=st.selectbox("Gender", ["M","F"])
            state=st.text_input("State", value="CA")
            lat=st.number_input("Customer Latitude", min_value=-90.0, max_value=90.0, value=24.7136, format="%.6f")
            long=st.number_input("Customer Longitude", min_value=-180.0, max_value=180.0, value=46.6753, format="%.6f")
            merch_lat=st.number_input("Merchant Latitude", min_value=-90.0, max_value=90.0, value=25.1972, format="%.6f")
            merch_long=st.number_input("Merchant Longitude", min_value=-180.0, max_value=180.0, value=55.2744, format="%.6f")
        submit=st.form_submit_button("Predict Fraud", use_container_width=True)

    if submit:
        payload={
            "trans_num": trans_num,
            "trans_date_trans_time": datetime.combine(transaction_date, transaction_time).isoformat(),
            "dob": dob.isoformat(),
            "amt": float(amt),
            "city_pop": int(city_pop),
            "lat": float(lat),
            "long": float(long),
            "merch_lat": float(merch_lat),
            "merch_long": float(merch_long),
            "category": category.strip(),
            "gender": gender,
            "state": state.strip(),
        }
        try:
            with st.spinner("Running fraud prediction..."):
                result=api.predict(payload)
            label=result.get("prediction_label")
            prob=float(result.get("fraud_probability",0))
            st.divider()
            if label == "FRAUD":
                st.error("FRAUD DETECTED")
            else:
                st.success("NORMAL TRANSACTION")
            a,b,c=st.columns(3)
            a.metric("Prediction",label)
            b.metric("Fraud Probability",f"{prob*100:.2f}%")
            c.metric("Model Version",result.get("model_version","-"))
            st.progress(min(max(prob,0.0),1.0))
            st.subheader("Prediction Details")
            st.json(result)
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to FastAPI.")
            st.info(f"Make sure FastAPI is running inside WSL on {FASTAPI_BASE_URL}")
        except requests.exceptions.Timeout:
            st.error("FastAPI request timed out.")
        except requests.exceptions.HTTPError as exc:
            st.error("FastAPI returned an error.")
            try: st.json(exc.response.json())
            except Exception: st.code(str(exc))
        except Exception as exc:
            st.exception(exc)

with tab_model:
    st.subheader("FastAPI and ML Model Status")
    c1,c2=st.columns(2)
    with c1:
        if st.button("Check API Health", use_container_width=True):
            try: st.json(api.health())
            except Exception as exc: st.error(str(exc))
    with c2:
        if st.button("Check Model Readiness", use_container_width=True):
            try: st.json(api.ready())
            except Exception as exc: st.error(str(exc))
    if st.button("Get MLflow Model Information", use_container_width=True):
        try: st.json(api.model_info())
        except Exception as exc: st.error(str(exc))

with tab_arch:
    st.subheader("Online Prediction Flow")
    st.code("Windows User\n↓\nStreamlit on Windows\n↓\nFastAPI in WSL\n↓\nSpark Feature Engineering\n↓\nMLflow preprocessing_model\n↓\nFraudLogisticRegression@champion\n↓\nFRAUD / NORMAL + probability\n↓\nJSON Response\n↓\nStreamlit", language=None)
