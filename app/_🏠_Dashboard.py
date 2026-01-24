import streamlit as st
import pandas as pd
from datetime import datetime
from utils import load_orders, load_suppliers, load_risk_report, load_anomalies
from app.theme import apply_dark_theme

st.set_page_config(
    page_title="APIS Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_dark_theme()

st.markdown("""
<h1 style="font-size:3.3rem; font-weight:900; margin-bottom:0.2rem;">
🚀 Adaptive Procurement Intelligence System
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style="
    font-size:1.15rem;
    color:#9ca3af;
    line-height:1.7;
    margin-top:0.2rem;
    max-width: 1100px;
">
<b style="color:#e5e7eb;">APIS (Adaptive Procurement Intelligence System)</b> is an AI-powered dashboard built to monitor procurement performance in real time.  
It helps analyze orders, evaluate supplier reliability, detect anomalies, and predict delivery risks.  
With interactive analytics and automated reporting, APIS supports faster and smarter decision-making.
</p>
""", unsafe_allow_html=True)

# Feature Highlights
st.markdown("### ✨ Feature Highlights")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🎯 Core Feature", "Risk Scoring", "+Advanced")
with col2:
    st.metric("🤖 AI/ML", "Predictions", "+Real-time")
with col3:
    st.metric("📊 Analytics", "Multi-View", "+Interactive")

st.markdown("""
<style>
.status-strip{
    display:flex;
    gap:0.8rem;
    flex-wrap:wrap;
    margin-top: 0.6rem;
    margin-bottom: 1.2rem;
}
.pill{
    padding:0.45rem 0.75rem;
    border-radius:999px;
    background: rgba(15, 26, 44, 0.45);
    border:1px solid rgba(34,49,77,0.75);
    color:#e5e7eb;
    font-size:0.9rem;
    font-weight:700;
}
.pill span{
    color:#9ca3af;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# Load data once
orders_df = load_orders()
risk_df = load_risk_report()
alerts_df = load_anomalies()

last_updated = datetime.now().strftime("%d %b %Y • %I:%M %p")

total_orders = len(orders_df)
total_alerts = len(alerts_df)

st.markdown(f"""
<div class="status-strip">
    <div class="pill">🟢 <span>System:</span> Online</div>
    <div class="pill">🤖 <span>Model:</span> Ready</div>
    <div class="pill">📦 <span>Total Orders:</span> {total_orders}</div>
    <div class="pill">🚨 <span>Active Alerts:</span> {total_alerts}</div>
    <div class="pill">🕒 <span>Last Updated:</span> {last_updated}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 📈 Trends & Risk Insights")

left, right = st.columns([7, 5])

with left:
    st.subheader("📊 Orders Trend (Sample)")
    
    # If you have a date column, we can do real trend.
    # Otherwise we generate a dummy trend from total orders.
    trend = pd.DataFrame({
        "Day": list(range(1, 15)),
        "Orders": [max(1, int(total_orders/14) + (i % 3) * 2) for i in range(14)]
    })
    st.line_chart(trend.set_index("Day"))

with right:
    st.subheader("🏢 Top Risk Suppliers")
    
    if "supplier_id" in risk_df.columns and "risk_score" in risk_df.columns:
        top_risk = risk_df.sort_values("risk_score", ascending=False).head(5)
        st.dataframe(top_risk[["supplier_id", "risk_score"]], use_container_width=True)
    else:
        st.info("Risk report columns not found (supplier_id / risk_score).")

st.markdown("## 🚨 Alerts & Quick Actions")

a1, a2 = st.columns([7, 5])

with a1:
    st.subheader("🔔 Recent Alerts")
    
    if len(alerts_df) > 0:
        show_cols = alerts_df.columns.tolist()
        st.dataframe(alerts_df.head(5), use_container_width=True)
    else:
        st.success("✅ No anomalies detected recently!")

with a2:
    st.subheader("⚡ Quick Actions")

    st.info("Use these shortcuts for faster workflows.")

    if st.button("📥 Download Supplier Risk Report", use_container_width=True):
        st.switch_page("pages/7_📄_Reports_&_Downloads.py")

    if st.button("📦 Go to Orders Explorer", use_container_width=True):
        st.switch_page("pages/2_📦_Orders_Explorer.py")

    if st.button("🚨 View Alerts & Anomalies", use_container_width=True):
        st.switch_page("pages/4_🚨_Alerts_&_Anomalies.py")

    if st.button("🔁 Retrain Model", use_container_width=True):
        st.switch_page("pages/8_🔁_Retrain_&_Logs.py")

st.markdown("""
---
### 📚 How to Use APIS

Use the **Top navigation bar** to explore different modules:

| Module | Purpose | Features |
|--------|---------|----------|
| **Overview** | Get started | Key metrics & trends |
| **Orders** | Track shipments | Filter & analyze orders |
| **Suppliers** | Manage vendors | Risk assessment & ranking |
| **Alerts** | Monitor issues | Anomalies & risks |
| **Prediction** | Forecast delays | ML-powered predictions |
| **Clustering** | Segment suppliers | K-Means segmentation |
| **Reports** | Download data | CSV exports |
| **Retrain** | Update models | Training logs |

---
**Status:** ✅ Production Ready | **Version:** 2.0 | **Updated:** Real-time Processing
""")
