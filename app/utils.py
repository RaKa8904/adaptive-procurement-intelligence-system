import pandas as pd
import joblib

def load_orders():
    return pd.read_csv("dataset/orders.csv")

def load_suppliers():
    return pd.read_csv("dataset/suppliers.csv")

def load_risk_report():
    return pd.read_csv("dataset/supplier_risk_report.csv")

def load_clusters():
    return pd.read_csv("dataset/supplier_clusters.csv")

def load_anomalies():
    return pd.read_csv("dataset/anomaly_report.csv")

def load_model():
    return joblib.load("models/model.pkl")
