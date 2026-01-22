import pandas as pd
import numpy as np
import os

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# -----------------------------
# 1) Load orders dataset
# -----------------------------
df = pd.read_csv("dataset/orders.csv")

# -----------------------------
# 2) Create supplier-level features
# -----------------------------
supplier_features = df.groupby("supplier_id").agg(
    avg_delay_days=("delay_days", "mean"),
    avg_defect_rate=("defect_rate", "mean"),
    avg_price_change=("price_change_percent", "mean"),
    on_time_rate=("order_status", lambda x: (x == "OnTime").mean()),
    total_orders=("order_id", "count")
).reset_index()

# -----------------------------
# 3) Prepare data for clustering
# -----------------------------
X = supplier_features[[
    "avg_delay_days",
    "avg_defect_rate",
    "avg_price_change",
    "on_time_rate"
]]

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# 4) KMeans clustering
# -----------------------------
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
supplier_features["cluster"] = kmeans.fit_predict(X_scaled)

# -----------------------------
# 5) Convert clusters into labels (Reliable/Moderate/Risky)
# -----------------------------
# We decide label based on avg_delay_days (higher delay = more risky)
cluster_delay_mean = supplier_features.groupby("cluster")["avg_delay_days"].mean().sort_values()

cluster_labels = {}
cluster_labels[cluster_delay_mean.index[0]] = "Reliable ✅"
cluster_labels[cluster_delay_mean.index[1]] = "Moderate ⚠️"
cluster_labels[cluster_delay_mean.index[2]] = "Risky 🚨"

supplier_features["supplier_segment"] = supplier_features["cluster"].map(cluster_labels)

# -----------------------------
# 6) Save output
# -----------------------------
os.makedirs("dataset", exist_ok=True)
supplier_features.to_csv("dataset/supplier_clusters.csv", index=False)

print("✅ Supplier clustering completed!")
print("Saved: dataset/supplier_clusters.csv")
print(supplier_features.head())
