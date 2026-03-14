import streamlit as st
import requests
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="AIOps Log Monitoring",
    page_icon="🚨",
    layout="wide"
)

# Title
st.title("🚨 AIOps Log Anomaly Detection Dashboard")

st.write(
    """
This dashboard detects anomalies from system logs using **AI (Isolation Forest)**.
Click the button below to analyze logs.
"""
)

# Detect button
if st.button("🔍 Detect Anomalies"):

    try:
        response = requests.get("http://127.0.0.1:8000/detect")

        if response.status_code == 200:

            data = response.json()

            st.subheader(f"⚠ Total Anomalies Detected: {data['total_anomalies']}")

            anomalies = pd.DataFrame(data["anomalies"])

            if len(anomalies) > 0:

                st.dataframe(
                    anomalies,
                    use_container_width=True
                )

            else:
                st.success("✅ No anomalies detected")

        else:
            st.error("API returned an error")

    except:
        st.error("FastAPI server is not running")

# Sidebar
st.sidebar.title("📊 System Info")

st.sidebar.write("Model : Isolation Forest")
st.sidebar.write("Backend : FastAPI")
st.sidebar.write("Frontend : Streamlit")

st.sidebar.title("⚙ Controls")

if st.sidebar.button("Refresh"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("AIOps Monitoring System")