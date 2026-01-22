import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


# -----------------------------
# 1) Load dataset
# -----------------------------
df = pd.read_csv("dataset/orders.csv")

# Target column (convert to binary)
# Delayed = 1, OnTime = 0
df["target"] = df["order_status"].apply(lambda x: 1 if x == "Delayed" else 0)

# -----------------------------
# 2) Select Features
# -----------------------------
features = [
    "quantity",
    "unit_price",
    "defect_rate",
    "delay_days",  # keep for now (later we improve further)
    "item_category",
    "shipping_mode",
    "payment_terms",
    "order_priority",
    "region",
    "price_change_percent"
]

X = df[features]
y = df["target"]

# Identify categorical and numeric columns
categorical_cols = ["item_category", "shipping_mode", "payment_terms", "order_priority", "region"]
numeric_cols = [col for col in features if col not in categorical_cols]

# Preprocessing: OneHotEncode categorical + pass numeric as is
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numeric_cols)
    ]
)

# -----------------------------
# 3) Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# 4) Models to compare
# -----------------------------
models = {
    "LogisticRegression": LogisticRegression(max_iter=2000),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42)
}

results = []

best_model_name = None
best_f1 = -1
best_pipeline = None

# -----------------------------
# 5) Train + Evaluate each model
# -----------------------------
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

# -----------------------------
# 6) Save report
# -----------------------------
os.makedirs("reports", exist_ok=True)
results_df = pd.DataFrame(results).sort_values("f1_score", ascending=False)
results_df.to_csv("reports/model_comparison.csv", index=False)

print("\n✅ Model Comparison Report Saved: reports/model_comparison.csv")
print(results_df)

# -----------------------------
# 7) Save best model
# -----------------------------
os.makedirs("models", exist_ok=True)
joblib.dump(best_pipeline, "models/model.pkl")

print(f"\n🏆 Best Model Saved: {best_model_name} → models/model.pkl")
