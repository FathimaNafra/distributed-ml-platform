import streamlit as st
import requests
import pandas as pd
import plotly.express as px
# -------------------------------------------------------
# Dashboard Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Distributed ML Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# Custom CSS
# -------------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.metric-container{
    background:#1E293B;
    padding:15px;
    border-radius:10px;
}

h1,h2,h3{
    color:white;
}

div[data-testid="metric-container"]{
    background-color:#1E293B;
    border:1px solid #334155;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.title("🤖 Distributed ML")

st.sidebar.markdown("---")

st.sidebar.info(
"""
### Dashboard

Monitor

- Worker Registration
- Training Progress
- Aggregation
- Performance
- Scalability
- Transparency
"""
)

st.sidebar.markdown("---")

EXPECTED_WORKERS = 3

st.sidebar.write(f"Expected Workers : **{EXPECTED_WORKERS}**")

# -------------------------------------------------------
# Aggregator URL
# -------------------------------------------------------

AGGREGATOR_URL = "http://16.171.129.6:8000"

# -------------------------------------------------------
# Helper Function
# -------------------------------------------------------

def get_api(endpoint):

    try:

        response = requests.get(
            f"{AGGREGATOR_URL}{endpoint}",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        st.error(f"Cannot connect to {endpoint}")

        st.write(e)

        if endpoint in ["/updates", "/training-history"]:
            return []

        return {}

# -------------------------------------------------------
# Read APIs
# -------------------------------------------------------

status = get_api("/status")

workers = get_api("/worker-locations")

metrics = get_api("/metrics")

scalability = get_api("/scalability")

updates = get_api("/updates")

history = get_api("/training-history")

# -------------------------------------------------------
# Dashboard Title
# -------------------------------------------------------

st.title("🤖 Distributed Machine Learning Dashboard")

st.caption(
    "Real-Time Monitoring Dashboard for Distributed Machine Learning Platform"
)

st.divider()

# -------------------------------------------------------
# System Overview
# -------------------------------------------------------

st.header("📊 System Overview")

registered_workers = status.get("registered_workers", 0)
current_round = status.get("current_round", 0)
pending_workers = status.get("pending_workers", 0)
aggregation_status = status.get("aggregation_status", "Unknown")
average_accuracy = status.get("average_worker_accuracy", 0)
last_aggregation = status.get("last_aggregation_time", "Not Available")

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Registered Workers",
        registered_workers
    )

with col2:
    st.metric(
        "🔄 Current Round",
        current_round
    )

with col3:
    st.metric(
        "⏳ Pending Workers",
        pending_workers
    )

with col4:
    if average_accuracy:
        st.metric(
            "🎯 Average Accuracy",
            f"{average_accuracy:.4f}"
        )
    else:
        st.metric(
            "🎯 Average Accuracy",
            "N/A"
        )

st.markdown("")

col5, col6 = st.columns(2)

with col5:

    if aggregation_status == "Completed":
        st.success("✅ Aggregation Completed")

    elif aggregation_status == "Waiting":
        st.warning("⏳ Waiting for Workers")

    else:
        st.info("🟢 System Ready")

with col6:

    st.info(f"🕒 Last Aggregation : {last_aggregation}")

st.divider()

# -------------------------------------------------------
# Worker Registration Progress
# -------------------------------------------------------

st.subheader("👥 Worker Registration Progress")

progress = registered_workers / EXPECTED_WORKERS

st.progress(progress)

st.write(
    f"**{registered_workers} of {EXPECTED_WORKERS} Workers Registered**"
)

remaining = EXPECTED_WORKERS - registered_workers

if remaining > 0:

    st.warning(
        f"⚠ Waiting for **{remaining}** more worker(s)."
    )

else:

    st.success(
        "🎉 All expected workers have registered."
    )

st.divider()

# -------------------------------------------------------
# System Health
# -------------------------------------------------------

st.subheader("❤️ System Health")

health_col1, health_col2, health_col3 = st.columns(3)

with health_col1:

    if registered_workers == EXPECTED_WORKERS:
        st.success("🟢 Worker Registration Healthy")
    else:
        st.warning("🟡 Waiting for Workers")

with health_col2:

    if aggregation_status == "Completed":
        st.success("🟢 Aggregation Healthy")
    else:
        st.warning("🟡 Aggregation Pending")

with health_col3:

    if average_accuracy and average_accuracy >= 0.80:
        st.success("🟢 Model Performance Good")
    elif average_accuracy:
        st.warning("🟡 Model Needs Improvement")
    else:
        st.info("⚪ No Training Completed Yet")

st.divider()

# -------------------------------------------------------
# Quick Statistics
# -------------------------------------------------------

st.subheader("📌 Quick Statistics")

stats_col1, stats_col2 = st.columns(2)

with stats_col1:

    st.write(f"**Expected Workers:** {EXPECTED_WORKERS}")

    st.write(f"**Registered Workers:** {registered_workers}")

    st.write(f"**Pending Workers:** {pending_workers}")

with stats_col2:

    completed = metrics.get("completed_rounds", 0)

    st.write(f"**Completed Rounds:** {completed}")

    st.write(f"**Aggregation Status:** {aggregation_status}")

    st.write(f"**Average Accuracy:** {average_accuracy}")

st.divider()

# =======================================================
# Worker Monitoring
# =======================================================

st.header("🖥️ Worker Monitoring")

if workers:

    worker_rows = []

    for worker_id, info in workers.items():

        worker_rows.append({
            "Worker ID": worker_id,
            "IP Address": info.get("ip", ""),
            "Status": "🟢 " + info.get("status", ""),
            "Last Seen": info.get("last_seen", "")
        })

    worker_df = pd.DataFrame(worker_rows)

    st.dataframe(
        worker_df,
        width="stretch",
        hide_index=True
    )

else:

    st.warning("No workers registered.")

st.divider()

# =======================================================
# Worker Leaderboard
# =======================================================

st.header("🏆 Worker Accuracy Leaderboard")

if history:

    latest_round = history[-1]

    leaderboard = pd.DataFrame(latest_round["workers"])

    leaderboard = leaderboard.sort_values(
        by="accuracy",
        ascending=False
    ).reset_index(drop=True)

    leaderboard.insert(
        0,
        "Rank",
        ["🥇","🥈","🥉"][:len(leaderboard)]
    )

    leaderboard.rename(
        columns={
            "worker_id":"Worker",
            "accuracy":"Accuracy"
        },
        inplace=True
    )

    st.dataframe(
        leaderboard,
        width="stretch",
        hide_index=True
    )

else:

    st.info("No worker accuracy available yet.")

st.divider()

# =======================================================
# Performance Metrics
# =======================================================

st.header("⚡ Performance Metrics")

perf1, perf2, perf3 = st.columns(3)

with perf1:

    st.metric(
        "Completed Rounds",
        metrics.get("completed_rounds",0)
    )

with perf2:

    st.metric(
        "Pending Workers",
        metrics.get("pending_workers",0)
    )

with perf3:

    accuracy = metrics.get("average_worker_accuracy",0)

    if accuracy:

        st.metric(
            "Average Accuracy",
            f"{accuracy:.4f}"
        )

    else:

        st.metric(
            "Average Accuracy",
            "N/A"
        )

perf4, perf5 = st.columns(2)

with perf4:

    st.metric(
        "Registered Workers",
        metrics.get("registered_workers",0)
    )

with perf5:

    st.metric(
        "Aggregation Status",
        metrics.get("aggregation_status","Unknown")
    )

st.divider()

# =======================================================
# Scalability
# =======================================================

st.header("📈 Scalability")

scale1, scale2, scale3 = st.columns(3)

with scale1:

    st.metric(
        "Expected Workers",
        EXPECTED_WORKERS
    )

with scale2:

    st.metric(
        "Registered Workers",
        scalability.get("registered_workers",0)
    )

with scale3:

    st.metric(
        "Pending Workers",
        scalability.get("pending_workers",0)
    )

st.success(
    scalability.get(
        "scalability_status",
        "System is scalable."
    )
)

st.divider()

# =======================================================
# Registration Summary
# =======================================================

st.header("📌 Worker Registration Overview")

registered = registered_workers
pending = EXPECTED_WORKERS - registered

pie_df = pd.DataFrame({
    "Status": ["Registered", "Pending"],
    "Workers": [registered, pending]
})

fig = px.pie(
    pie_df,
    values="Workers",
    names="Status",
    hole=0.55,
    color="Status",
    color_discrete_map={
        "Registered": "#00CC96",
        "Pending": "#EF553B"
    }
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)
fig.update_layout(
    template="plotly_dark",
    height=400,
    showlegend=True,
    margin=dict(l=20, r=20, t=40, b=20)
)

# Display the chart
st.plotly_chart(fig, width="stretch")
st.divider()

# =======================================================
# Training Analytics
# =======================================================

st.header("📈 Training Analytics")

left_chart, right_chart = st.columns(2)

# -------------------------------------------------------
# Training Accuracy Trend
# -------------------------------------------------------

with left_chart:

    st.subheader("📈 Accuracy Trend")

    if history:

       accuracy_df = pd.DataFrame({
           "Round": [item["round"] for item in history],
           "Average Accuracy": [item["average_accuracy"] for item in history]
       })

       fig = px.line(
          accuracy_df,
          x="Round",
          y="Average Accuracy",
          markers=True,
          line_shape="spline",
          template="plotly_dark",
          color_discrete_sequence=["#00CC96"]
       )

       fig.update_layout(
          height=420,
          xaxis_title="Training Round",
          yaxis_title="Average Accuracy",
          title="Training Accuracy Over Time"
       )

       st.plotly_chart(fig, width="stretch")

    else:
       st.info("No training history available.")

# -------------------------------------------------------
# Worker Participation
# -------------------------------------------------------

with right_chart:

   st.subheader("👥 Worker Participation")

   if history:

    participation_df = pd.DataFrame({
        "Round": [item["round"] for item in history],
        "Workers": [len(item["workers"]) for item in history]
    })

    fig = px.bar(
        participation_df,
        x="Round",
        y="Workers",
        color="Workers",
        text="Workers",
        template="plotly_dark",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        height=420,
        title="Workers Participated Per Round"
    )

    st.plotly_chart(fig, width="stretch")

   else:
    st.info("No participation history.")
st.divider()

# =======================================================
# Worker Accuracy
# =======================================================

st.header("📊 Worker Accuracy")

if history:

    latest_round = history[-1]

    worker_accuracy = pd.DataFrame({
        "Worker":[
            worker["worker_id"]
            for worker in latest_round["workers"]
        ],
        "Accuracy":[
            worker["accuracy"]
            for worker in latest_round["workers"]
        ]
    })

    worker_accuracy = worker_accuracy.set_index("Worker")

    st.bar_chart(worker_accuracy)

else:

    st.info("No worker accuracy data.")

st.divider()

# =======================================================
# Registration Progress
# =======================================================

st.header("📌 Registration Progress")

progress_col1, progress_col2 = st.columns(2)

with progress_col1:

    registered = registered_workers
    pending = EXPECTED_WORKERS - registered

    registration_df = pd.DataFrame({
        "Category":[
            "Registered",
            "Pending"
        ],
        "Workers":[
            registered,
            pending
        ]
    })

    registration_df = registration_df.set_index("Category")

    st.bar_chart(registration_df)

with progress_col2:

    progress_percentage = (
        registered_workers /
        EXPECTED_WORKERS
    ) * 100

    st.metric(
        "Registration Progress",
        f"{progress_percentage:.0f}%"
    )

    st.progress(
        registered_workers /
        EXPECTED_WORKERS
    )

st.divider()

# =======================================================
# Accuracy Performance Indicator
# =======================================================

st.header("🎯 Accuracy Performance")

accuracy = status.get("average_worker_accuracy", 0)

if accuracy:

    st.progress(float(accuracy))

    if accuracy >= 0.90:

        st.success(
            f"Excellent Accuracy ({accuracy:.4f})"
        )

    elif accuracy >= 0.80:

        st.success(
            f"Good Accuracy ({accuracy:.4f})"
        )

    elif accuracy >= 0.70:

        st.warning(
            f"Average Accuracy ({accuracy:.4f})"
        )

    else:

        st.error(
            f"Low Accuracy ({accuracy:.4f})"
        )

else:

    st.info("Training has not completed yet.")

st.divider()

# =======================================================
# Dashboard Insights
# =======================================================

st.header("📋 Dashboard Insights")

insight1, insight2, insight3 = st.columns(3)

with insight1:

    st.info(
        f"""
        👥 **Workers**

        Registered : {registered_workers}

        Pending : {pending_workers}
        """
    )

with insight2:

    completed_rounds = metrics.get(
        "completed_rounds",
        0
    )

    st.info(
        f"""
        🔄 **Training**

        Completed Rounds : {completed_rounds}

        Current Round : {current_round}
        """
    )

with insight3:

    st.info(
        f"""
        🎯 **Model**

        Accuracy : {average_accuracy}

        Status : {aggregation_status}
        """
    )

st.divider()

# =======================================================
# Submitted Model Updates
# =======================================================

st.header("📦 Submitted Model Updates")

if updates:

    update_df = pd.DataFrame(updates)

    if "worker_id" in update_df.columns and "accuracy" in update_df.columns:

        display_df = update_df[["worker_id", "accuracy"]].rename(
            columns={
                "worker_id": "Worker ID",
                "accuracy": "Accuracy"
            }
        )

        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True
        )

    else:
        st.dataframe(update_df, width="stretch", hide_index=True)

