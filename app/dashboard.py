import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="APIS Dashboard", layout="wide")

st.title("📦 Adaptive Procurement Intelligence System (APIS)")
st.write("This dashboard shows supplier performance, risk scoring and delay prediction using ML.")

# Load dataset
df = pd.read_csv("dataset/orders.csv")

# ✅ Creating risk_score(for Alerts Panel)
if "risk_score" not in df.columns:
    priority_weight = {"Low": 5, "Medium": 10, "High": 20}
    df["priority_weight"] = df["order_priority"].map(priority_weight).fillna(10)

    df["risk_score"] = (
        (df["delay_days"] * 18) +
        (df["defect_rate"] * 100 * 2.5) +
        (df["price_change_percent"].abs() * 1.2) +
        (df["priority_weight"] * 0.6)
    ).clip(0, 100)

#alerts panel
st.subheader("🚨 Alerts Panel (Procurement Monitoring)")

# Basic alerts from orders dataset
high_risk_orders = df[df["risk_score"] >= 70]
high_defect_orders = df[df["defect_rate"] >= 0.06]
price_spike_orders = df[df["price_change_percent"].abs() >= 10]
delayed_orders = df[df["order_status"] == "Delayed"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("High Risk Orders", len(high_risk_orders))
with col2:
    st.metric("High Defect Orders", len(high_defect_orders))
with col3:
    st.metric("Price Spike Orders", len(price_spike_orders))
with col4:
    st.metric("Delayed Orders", len(delayed_orders))

# Show details
with st.expander("🔍 View Alert Details"):
    st.write("🚨 High Risk Orders (risk_score >= 70)")
    st.dataframe(high_risk_orders.head(15))

    st.write("⚠️ High Defect Orders (defect_rate >= 0.06)")
    st.dataframe(high_defect_orders.head(15))

    st.write("📈 Price Spike Orders (|price_change_percent| >= 10)")
    st.dataframe(price_spike_orders.head(15))

    st.write("⏳ Delayed Orders")
    st.dataframe(delayed_orders.head(15))

# Recommended Suppliers
st.subheader("🏆 Recommended Suppliers (Top 3)")

risk_report = pd.read_csv("dataset/supplier_risk_report.csv")

top_suppliers = risk_report.sort_values("risk_score", ascending=True).head(3)

st.success("These suppliers have the lowest risk score (recommended for new orders).")
st.dataframe(top_suppliers)

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

# -------------------- SECTION 3: Supplier Segmentation MODULE --------------------
st.subheader("🧩 Supplier Segmentation (Clustering)")

clusters = pd.read_csv("dataset/supplier_clusters.csv")
st.dataframe(clusters)

st.info("Suppliers are automatically grouped into Reliable / Moderate / Risky segments using K-Means clustering.")

# -------------------- SECTION 4: BASIC ANALYTICS --------------------
st.subheader("📊 Procurement Analytics")

col1, col2 = st.columns(2)

with col1:
    status_count = df["order_status"].value_counts()
    st.bar_chart(status_count)

with col2:
    st.write("📌 Average Delay Days per Supplier")
    avg_delay = df.groupby("supplier_id")["delay_days"].mean()
    st.bar_chart(avg_delay)

# -------------------- SECTION 5: Anomaly_Detection MODULE --------------------
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

# -------------------- SECTION 6: Supplier Segmentation MODULE --------------------
st.subheader("🧩 Supplier Segmentation (Clustering)")

clusters = pd.read_csv("dataset/supplier_clusters.csv")
st.dataframe(clusters)

st.info("Suppliers are automatically grouped into Reliable / Moderate / Risky segments using K-Means clustering.")

# -------------------- SECTION 7: Download Buttons MODULE --------------------
st.subheader("📥 Download Reports")
# Supplier Risk Report Download
with open("dataset/supplier_risk_report.csv", "rb") as f:
    st.download_button(
        label="⬇️ Download Supplier Risk Report",
        data=f,
        file_name="supplier_risk_report.csv",
        mime="text/csv"
    )
# Anomaly Report Download (if exists)
try:
    with open("dataset/anomaly_report.csv", "rb") as f:
        st.download_button(
            label="⬇️ Download Anomaly Report",
            data=f,
            file_name="anomaly_report.csv",
            mime="text/csv"
        )
except:
    st.info("Anomaly report not found (run Phase 3 script if needed).")
# Supplier Clusters Download (if exists)
try:
    with open("dataset/supplier_clusters.csv", "rb") as f:
        st.download_button(
            label="⬇️ Download Supplier Clustering Report",
            data=f,
            file_name="supplier_clusters.csv",
            mime="text/csv"
        )
except:
    st.info("Supplier clustering report not found (run Phase 4 script if needed).")

# -------------------- SECTION 7: PREDICTION MODULE --------------------
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

