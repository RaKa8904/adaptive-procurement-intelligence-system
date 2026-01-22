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

st.subheader("📌 Model Performance Comparison")
model_report = pd.read_csv("reports/model_comparison.csv")
st.dataframe(model_report)

# -------------------- SECTION 4: PREDICTION MODULE --------------------
st.subheader("🤖 Predict Delay for a New Order")

quantity = st.number_input("Enter Quantity", min_value=1, value=100)
unit_price = st.number_input("Enter Unit Price", min_value=1, value=100)
defect_rate = st.number_input("Enter Defect Rate (0.00 to 0.10)", min_value=0.0, max_value=1.0, value=0.03)
delay_days = st.number_input("Enter Delay Days (0 if new order)", min_value=0, value=0)

if st.button("Predict Delivery Status"):
    input_data = pd.DataFrame([[quantity, unit_price, defect_rate, delay_days]],
                              columns=["quantity", "unit_price", "defect_rate", "delay_days"])

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("🚨 Prediction: DELAYED Order (Risky Supplier/Order)")
    else:
        st.success("✅ Prediction: ON TIME Order (Safe Supplier/Order)")
