import streamlit as st
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


st.markdown("""
<style>
.module-grid{
    display:grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-top: 1rem;
}
.module-card{
    background:#111c2e;
    border:1px solid #22314d;
    border-radius:16px;
    padding:1.2rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
    transition:0.2s ease;
}
.module-card:hover{
    transform: translateY(-4px);
    border-color:#22d3ee;
}
.module-title{
    font-size:1.1rem;
    font-weight:900;
    color:#e5e7eb;
    margin-bottom:0.4rem;
}
.module-desc{
    color:#9ca3af;
    font-size:0.9rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="module-grid">
    <div class="module-card">
        <div class="module-title">📊 Overview</div>
        <div class="module-desc">KPIs, trends, and quick insights.</div>
    </div>
    <div class="module-card">
        <div class="module-title">📦 Orders Explorer</div>
        <div class="module-desc">Filter, sort and analyze orders.</div>
    </div>
    <div class="module-card">
        <div class="module-title">🏢 Suppliers</div>
        <div class="module-desc">Supplier ranking & risk assessment.</div>
    </div>
    <div class="module-card">
        <div class="module-title">🚨 Alerts</div>
        <div class="module-desc">Anomalies & risk monitoring.</div>
    </div>
</div>
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
