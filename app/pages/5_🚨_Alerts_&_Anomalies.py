import streamlit as st
from app.utils import load_orders
import pandas as pd

from app.theme import apply_dark_theme
apply_dark_theme()

st.set_page_config(page_title="Alerts & Anomalies", layout="wide")

# Custom styling
st.markdown("""
<style>
    .alert-card {
        border-radius: 10px;
        padding: 1.5rem;
        color: white;
        font-weight: 700;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .alert-card:hover {
        transform: translateY(-5px);
    }
    
    .alert-critical {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #ea580c 0%, #b45309 100%);
    }
    
    .alert-info {
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%);
    }
    
    .alert-value {
        font-size: 2.5rem;
        margin: 0.5rem 0;
    }
    
    .alert-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #06b6d4;
        padding-bottom: 0.5rem;
    }
    
    .severity-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    
    .severity-critical {
        background: #fecaca;
        color: #991b1b;
    }
    
    .severity-warning {
        background: #fed7aa;
        color: #b45309;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🚨 Alerts & Anomaly Detection")
st.markdown("Real-time monitoring of critical issues and anomalies")

df = load_orders()

# Create risk_score if missing
if "risk_score" not in df.columns:
    priority_weight = {"Low": 5, "Medium": 10, "High": 20}
    df["priority_weight"] = df["order_priority"].map(priority_weight).fillna(10)
    df["risk_score"] = (
        (df["delay_days"] * 18) +
        (df["defect_rate"] * 100 * 2.5) +
        (df["price_change_percent"].abs() * 1.2) +
        (df["priority_weight"] * 0.6)
    ).clip(0, 100)

# Identify anomalies
high_risk = df[df["risk_score"] >= 70]
high_defect = df[df["defect_rate"] >= 0.06]
price_spike = df[df["price_change_percent"].abs() >= 10]
delayed = df[df["order_status"] == "Delayed"]

# Alert Metrics
st.markdown("### ⚠️ Alert Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="alert-card alert-critical">
        <div class="alert-label">🚨 Critical</div>
        <div class="alert-value">{len(high_risk)}</div>
        <div class="alert-label">High Risk Orders</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="alert-card alert-warning">
        <div class="alert-label">⚠️ Warning</div>
        <div class="alert-value">{len(high_defect)}</div>
        <div class="alert-label">Quality Issues</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="alert-card alert-info">
        <div class="alert-label">📈 Price Alert</div>
        <div class="alert-value">{len(price_spike)}</div>
        <div class="alert-label">Price Anomalies</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="alert-card alert-critical">
        <div class="alert-label">⏳ Delay Alert</div>
        <div class="alert-value">{len(delayed)}</div>
        <div class="alert-label">Delayed Orders</div>
    </div>
    """, unsafe_allow_html=True)

# Detailed Analysis Tabs
st.markdown(f"<div class='section-header'>📊 Anomaly Details</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🚨 High Risk Orders", "⚠️ Quality Issues", "📈 Price Spikes", "⏳ Delayed Orders"])

with tab1:
    st.markdown("#### Critical Risk Orders (Risk Score ≥ 70)")
    if len(high_risk) > 0:
        display_cols = st.multiselect(
            "Select columns to display",
            high_risk.columns.tolist(),
            default=['supplier_id', 'order_id', 'risk_score', 'delay_days', 'defect_rate'],
            key="tab1"
        )
        st.dataframe(
            high_risk[display_cols].head(50).sort_values('risk_score', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("✅ No high-risk orders detected!")

with tab2:
    st.markdown("#### Quality Control Issues (Defect Rate ≥ 6%)")
    if len(high_defect) > 0:
        display_cols = st.multiselect(
            "Select columns to display",
            high_defect.columns.tolist(),
            default=['supplier_id', 'order_id', 'defect_rate', 'quantity'],
            key="tab2"
        )
        st.dataframe(
            high_defect[display_cols].head(50).sort_values('defect_rate', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("✅ All quality metrics within acceptable range!")

with tab3:
    st.markdown("#### Price Volatility Alerts (Price Change ≥ ±10%)")
    if len(price_spike) > 0:
        display_cols = st.multiselect(
            "Select columns to display",
            price_spike.columns.tolist(),
            default=['supplier_id', 'order_id', 'price_change_percent', 'unit_price'],
            key="tab3"
        )
        st.dataframe(
            price_spike[display_cols].head(50).sort_values('price_change_percent', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("✅ No significant price spikes detected!")

with tab4:
    st.markdown("#### Delivery Delays")
    if len(delayed) > 0:
        display_cols = st.multiselect(
            "Select columns to display",
            delayed.columns.tolist(),
            default=['supplier_id', 'order_id', 'delay_days', 'order_status'],
            key="tab4"
        )
        st.dataframe(
            delayed[display_cols].head(50).sort_values('delay_days', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("✅ No delayed orders!")

# Anomaly Statistics
st.markdown(f"<div class='section-header'>📉 Statistical Analysis</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Anomaly Distribution")
    anomaly_data = pd.DataFrame({
        'Anomaly Type': ['High Risk', 'Quality Issues', 'Price Spikes', 'Delayed Orders'],
        'Count': [len(high_risk), len(high_defect), len(price_spike), len(delayed)]
    })
    st.bar_chart(anomaly_data.set_index('Anomaly Type'))

with col2:
    st.markdown("#### Risk Score Distribution")
    risk_bins = pd.cut(df['risk_score'], bins=[0, 30, 50, 70, 100])
    risk_dist = risk_bins.value_counts().sort_index()
    risk_dist_data = pd.DataFrame({
        'Risk Range': ['0-30 (Low)', '30-50 (Medium)', '50-70 (High)', '70+ (Critical)'],
        'Count': [risk_dist.iloc[i] if i < len(risk_dist) else 0 for i in range(4)]
    })
    st.bar_chart(risk_dist_data.set_index('Risk Range'))
