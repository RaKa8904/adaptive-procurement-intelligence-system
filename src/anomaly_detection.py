import pandas as pd
import numpy as np
import os

from sklearn.ensemble import IsolationForest

# -----------------------------
# 1) Load dataset
# -----------------------------
df = pd.read_csv("dataset/orders.csv")

# -----------------------------
# 2) Select numeric features for anomaly detection
# -----------------------------
features = ["delay_days", "defect_rate", "price_change_percent", "unit_price", "quantity"]

X = df[features].copy()

# Fill missing values (safety)
X = X.fillna(0)

# -----------------------------
# 3) Train Isolation Forest
# -----------------------------
# contamination = approx % of anomalies expected
model = IsolationForest(
    n_estimators=200,
    contamination=0.08,   # 8% anomalies (you can change to 0.05 or 0.10)
    random_state=42
)

model.fit(X)

# Predict anomalies: -1 = anomaly, 1 = normal
df["anomaly_flag"] = model.predict(X)
df["anomaly_flag"] = df["anomaly_flag"].apply(lambda x: 1 if x == -1 else 0)

# Anomaly score (lower = more anomalous)
df["anomaly_score"] = model.decision_function(X)
df["anomaly_score"] = df["anomaly_score"].round(4)

# -----------------------------
# 4) Create anomaly report
# -----------------------------
anomalies = df[df["anomaly_flag"] == 1].copy()

# Sort most suspicious first
anomalies = anomalies.sort_values("anomaly_score")

# Save report
os.makedirs("dataset", exist_ok=True)
anomalies.to_csv("dataset/anomaly_report.csv", index=False)

print("✅ Anomaly Detection Completed!")
print(f"Total Orders: {len(df)}")
print(f"Anomalies Found: {len(anomalies)}")
print("Saved: dataset/anomaly_report.csv")
