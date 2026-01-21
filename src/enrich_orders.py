import pandas as pd
import numpy as np
import os

# Load old orders.csv
df = pd.read_csv("dataset/orders.csv")

# New columns options
item_categories = ["Electrical", "Mechanical", "Electronics", "Metals", "Packaging", "Chemicals"]
shipping_modes = ["Road", "Air", "Rail", "Sea"]
payment_terms_list = ["Net30", "Net45", "Net60"]
priority_list = ["Low", "Medium", "High"]
regions = ["North", "South", "East", "West"]

np.random.seed(42)

# Add new columns
df["item_category"] = np.random.choice(item_categories, size=len(df))
df["shipping_mode"] = np.random.choice(shipping_modes, size=len(df))
df["payment_terms"] = np.random.choice(payment_terms_list, size=len(df))
df["order_priority"] = np.random.choice(priority_list, size=len(df))
df["region"] = np.random.choice(regions, size=len(df))

# Price change % (simulate market fluctuations)
# delayed suppliers tend to have higher price changes (realistic effect)
df["price_change_percent"] = np.where(
    df["order_status"] == "Delayed",
    np.round(np.random.uniform(3, 15, size=len(df)), 2),
    np.round(np.random.uniform(-2, 8, size=len(df)), 2)
)

# Save upgraded orders.csv
os.makedirs("dataset", exist_ok=True)
df.to_csv("dataset/orders.csv", index=False)

print("✅ orders.csv upgraded successfully with new industry-level columns!")
print("New shape:", df.shape)
print(df.head())
