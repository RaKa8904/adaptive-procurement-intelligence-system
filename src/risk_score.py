import pandas as pd
import os

df = pd.read_csv("dataset/orders.csv")

# Convert priority into numeric weight
priority_weight = {"Low": 5, "Medium": 10, "High": 20}
df["priority_weight"] = df["order_priority"].map(priority_weight)

# Risk score formula (improved)
# Delay + defects + price spikes + priority
df["risk_score"] = (
    (df["delay_days"] * 18) +
    (df["defect_rate"] * 100 * 2.5) +
    (df["price_change_percent"].abs() * 1.2) +
    (df["priority_weight"] * 0.6)
)

# Clip between 0 and 100
df["risk_score"] = df["risk_score"].clip(0, 100)

# Supplier-wise risk report
supplier_risk = df.groupby("supplier_id")["risk_score"].mean().reset_index()
supplier_risk = supplier_risk.sort_values("risk_score", ascending=False)

print("\n📌 Supplier Risk Ranking:\n")
print(supplier_risk)

# Save report
os.makedirs("dataset", exist_ok=True)
supplier_risk.to_csv("dataset/supplier_risk_report.csv", index=False)
print("\n✅ Saved: dataset/supplier_risk_report.csv")
