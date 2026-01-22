import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="APIS Dashboard", layout="wide")

st.title("📦 Adaptive Procurement Intelligence System (APIS)")
st.write("This dashboard shows supplier performance, risk scoring and delay prediction using ML.")

# Load dataset
df = pd.read_csv("dataset/orders.csv")

# Supplier Master Data
suppliers = pd.read_csv("dataset/suppliers.csv")
st.subheader("🏢 Supplier Master Data")
st.dataframe(suppliers)

# Load supplier risk report
risk_report = pd.read_csv("dataset/supplier_risk_report.csv")

# Load trained model
model = joblib.load("models/model.pkl")
# -------------------- SECTION 1: DATA PREVIEW --------------------
st.subheader("📄 Orders Dataset Preview")
st.dataframe(df.head(15))

# -------------------- SECTION 2: SUPPLIER RISK RANKING --------------------
st.subheader("⚠ Supplier Risk Ranking (Higher = More Risk)")
st.dataframe(risk_report)

# -------------------- SECTION 3: BASIC ANALYTICS --------------------
st.subheader("📊 Procurement Analytics")

col1, col2 = st.columns(2)

with col1:
    status_count = df["order_status"].value_counts()
    st.bar_chart(status_count)

with col2:
    st.write("📌 Average Delay Days per Supplier")
    avg_delay = df.groupby("supplier_id")["delay_days"].mean()
    st.bar_chart(avg_delay)

# -------------------- SECTION 4: Anomaly_Detection MODULE --------------------
st.subheader("🚨 Anomaly Alerts (Unusual Orders)")
anomaly_report = pd.read_csv("dataset/anomaly_report.csv")

if anomaly_report.empty:
    st.success("No anomalies detected ✅")
else:
    st.warning(f"Anomalies detected: {len(anomaly_report)} 🚨")
    st.dataframe(anomaly_report.head(20))

st.subheader("📌 Model Performance Comparison")
model_report = pd.read_csv("reports/model_comparison.csv")
st.dataframe(model_report)

# -------------------- SECTION 5: PREDICTION MODULE --------------------
st.subheader("🤖 Predict Delay for a New Order (Using Supplier History)")

# Load orders dataset to compute supplier history
orders_df = pd.read_csv("dataset/orders.csv")

# Supplier dropdown
supplier_id = st.selectbox("Select Supplier ID", sorted(orders_df["supplier_id"].unique()))

# Compute supplier history stats
supplier_orders = orders_df[orders_df["supplier_id"] == supplier_id]

supplier_avg_delay_days = supplier_orders["delay_days"].mean()
supplier_avg_defect_rate = supplier_orders["defect_rate"].mean()
supplier_on_time_rate = (supplier_orders["order_status"] == "OnTime").mean()

st.info(
    f"📌 Supplier History → Avg Delay: {supplier_avg_delay_days:.2f} days | "
    f"Avg Defect Rate: {supplier_avg_defect_rate:.3f} | "
    f"On-Time Rate: {supplier_on_time_rate:.2%}"
)

# User inputs for new order
quantity = st.number_input("Enter Quantity", min_value=1, value=100)
unit_price = st.number_input("Enter Unit Price", min_value=1.0, value=100.0)
defect_rate = st.number_input("Enter Defect Rate", min_value=0.0, max_value=1.0, value=0.02)

item_category = st.selectbox("Select Item Category", ["Electrical", "Mechanical", "Electronics", "Metals", "Packaging", "Chemicals"])
shipping_mode = st.selectbox("Select Shipping Mode", ["Road", "Air", "Rail", "Sea"])
payment_terms = st.selectbox("Select Payment Terms", ["Net30", "Net45", "Net60"])
order_priority = st.selectbox("Select Order Priority", ["Low", "Medium", "High"])
region = st.selectbox("Select Region", ["North", "South", "East", "West"])
price_change_percent = st.number_input("Enter Price Change %", value=2.5)

# Create input dataframe with EXACT columns used in training
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

if st.button("Predict Delay"):
    prediction = model.predict(input_data)[0]
    result = "Delayed 🚨" if prediction == 1 else "OnTime ✅"
    st.success(f"Prediction Result: {result}")

