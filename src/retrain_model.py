import pandas as pd
import os
import joblib
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def train_and_save_model():
    df = pd.read_csv("dataset/orders.csv")

    # Target: Delayed=1, OnTime=0
    df["target"] = df["order_status"].apply(lambda x: 1 if x == "Delayed" else 0)

    # Supplier history features
    supplier_stats = df.groupby("supplier_id").agg(
        supplier_avg_delay_days=("delay_days", "mean"),
        supplier_avg_defect_rate=("defect_rate", "mean"),
        supplier_on_time_rate=("order_status", lambda x: (x == "OnTime").mean())
    ).reset_index()

    df = df.merge(supplier_stats, on="supplier_id", how="left")

    features = [
        "quantity",
        "unit_price",
        "defect_rate",
        "item_category",
        "shipping_mode",
        "payment_terms",
        "order_priority",
        "region",
        "price_change_percent",
        "supplier_avg_delay_days",
        "supplier_avg_defect_rate",
        "supplier_on_time_rate"
    ]

    X = df[features]
    y = df["target"]

    categorical_cols = ["item_category", "shipping_mode", "payment_terms", "order_priority", "region"]
    numeric_cols = [c for c in features if c not in categorical_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", "passthrough", numeric_cols)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "LogisticRegression": LogisticRegression(max_iter=2000),
        "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42)
    }

    best_model_name = None
    best_f1 = -1
    best_pipeline = None
    results = []

    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ("preprocess", preprocessor),
            ("model", model)
        ])

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        results.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": name,
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4)
        })

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipeline = pipeline

    # Save best model
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_pipeline, "models/model.pkl")

    # Save model comparison report
    os.makedirs("reports", exist_ok=True)
    pd.DataFrame(results).sort_values("f1_score", ascending=False).to_csv(
        "reports/model_comparison.csv", index=False
    )

    # Save training logs (append mode)
    os.makedirs("logs", exist_ok=True)
    log_path = "logs/training_log.csv"
    log_df = pd.DataFrame(results)

    if os.path.exists(log_path):
        old = pd.read_csv(log_path)
        log_df = pd.concat([old, log_df], ignore_index=True)

    log_df.to_csv(log_path, index=False)

    return best_model_name, best_f1


if __name__ == "__main__":
    model_name, f1 = train_and_save_model()
    print(f"✅ Retraining done! Best Model: {model_name} | Best F1: {f1:.4f}")
