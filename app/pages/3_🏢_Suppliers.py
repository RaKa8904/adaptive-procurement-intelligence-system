import streamlit as st
from app.utils import load_suppliers, load_risk_report
import pandas as pd

from app.theme import apply_dark_theme
apply_dark_theme()

st.set_page_config(page_title="Suppliers", layout="wide")

# Custom styling
st.markdown("""
<style>
    .risk-score-high {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 6px;
        text-align: center;
        font-weight: 700;
    }
    
    .risk-score-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 6px;
        text-align: center;
        font-weight: 700;
    }
    
    .risk-score-low {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 6px;
        text-align: center;
        font-weight: 700;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #06b6d4;
        padding-bottom: 0.5rem;
    }
    
    .supplier-card {
        background: #111c2e;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        margin-bottom: 0.5rem;
        border: 1px solid #22314d;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🏢 Supplier Intelligence Center")
st.markdown("Comprehensive supplier management and risk assessment")

suppliers = load_suppliers()
risk_report = load_risk_report()

# KPI Cards
st.markdown("### 📊 Supplier Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_suppliers = len(suppliers)
    st.metric("📦 Total Suppliers", f"{total_suppliers:,}")

with col2:
    high_risk = (risk_report["risk_score"] >= 70).sum()
    st.metric("🚨 High Risk", f"{high_risk:,}")

with col3:
    medium_risk = ((risk_report["risk_score"] >= 40) & (risk_report["risk_score"] < 70)).sum()
    st.metric("⚠️ Medium Risk", f"{medium_risk:,}")

with col4:
    low_risk = (risk_report["risk_score"] < 40).sum()
    st.metric("✅ Low Risk", f"{low_risk:,}")

# Risk Distribution Chart
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Risk Score Distribution")
    risk_data = pd.DataFrame({
        'Risk Level': ['Low (<40)', 'Medium (40-70)', 'High (≥70)'],
        'Count': [low_risk, medium_risk, high_risk]
    })
    st.bar_chart(risk_data.set_index('Risk Level'))

with col2:
    st.markdown("### 🎯 Risk Composition")
    st.bar_chart(risk_data.set_index('Risk Level'))

# Supplier Master Data
st.markdown(f"<div class='section-header'>🏢 Supplier Master Data</div>", unsafe_allow_html=True)

search_term = st.text_input("🔍 Search suppliers", placeholder="Search by supplier ID or name")

if search_term:
    suppliers_filtered = suppliers[suppliers.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)]
else:
    suppliers_filtered = suppliers

st.info(f"Showing {len(suppliers_filtered)} suppliers")
st.dataframe(
    suppliers_filtered,
    use_container_width=True,
    hide_index=True
)

# Risk Ranking
st.markdown(f"<div class='section-header'>📌 Risk-Based Ranking</div>", unsafe_allow_html=True)

risk_sorted = risk_report.sort_values("risk_score", ascending=False)

# Add risk level category
risk_sorted_display = risk_sorted.copy()
risk_sorted_display['Risk Level'] = risk_sorted_display['risk_score'].apply(
    lambda x: '🔴 HIGH' if x >= 70 else ('🟠 MEDIUM' if x >= 40 else '🟢 LOW')
)

sort_ascending = st.checkbox("Sort by lowest risk first")
if sort_ascending:
    risk_sorted_display = risk_sorted_display.sort_values("risk_score", ascending=True)

st.dataframe(
    risk_sorted_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "risk_score": st.column_config.ProgressColumn(
            "Risk Score",
            min_value=0,
            max_value=100
        )
    }
)
