import os
import pandas as pd
from datetime import datetime


def retrain_risk_model():
    # Load data
    orders = pd.read_csv("dataset/orders.csv")

    # Basic supplier performance metrics
    supplier_stats = orders.groupby("supplier_id").agg(
        total_orders=("order_id", "count"),
        avg_defect_rate=("defect_rate", "mean"),
        avg_delay_days=("delay_days", "mean"),
        on_time_rate=("order_status", lambda x: (x == "OnTime").mean())
    ).reset_index()

    # -----------------------------
    # Risk Score Calculation (0-100)
    # -----------------------------
    # Higher delay + higher defects + lower on-time => higher risk

    supplier_stats["risk_score"] = (
        (supplier_stats["avg_defect_rate"] * 400) +
        (supplier_stats["avg_delay_days"] * 3) +
        ((1 - supplier_stats["on_time_rate"]) * 50)
    )

    # Clamp risk_score between 0 and 100
    supplier_stats["risk_score"] = supplier_stats["risk_score"].clip(0, 100).round(2)

    # Add risk category
    def risk_category(score):
        if score >= 70:
            return "High"
        elif score >= 40:
            return "Medium"
        return "Low"

    supplier_stats["risk_category"] = supplier_stats["risk_score"].apply(risk_category)

    # Save report
    os.makedirs("dataset", exist_ok=True)
    out_path = "dataset/supplier_risk_report.csv"
    supplier_stats.to_csv(out_path, index=False)

    # -----------------------------
    # Logging
    # -----------------------------
    os.makedirs("logs", exist_ok=True)
    log_path = "logs/risk_training_log.csv"

    log_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_suppliers": len(supplier_stats),
        "avg_risk_score": round(float(supplier_stats["risk_score"].mean()), 2),
        "status": "SUCCESS"
    }

    if os.path.exists(log_path):
        old = pd.read_csv(log_path)
        new = pd.concat([old, pd.DataFrame([log_row])], ignore_index=True)
    else:
        new = pd.DataFrame([log_row])

    new.to_csv(log_path, index=False)

    print(f"✅ Risk scoring report updated: {out_path}")
    print(f"📝 Risk log updated: {log_path}")


if __name__ == "__main__":
    retrain_risk_model()
