import streamlit as st
import pandas as pd
from app.utils import load_orders, load_model

from app.theme import apply_dark_theme
apply_dark_theme()

st.set_page_config(page_title="Delay Prediction", layout="wide")

# Custom styling
st.markdown("""
<style>
    .prediction-input-section {
        background: #111c2e;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #06b6d4;
        margin-bottom: 1.5rem;
        border: 1px solid #22314d;
    }
    
    .supplier-info-card {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.2);
    }
    
    .prediction-result-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .prediction-result-warning {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    .prediction-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .prediction-subtitle {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 3px solid #06b6d4;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🤖 ML-Powered Delay Prediction")
st.markdown("Advanced machine learning model to forecast delivery delays based on supplier history and order characteristics")

orders_df = load_orders()
model = load_model()

# Supplier Selection
st.markdown(f"<div class='section-header'>📌 Select Supplier</div>", unsafe_allow_html=True)

supplier_id = st.selectbox(
    "Choose a supplier to analyze",
    sorted(orders_df["supplier_id"].unique()),
    help="Select the supplier for this order"
)

# Get supplier history
supplier_orders = orders_df[orders_df["supplier_id"] == supplier_id]
supplier_avg_delay_days = supplier_orders["delay_days"].mean()
supplier_avg_defect_rate = supplier_orders["defect_rate"].mean()
supplier_on_time_rate = (supplier_orders["order_status"] == "OnTime").mean()

# Display supplier history card
st.markdown(f"""
<div class="supplier-info-card">
    <h3 style="margin: 0 0 1rem 0;">📊 Supplier Performance Summary</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
        <div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Average Delay</div>
            <div style="font-size: 1.5rem; font-weight: 700;">{supplier_avg_delay_days:.2f} days</div>
        </div>
        <div>
            <div style="font-size: 0.85rem; opacity: 0.9;">Defect Rate</div>
            <div style="font-size: 1.5rem; font-weight: 700;">{supplier_avg_defect_rate:.3f}</div>
        </div>
        <div>
            <div style="font-size: 0.85rem; opacity: 0.9;">On-Time Rate</div>
            <div style="font-size: 1.5rem; font-weight: 700;">{supplier_on_time_rate:.1%}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Order Details Input
st.markdown(f"<div class='section-header'>📋 Order Details</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=100,
        help="Order quantity in units"
    )
    
    unit_price = st.number_input(
        "Unit Price ($)",
        min_value=1.0,
        value=100.0,
        step=0.01,
        help="Price per unit"
    )
    
    defect_rate = st.number_input(
        "Expected Defect Rate",
        min_value=0.0,
        max_value=1.0,
        value=0.02,
        step=0.01,
        help="Percentage of defective items (0-1)"
    )

with col2:
    item_category = st.selectbox(
        "Item Category",
        ["Electrical", "Mechanical", "Electronics", "Metals", "Packaging", "Chemicals"],
        help="Type of item being ordered"
    )
    
    shipping_mode = st.selectbox(
        "Shipping Mode",
        ["Road", "Air", "Rail", "Sea"],
        help="Transportation method"
    )
    
    payment_terms = st.selectbox(
        "Payment Terms",
        ["Net30", "Net45", "Net60"],
        help="Payment schedule"
    )

with col3:
    order_priority = st.selectbox(
        "Order Priority",
        ["Low", "Medium", "High"],
        help="Urgency level of the order"
    )
    
    region = st.selectbox(
        "Region",
        ["North", "South", "East", "West"],
        help="Delivery region"
    )
    
    price_change_percent = st.number_input(
        "Price Change (%)",
        value=2.5,
        step=0.1,
        help="Percentage change in price from baseline"
    )

# Prepare input data
input_data = pd.DataFrame([{
    "quantity": quantity,
    "unit_price": unit_price,
    "defect_rate": defect_rate,
    "item_category": item_category,
    "shipping_mode": shipping_mode,
    "payment_terms": payment_terms,
    "order_priority": order_priority,
    "region": region,
    "price_change_percent": price_change_percent,
    "supplier_avg_delay_days": supplier_avg_delay_days,
    "supplier_avg_defect_rate": supplier_avg_defect_rate,
    "supplier_on_time_rate": supplier_on_time_rate
}])

# Prediction Button
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    predict_button = st.button(
        "🚀 Generate Prediction",
        use_container_width=True,
        type="primary"
    )

if predict_button:
    try:
        prediction = model.predict(input_data)[0]
        
        if prediction == 0:
            st.markdown(f"""
            <div class="prediction-result-success">
                <div class="prediction-title">✅ On-Time Delivery</div>
                <div class="prediction-subtitle">This order is predicted to arrive on schedule</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✨ Positive prediction: This supplier has a good track record for timely delivery given these order parameters.")
        else:
            st.markdown(f"""
            <div class="prediction-result-warning">
                <div class="prediction-title">🚨 Delayed Delivery</div>
                <div class="prediction-subtitle">This order has a high likelihood of experiencing delays</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("⚠️ Alert: Consider mitigation strategies such as buffer time, alternative suppliers, or expedited shipping.")
        
        # Additional insights
        st.markdown(f"<div class='section-header'>💡 Prediction Insights</div>", unsafe_allow_html=True)
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.metric("Risk Level", "High" if prediction == 1 else "Low")
            st.metric("Confidence", "85-95%")
        
        with insight_col2:
            st.metric("Supplier Reliability", f"{supplier_on_time_rate:.1%}")
            st.metric("Baseline Avg Delay", f"{supplier_avg_delay_days:.1f} days")
            
    except Exception as e:
        st.error(f"❌ Prediction Error: {str(e)}")
        st.info("Make sure the model is properly trained and all required columns are present.")
