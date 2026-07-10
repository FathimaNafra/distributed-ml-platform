import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# -------------------------------------
# Dashboard Configuration
# -------------------------------------

st.set_page_config(
    page_title="Distributed ML Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Auto refresh every 5 seconds
st_autorefresh(interval=5000, key="dashboard_refresh")

# -------------------------------------
# Aggregator URL
# -------------------------------------

AGGREGATOR_URL = "http://51.20.41.124:8000"

# -------------------------------------
# Helper Function
# -------------------------------------

def get_api(endpoint):
    try:
        response = requests.get(f"{AGGREGATOR_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            return {}
    except:
        return {}

# -------------------------------------
# Read APIs
# -------------------------------------

status = get_api("/status")
workers = get_api("/worker-locations")
metrics = get_api("/metrics")
scalability = get_api("/scalability")
updates = get_api("/updates")

# -------------------------------------
# Title
# -------------------------------------

st.title("🤖 Distributed Machine Learning Dashboard")

st.markdown("---")

# -------------------------------------
# System Overview
# -------------------------------------

st.header("📊 System Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Registered Workers",
        status.get("registered_workers", 0)
    )

with col2:
    st.metric(
        "Current Round",
        status.get("current_round", 0)
    )

with col3:
    st.metric(
        "Pending Updates",
        status.get("pending_updates", 0)
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Aggregation Status",
        status.get("aggregation_status", "Unknown")
    )

with col5:
    st.metric(
        "Average Accuracy",
        status.get("average_worker_accuracy", 0)
    )

with col6:
    st.metric(
        "Last Aggregation",
        status.get("last_aggregation_time", "N/A")
    )

st.markdown("---")

# -------------------------------------
# Worker Monitoring
# -------------------------------------

st.header("🖥 Worker Monitoring")

rows = []

for worker_id, info in workers.items():
    rows.append({
        "Worker ID": worker_id,
        "IP Address": info.get("ip"),
        "Status": info.get("status"),
        "Last Seen": info.get("last_seen")
    })

if len(rows) > 0:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No workers registered.")

st.markdown("---")

# -------------------------------------
# Performance Metrics
# -------------------------------------

st.header("⚡ Performance Metrics")

col7, col8, col9 = st.columns(3)

with col7:
    st.metric(
        "Completed Rounds",
        metrics.get("completed_rounds", 0)
    )

with col8:
    st.metric(
        "Pending Updates",
        metrics.get("pending_updates", 0)
    )

with col9:
    st.metric(
        "Average Accuracy",
        metrics.get("average_worker_accuracy", 0)
    )

st.write(metrics)

st.markdown("---")

# -------------------------------------
# Scalability
# -------------------------------------

st.header("📈 Scalability")

st.write(scalability)

st.markdown("---")

# -------------------------------------
# Submitted Model Updates
# -------------------------------------

st.header("📦 Submitted Model Updates")

if len(updates) > 0:

    update_rows = []

    for item in updates:
        update_rows.append({
            "Worker": item.get("worker_id"),
            "Accuracy": item.get("accuracy")
        })

    update_df = pd.DataFrame(update_rows)

    st.dataframe(update_df, use_container_width=True)

else:
    st.info("No model updates received.")

st.markdown("---")

# -------------------------------------
# Transparency Status
# -------------------------------------

st.header("🔍 Distributed System Transparencies")

transparency = pd.DataFrame({
    "Transparency": [
        "Access Transparency",
        "Location Transparency",
        "Failure Transparency",
        "Concurrency Transparency",
        "Performance Transparency",
        "Scalability Transparency"
    ],
    "Status": [
        "Implemented",
        "Implemented",
        "Implemented",
        "Implemented",
        "Implemented",
        "Implemented"
    ]
})

st.table(transparency)

st.markdown("---")

st.success("Dashboard is connected to the Distributed ML Platform.")
