import pandas as pd
import os

df = pd.read_csv("src/orders.csv")

# Simple risk score (0 to 100)
df["risk_score"] = (df["delay_days"] * 20) + (df["defect_rate"] * 100 * 2)
df["risk_score"] = df["risk_score"].clip(0, 100)

# Supplier-wise average risk
supplier_risk = df.groupby("supplier_id")["risk_score"].mean().reset_index()
supplier_risk = supplier_risk.sort_values("risk_score", ascending=False)

print("\n📌 Supplier Risk Ranking:\n")
print(supplier_risk)

# Save report
os.makedirs("dataset", exist_ok=True)
supplier_risk.to_csv("dataset/supplier_risk_report.csv", index=False)
print("\n✅ Saved: dataset/supplier_risk_report.csv")
