import streamlit as st
from app.utils import load_orders
import pandas as pd

from app.theme import apply_dark_theme
apply_dark_theme()


st.set_page_config(page_title="Overview", layout="wide")

# Custom styling for dark theme
st.markdown("""
<style>
    .metric-card {
    background: linear-gradient(180deg, #0f1a2c 0%, #111c2e 100%);
    border: 1px solid #22314d;
    color: #e5e7eb;
    padding: 1.4rem;
    border-radius: 14px;
    text-align: left;
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 35px rgba(0,0,0,0.45);
}
    
    .metric-label {
    font-size: 0.9rem;
    color: #9ca3af;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}

.metric-value {
    font-size: 2.2rem;
    font-weight: 900;
    color: #ffffff;
    margin: 0;
}

    
    .status-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .status-ontime {
        background: #10b981;
        color: white;
    }
    
    .status-delayed {
        background: #ef4444;
        color: white;
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
</style>
""", unsafe_allow_html=True)

st.markdown("# 🏠 Dashboard Overview")
st.markdown("Real-time procurement analytics and performance metrics")

df = load_orders()

total_orders = len(df)
delayed_orders = int((df["order_status"] == "Delayed").sum())
ontime_orders = int((df["order_status"] == "OnTime").sum())
on_time_percentage = (ontime_orders / total_orders * 100) if total_orders > 0 else 0
delayed_percentage = (delayed_orders / total_orders * 100) if total_orders > 0 else 0

# Key Metrics with custom styling
st.markdown("### 📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📦 Total Orders</div>
        <div class="metric-value">{total_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);">
        <div class="metric-label">✅ On-Time Orders</div>
        <div class="metric-value">{ontime_orders:,}</div>
        <div class="metric-label">{on_time_percentage:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);">
        <div class="metric-label">⏳ Delayed Orders</div>
        <div class="metric-value">{delayed_orders:,}</div>
        <div class="metric-label">{delayed_percentage:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_delay = df["delay_days"].mean()
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);">
        <div class="metric-label">⏱️ Avg Delay</div>
        <div class="metric-value">{avg_delay:.1f}</div>
        <div class="metric-label">Days</div>
    </div>
    """, unsafe_allow_html=True)

# Status Distribution
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Order Status Distribution")
    status_counts = df["order_status"].value_counts()
    fig_data = pd.DataFrame({
        'Status': status_counts.index,
        'Count': status_counts.values
    })
    st.bar_chart(fig_data.set_index('Status'))

with col2:
    st.markdown("### 🎯 Priority Breakdown")
    priority_counts = df["order_priority"].value_counts()
    fig_data = pd.DataFrame({
        'Priority': priority_counts.index,
        'Count': priority_counts.values
    })
    st.bar_chart(fig_data.set_index('Priority'))

# Data Filters and Preview
st.markdown(f"<div class='section-header'>📋 Detailed Orders Data</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df["order_status"].unique()))
with col2:
    priority_filter = st.selectbox("Filter by Priority", ["All"] + sorted(df["order_priority"].unique()))
with col3:
    rows_display = st.slider("Rows to Display", 5, 100, 20, step=5)

# Apply filters
filtered_df = df.copy()
if status_filter != "All":
    filtered_df = filtered_df[filtered_df["order_status"] == status_filter]
if priority_filter != "All":
    filtered_df = filtered_df[filtered_df["order_priority"] == priority_filter]

# Display filtered data
st.info(f"Showing {len(filtered_df)} of {len(df)} orders")
st.dataframe(
    filtered_df.head(rows_display),
    use_container_width=True,
    hide_index=True
)