else:

    st.info("No submitted updates available.")

st.divider()

# =======================================================
# Top Performing Worker
# =======================================================

st.header("🏅 Top Performing Worker")

if history:

    latest_round = history[-1]

    best_worker = max(
        latest_round["workers"],
        key=lambda x: x["accuracy"]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.success("🥇 Best Worker")

        st.metric(
            "Worker",
            best_worker["worker_id"]
        )

    with col2:
        st.metric(
            "Accuracy",
            f"{best_worker['accuracy']:.4f}"
        )

else:

    st.info("No worker ranking available.")

st.divider()

# =======================================================
# API Health Dashboard
# =======================================================

st.header("🌐 API Health")

api_health = pd.DataFrame({
    "Endpoint": [
        "/status",
        "/worker-locations",
        "/metrics",
        "/scalability",
        "/updates",
        "/training-history"
    ],
    "Status": [
        "🟢 Online" if status else "🔴 Offline",
        "🟢 Online" if workers else "🔴 Offline",
        "🟢 Online" if metrics else "🔴 Offline",
        "🟢 Online" if scalability else "🔴 Offline",
        "🟢 Online" if isinstance(updates, list) else "🔴 Offline",
        "🟢 Online" if isinstance(history, list) else "🔴 Offline"
    ]
})

st.dataframe(
    api_health,
    width="stretch",
    hide_index=True
)

st.divider()

# =======================================================
# Live System Status
# =======================================================

st.header("🟢 Live System Status")

if aggregation_status == "Completed":

    st.success("✅ Aggregation completed successfully.")

elif aggregation_status == "Waiting":

    st.warning("⏳ Waiting for remaining workers.")

else:

    st.info("🟢 System is ready.")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:

    st.metric(
        "Workers Online",
        registered_workers
    )

with status_col2:

    st.metric(
        "Current Round",
        current_round
    )

with status_col3:

    st.metric(
        "Completed Rounds",
        metrics.get("completed_rounds", 0)
    )

st.divider()

# =======================================================
# Dashboard Summary
# =======================================================

st.header("📋 Dashboard Summary")

summary = f"""
### Current System State

- 👥 Registered Workers : **{registered_workers}/{EXPECTED_WORKERS}**
- ⏳ Pending Workers : **{pending_workers}**
- 🔄 Current Round : **{current_round}**
- 🏁 Completed Rounds : **{metrics.get('completed_rounds',0)}**
- 🎯 Average Accuracy : **{average_accuracy}**
- ⚙ Aggregation Status : **{aggregation_status}**
"""

st.markdown(summary)

st.divider()

# =======================================================
# Distributed System Transparencies
# =======================================================

st.header("🔍 Distributed System Transparencies")

t1, t2, t3 = st.columns(3)

with t1:
    st.success("✅ Access Transparency")
    st.write("Workers access the Aggregator through REST APIs.")

    st.success("✅ Location Transparency")
    st.write("Workers communicate using API endpoints without knowing physical locations.")

with t2:
    st.success("✅ Failure Transparency")
    st.write("Missing workers are detected during aggregation.")

    st.success("✅ Concurrency Transparency")
    st.write("Thread locking protects simultaneous worker submissions.")

with t3:
    st.success("✅ Performance Transparency")
    st.write("Performance metrics are monitored during each round.")

    st.success("✅ Scalability Transparency")
    st.write("New workers can register dynamically without changing the architecture.")

st.divider()

# =======================================================
# Overall Project Progress
# =======================================================

st.header("🚀 Project Progress")

progress_items = {
    "Worker Registration": registered_workers / EXPECTED_WORKERS,
    "Training Progress": min(current_round / 10, 1.0),
    "Dashboard": 1.0,
    "Transparency Features": 1.0
}

for name, value in progress_items.items():
    st.write(f"**{name}**")
    st.progress(value)

st.divider()

# =======================================================
# Platform Overview
# =======================================================

st.header("📌 Platform Overview")

overview_col1, overview_col2 = st.columns(2)

with overview_col1:

    st.info(
        f"""
### System Information

- 🤖 Expected Workers : {EXPECTED_WORKERS}
- 👥 Registered Workers : {registered_workers}
- 🔄 Current Round : {current_round}
- 🏁 Completed Rounds : {metrics.get("completed_rounds",0)}
"""
    )

with overview_col2:

    st.info(
        f"""
### Training Information

- 🎯 Average Accuracy : {average_accuracy}
- ⚙ Aggregation Status : {aggregation_status}
- 📅 Last Aggregation : {last_aggregation}
"""
    )

st.divider()

# =======================================================
# Dashboard Footer
# =======================================================

st.markdown(
"""
---
### 🎓 Distributed Machine Learning Platform

**Technologies Used**

- ⚡ FastAPI
- 🐍 Python
- 📊 Streamlit
- 🌐 REST API
- ☁ AWS EC2

**Features**

✅ Worker Registration

✅ Model Aggregation

✅ Performance Monitoring

✅ Scalability

✅ Distributed System Transparencies

✅ Interactive Dashboard
"""
)

st.success("🎉 Dashboard Connected Successfully")

st.caption(
    "Distributed Machine Learning Platform Dashboard © 2026"
)
