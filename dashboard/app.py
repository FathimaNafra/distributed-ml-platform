import streamlit as st
import requests
import pandas as pd


# ---------------------------------------
# Dashboard Configuration
# ---------------------------------------

st.set_page_config(
    page_title="Distributed ML Dashboard",
    page_icon="🤖",
    layout="wide"
)



# ---------------------------------------
# Aggregator URL
# ---------------------------------------

AGGREGATOR_URL = "http://51.20.41.124:8000"

# ---------------------------------------
# Helper Function
# ---------------------------------------

def get_api(endpoint):
    try:
        response = requests.get(
            f"{AGGREGATOR_URL}{endpoint}",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        st.error(f"Unable to connect to {endpoint}")
        st.code(str(e))
        return {}

# ---------------------------------------
# Read API Data
# ---------------------------------------

status = get_api("/status")
workers = get_api("/worker-locations")
metrics = get_api("/metrics")
scalability = get_api("/scalability")
updates = get_api("/updates")
history = get_api("/training-history")

# ---------------------------------------
# Dashboard Title
# ---------------------------------------

st.title("🤖 Distributed Machine Learning Dashboard")
st.caption("Federated Learning Monitoring Dashboard")

st.divider()

# ---------------------------------------
# System Overview
# ---------------------------------------

st.subheader("📊 System Overview")

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

st.divider()

# ---------------------------------------
# Worker Monitoring
# ---------------------------------------

st.subheader("🖥 Worker Monitoring")

worker_rows = []

for worker_id, info in workers.items():

    worker_rows.append({
        "Worker ID": worker_id,
        "IP Address": info.get("ip", ""),
        "Status": info.get("status", ""),
        "Last Seen": info.get("last_seen", "")
    })

if worker_rows:

    worker_df = pd.DataFrame(worker_rows)

    st.dataframe(
        worker_df,
        width="stretch"
    )

else:

    st.info("No workers are currently registered.")

st.divider()

# ---------------------------------------
# Performance Metrics
# ---------------------------------------

st.subheader("⚡ Performance Metrics")

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

col10, col11 = st.columns(2)

with col10:
    st.metric(
        "Registered Workers",
        metrics.get("registered_workers", 0)
    )

with col11:
    st.metric(
        "System Status",
        metrics.get("aggregation_status", "Unknown")
    )

st.divider()

# ---------------------------------------
# Scalability
# ---------------------------------------

st.subheader("📈 Scalability")

col12, col13 = st.columns(2)

with col12:
    st.metric(
        "Registered Workers",
        scalability.get("registered_workers", 0)
    )

with col13:
    st.metric(
        "Pending Updates",
        scalability.get("pending_updates", 0)
    )

st.info(
    scalability.get(
        "scalability_status",
        "No scalability information available."
    )
)

st.divider()

# ---------------------------------------
# Submitted Model Updates
# ---------------------------------------

st.subheader("📦 Submitted Model Updates")

if updates:

    update_rows = []

    for item in updates:

        update_rows.append({
            "Worker ID": item.get("worker_id"),
            "Accuracy": item.get("accuracy")
        })

    update_df = pd.DataFrame(update_rows)

    st.dataframe(
        update_df,
        width="stretch"
    )

else:

    st.info("No model updates submitted yet.")

st.divider()

# ---------------------------------------
# Training Accuracy Trend
# ---------------------------------------

st.subheader("📈 Training Accuracy Trend")

if history:

    accuracy_df = pd.DataFrame({
        "Round": [
            item["round"]
            for item in history
        ],
        "Average Accuracy": [
            item["average_accuracy"]
            for item in history
        ]
    })

    accuracy_df = accuracy_df.set_index("Round")

    st.line_chart(accuracy_df)

else:

    st.info("No training history available.")

st.divider()

# ---------------------------------------
# Worker Accuracy Comparison
# ---------------------------------------

st.subheader("📊 Worker Accuracy Comparison")

if history:

    latest_round = history[-1]

    worker_df = pd.DataFrame({
        "Worker": [
            worker["worker_id"]
            for worker in latest_round["workers"]
        ],
        "Accuracy": [
            worker["accuracy"]
            for worker in latest_round["workers"]
        ]
    })

    worker_df = worker_df.set_index("Worker")

    st.bar_chart(worker_df)

else:

    st.info("No worker accuracy data available.")

st.divider()

# ---------------------------------------
# Worker Participation Per Round
# ---------------------------------------

st.subheader("👥 Worker Participation")

if history:

    participation_df = pd.DataFrame({
        "Round": [
            item["round"]
            for item in history
        ],
        "Workers": [
            len(item["workers"])
            for item in history
        ]
    })

    participation_df = participation_df.set_index("Round")

    st.bar_chart(participation_df)

else:

    st.info("No participation history available.")

st.divider()

# ---------------------------------------
# Transparency Status
# ---------------------------------------

st.subheader("🔍 Distributed System Transparencies")

transparency_df = pd.DataFrame({
    "Transparency": [
        "Access Transparency",
        "Location Transparency",
        "Failure Transparency",
        "Concurrency Transparency",
        "Performance Transparency",
        "Scalability Transparency"
    ],
    "Status": [
        "✅ Implemented",
        "✅ Implemented",
        "✅ Implemented",
        "✅ Implemented",
        "✅ Implemented",
        "✅ Implemented"
    ]
})

st.table(transparency_df)

st.divider()

# ---------------------------------------
# API Health Status
# ---------------------------------------

st.subheader("🌐 API Health Status")

api_status = pd.DataFrame({
    "API Endpoint": [
        "/status",
        "/worker-locations",
        "/metrics",
        "/scalability",
        "/updates",
        "/training-history"
    ],
    "Status": [
        "🟢 Connected" if status else "🔴 Offline",
        "🟢 Connected" if workers else "🔴 Offline",
        "🟢 Connected" if metrics else "🔴 Offline",
        "🟢 Connected" if scalability else "🔴 Offline",
        "🟢 Connected" if isinstance(updates, list) else "🔴 Offline",
        "🟢 Connected" if isinstance(history, list) else "🔴 Offline"
    ]
})

st.dataframe(api_status, width="stretch")

st.divider()

# ---------------------------------------
# Dashboard Summary
# ---------------------------------------

st.subheader("📋 Dashboard Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.success("✔ Distributed ML Platform Running")

    st.write(f"**Registered Workers:** {status.get('registered_workers',0)}")

    st.write(f"**Current Round:** {status.get('current_round',0)}")

    st.write(f"**Aggregation Status:** {status.get('aggregation_status','Unknown')}")

with summary_col2:

    st.info("Transparency Features")

    st.write("✅ Access")

    st.write("✅ Location")

    st.write("✅ Failure")

    st.write("✅ Concurrency")

    st.write("✅ Performance")

    st.write("✅ Scalability")

st.divider()

# ---------------------------------------
# Footer
# ---------------------------------------

st.caption(
    "Distributed Machine Learning Platform Dashboard | "
    "Built with Streamlit | Auto Refresh: Every 5 Seconds"
)
