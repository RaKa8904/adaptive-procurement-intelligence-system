import streamlit as st
from app.utils import load_orders
import pandas as pd

from app.theme import apply_dark_theme
apply_dark_theme()

st.set_page_config(page_title="Orders Explorer", layout="wide")

# Custom styling
st.markdown("""
<style>
    .filter-container {
        background: #111c2e;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #06b6d4;
        margin-bottom: 1.5rem;
        border: 1px solid #22314d;
    }
    
    .order-count {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 1rem 0;
        border-bottom: 3px solid #06b6d4;
        padding-bottom: 0.5rem;
    }
    
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📦 Orders Explorer")
st.markdown("Advanced filtering and analysis of all orders in the system")

df = load_orders()

# Enhanced Filter Section
st.markdown("## 🔍 Advanced Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    supplier_filter = st.selectbox(
        "Supplier ID",
        ["All"] + sorted(df["supplier_id"].unique()),
        help="Select specific supplier or view all"
    )

with col2:
    status_filter = st.selectbox(
        "Order Status",
        ["All", "OnTime", "Delayed"],
        help="Filter by delivery status"
    )

with col3:
    priority_filter = st.selectbox(
        "Priority Level",
        ["All"] + sorted(df["order_priority"].unique()),
        help="Filter by order priority"
    )

with col4:
    rows_to_show = st.slider(
        "Results per page",
        5, 100, 50, step=5,
        help="Number of orders to display"
    )

# Apply filters
filtered = df.copy()

if supplier_filter != "All":
    filtered = filtered[filtered["supplier_id"] == supplier_filter]

if status_filter != "All":
    filtered = filtered[filtered["order_status"] == status_filter]

if priority_filter != "All":
    filtered = filtered[filtered["order_priority"] == priority_filter]

# Display count
st.markdown(f'<div class="order-count">📊 Showing {len(filtered):,} orders (filtered from {len(df):,} total)</div>', unsafe_allow_html=True)

# Summary stats for filtered data
col1, col2, col3, col4 = st.columns(4)

with col1:
    on_time_count = (filtered["order_status"] == "OnTime").sum()
    st.metric("✅ On-Time", f"{on_time_count:,}")

with col2:
    delayed_count = (filtered["order_status"] == "Delayed").sum()
    st.metric("⏳ Delayed", f"{delayed_count:,}")

with col3:
    avg_delay = filtered["delay_days"].mean()
    st.metric("⏱️ Avg Delay (days)", f"{avg_delay:.1f}")

with col4:
    avg_defect = filtered["defect_rate"].mean()
    st.metric("🔧 Avg Defect Rate", f"{avg_defect:.3f}")

# Sortable data display
st.markdown(f"<div class='section-header'>📋 Orders Data</div>", unsafe_allow_html=True)

sort_by = st.selectbox(
    "Sort by",
    ["delay_days", "defect_rate", "quantity", "unit_price"],
    format_func=lambda x: {"delay_days": "Delay Days", "defect_rate": "Defect Rate", "quantity": "Quantity", "unit_price": "Unit Price"}.get(x, x)
)

sort_order = st.radio("Sort order", ["Ascending", "Descending"], horizontal=True)
ascending = sort_order == "Ascending"

filtered_sorted = filtered.sort_values(by=sort_by, ascending=ascending)

st.dataframe(
    filtered_sorted.head(rows_to_show),
    use_container_width=True,
    hide_index=True
)
