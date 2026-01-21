import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Load dataset
df = pd.read_csv("src/orders.csv")

# Convert order_status to binary
df["target_delay"] = df["order_status"].map({"OnTime": 0, "Delayed": 1})

# Features and Target
X = df[["quantity", "unit_price", "defect_rate", "delay_days"]]
y = df["target_delay"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📌 Classification Report:\n", classification_report(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.pkl")
print("\n✅ Model saved: models/model.pkl")
