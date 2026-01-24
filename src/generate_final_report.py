import pandas as pd
import os
from datetime import datetime

def safe_read_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

def main():
    orders = safe_read_csv("dataset/orders.csv")
    suppliers = safe_read_csv("dataset/suppliers.csv")
    risk_report = safe_read_csv("dataset/supplier_risk_report.csv")
    anomalies = safe_read_csv("dataset/anomaly_report.csv")
    clusters = safe_read_csv("dataset/supplier_clusters.csv")

    if orders is None:
        raise FileNotFoundError("dataset/orders.csv not found. Cannot generate report.")

    # ----------------------------
    # 1) Procurement KPIs
    # ----------------------------
    total_orders = len(orders)
    delayed_orders = int((orders["order_status"] == "Delayed").sum()) if "order_status" in orders.columns else 0
    ontime_orders = int((orders["order_status"] == "OnTime").sum()) if "order_status" in orders.columns else 0

    avg_delay = float(orders["delay_days"].mean()) if "delay_days" in orders.columns else 0.0
    avg_defect = float(orders["defect_rate"].mean()) if "defect_rate" in orders.columns else 0.0
    avg_price_change = float(orders["price_change_percent"].mean()) if "price_change_percent" in orders.columns else 0.0

    on_time_rate = (ontime_orders / total_orders) * 100 if total_orders > 0 else 0

    # ----------------------------
    # 2) Supplier KPIs
    # ----------------------------
    total_suppliers = orders["supplier_id"].nunique() if "supplier_id" in orders.columns else 0

    # Top risky suppliers (from risk report if available)
    top_risky = []
    top_recommended = []
    if risk_report is not None and "risk_score" in risk_report.columns:
        top_risky = risk_report.sort_values("risk_score", ascending=False).head(3)["supplier_id"].astype(str).tolist()
        top_recommended = risk_report.sort_values("risk_score", ascending=True).head(3)["supplier_id"].astype(str).tolist()

    # Anomaly count
    anomaly_count = 0
    if anomalies is not None:
        anomaly_count = len(anomalies)

    # Cluster breakdown
    cluster_summary = {}
    if clusters is not None and "supplier_segment" in clusters.columns:
        cluster_summary = clusters["supplier_segment"].value_counts().to_dict()

    # ----------------------------
    # 3) Build Final Summary Report (1-row table)
    # ----------------------------
    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_orders": total_orders,
        "delayed_orders": delayed_orders,
        "ontime_orders": ontime_orders,
        "on_time_rate_percent": round(on_time_rate, 2),
        "avg_delay_days": round(avg_delay, 2),
        "avg_defect_rate": round(avg_defect, 4),
        "avg_price_change_percent": round(avg_price_change, 2),
        "total_suppliers": total_suppliers,
        "anomaly_records": anomaly_count,
        "top_3_risky_suppliers": ", ".join(top_risky) if top_risky else "N/A",
        "top_3_recommended_suppliers": ", ".join(top_recommended) if top_recommended else "N/A",
        "cluster_breakdown": str(cluster_summary) if cluster_summary else "N/A"
    }

    os.makedirs("reports", exist_ok=True)
    final_path = "reports/final_procurement_summary.csv"
    pd.DataFrame([report]).to_csv(final_path, index=False)

    print("✅ Final Procurement Summary Generated!")
    print(f"Saved: {final_path}")

if __name__ == "__main__":
    main()
