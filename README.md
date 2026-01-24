🚀 Adaptive Procurement Intelligence System (APIS)

An AI-powered procurement intelligence platform that helps organizations monitor procurement performance, evaluate supplier reliability, detect anomalies, and predict delivery delays using Machine Learning + Analytics.

APIS is built as a multi-page Streamlit dashboard with automated risk scoring, supplier segmentation, anomaly detection, reporting, and model retraining.

📌 Problem Statement

In real-world procurement operations, organizations face challenges such as:

Late deliveries impacting production timelines

Quality issues (high defect rates) increasing costs

Price fluctuations affecting budgeting

Difficulty identifying risky suppliers early

Manual monitoring & lack of intelligent decision support

Traditional procurement systems are reactive.
✅ APIS makes procurement proactive using AI-driven risk intelligence.

🎯 Project Objectives

✔ Monitor procurement order performance in real-time
✔ Score supplier risk from delivery + quality + pricing patterns
✔ Predict order delay probability using supplier history + order parameters
✔ Detect anomalies/outliers automatically (risk, defects, price spikes)
✔ Segment suppliers into reliability groups using clustering
✔ Provide downloadable reports & analytics dashboards
✔ Support adaptive learning through model retraining & training logs

✨ Final Phase Upgrades (All-in-One)

This final version of APIS includes the following major upgrades:

✅ 1) Multi-Page Streamlit Dashboard (Full Navigation)

APIS is now a complete dashboard suite, not just a single page.

Modules included:

🏠 Main Dashboard Home

📊 Overview Analytics

📦 Orders Explorer

🏢 Supplier Intelligence

🧩 Supplier Segmentation (Clustering)

🚨 Alerts & Anomalies

🤖 Delay Predictor (ML)

📄 Reports & Downloads

🔁 Retrain & Logs

Dashboard entry page: \_🏠_Dashboard.py

\_🏠_Dashboard

✅ 2) Modern Dark Mode UI Theme (Professional Look)

A custom dark theme UI is applied across all pages for:

Better readability

High contrast text

Consistent UI styling

Modern enterprise dashboard feel

Theme is applied using: apply_dark_theme() from theme.py

theme

✅ 3) Supplier Risk Scoring + Ranking System

Suppliers are evaluated using risk scores and categorized into:

🟢 Low Risk

🟠 Medium Risk

🔴 High Risk

The Suppliers module shows:

risk distribution

risk ranking table

progress-style risk bars

Supplier page: 3_🏢_Suppliers.py

3_🏢_Suppliers

✅ 4) Orders Explorer with Advanced Filtering

A full orders explorer is added to filter and analyze orders by:

supplier

order status (OnTime / Delayed)

priority (Low / Medium / High)

sorting by delay, defect rate, quantity, price

Orders Explorer page: 2_📦_Orders_Explorer.py

2_📦_Orders_Explorer

✅ 5) Supplier Segmentation using K-Means Clustering

Suppliers are segmented into strategic categories:

🟢 Reliable

🟠 Moderate

🔴 Risky

This helps procurement teams with:

supplier strategy planning

vendor relationship management

risk mitigation

Clustering page: 4_🧩_Supplier Segmentation.py

4_🧩_Supplier Segmentation

✅ 6) Alerts & Anomaly Detection Dashboard

APIS detects anomalies like:

🚨 High Risk Orders (risk score ≥ 70)

⚠️ Quality issues (defect rate ≥ 6%)

📈 Price spikes (±10% change)

⏳ Delivery delays

Alerts module: 5*🚨_Alerts*&\_Anomalies.py

5*🚨_Alerts*&\_Anomalies

Isolation Forest anomaly engine: anomaly_detection.py

anomaly_detection

✅ 7) ML Delay Prediction (Supplier History Based)

Delay prediction is upgraded to be more realistic using supplier historical performance:

supplier_avg_delay_days

supplier_avg_defect_rate

supplier_on_time_rate

User selects a supplier and enters order details → model predicts:

✅ On-Time
🚨 Delayed

Delay predictor UI: 6_🤖_Delay_Predictor.py

6_🤖_Delay_Predictor

✅ 8) Model Retraining + Best Model Selection (LR vs RF)

APIS supports adaptive learning through retraining:

Trains both Logistic Regression & Random Forest

Selects best model using F1-score

Saves best model to models/model.pkl

Stores training logs to logs/training_log.csv

Generates reports/model_comparison.csv

Retraining engine: retrain_model.py

retrain_model

Retrain dashboard page: 8*🔁_Retrain*&\_Logs.py

8*🔁_Retrain*&\_Logs

✅ 9) Reports & Bulk Export Downloads (ZIP Support)

A dedicated Reports Center allows users to download:

Supplier Risk Report

Anomaly Detection Report

Supplier Clustering Report

Procurement Summary

It also supports bulk export ZIP containing all CSVs.

Reports page: 7*📄_Reports*&\_Downloads.py

7*📄_Reports*&\_Downloads

🏗️ System Workflow / Architecture

1. Order Data Collection (CSV dataset)
   ⬇
2. Risk Score Calculation + Supplier Ranking
   ⬇
3. Supplier Clustering (Segmentation)
   ⬇
4. Anomaly Detection (Isolation Forest)
   ⬇
5. ML Delay Prediction (Supplier + Order Features)
   ⬇
6. Dashboard Visualization + Reports Export
   ⬇
7. Retraining & Logs (Adaptive Learning)

🧰 Tech Stack
🖥️ Frontend / UI

Streamlit (Multi-page dashboard)

⚙️ Backend / Analytics / ML

Python

Pandas / NumPy

Scikit-learn

Joblib

📦 Models Used

RandomForestClassifier

LogisticRegression

IsolationForest

K-Means (for clustering report)

📂 Project Structure

adaptive-procurement-intelligence-system/
│
├── app/
│ ├── theme.py
│ ├── utils.py
│ ├── *🏠_Dashboard.py
│ └── pages/
│ ├── 1*📊*Overview.py
│ ├── 2*📦*Orders_Explorer.py
│ ├── 3*🏢*Suppliers.py
│ ├── 4*🧩*Supplier Segmentation.py
│ ├── 5*🚨*Alerts*&*Anomalies.py
│ ├── 6*🤖*Delay_Predictor.py
│ ├── 7*📄*Reports*&*Downloads.py
│ └── 8*🔁*Retrain*&\_Logs.py
│
├── dataset/
│ ├── orders.csv
│ ├── suppliers.csv
│ ├── supplier_risk_report.csv
│ ├── supplier_clusters.csv
│ └── anomaly_report.csv
│
├── models/
│ └── model.pkl
│
├── src/
│ ├── retrain_model.py
│ ├── anomaly_detection.py
│ └── risk_score.py
│
├── reports/
│ └── model_comparison.csv
│
├── logs/
│ └── training_log.csv
│
├── requirements.txt
└── README.md

📊 Dataset Details

This project uses procurement order records containing supplier and order performance information.

Common dataset columns include:

order_id

supplier_id

quantity

unit_price

defect_rate

delay_days

order_status (OnTime / Delayed)

order_priority

region

price_change_percent

shipping_mode

payment_terms

item_category

⚙️ Installation & Setup
✅ 1) Clone the Repository
git clone https://github.com/RaKa8904/adaptive-procurement-intelligence-system.git
cd adaptive-procurement-intelligence-system

✅ 2) Install Dependencies
pip install -r requirements.txt

✅ 3) Run the Dashboard
streamlit run \_🏠_Dashboard.py

🚀 How to Use the Dashboard

Once the dashboard is running:

🏠 Dashboard Home

Shows quick system status, alerts, trends, and top risky suppliers.

KPIs + order distribution + priority breakdown.

📦 Orders Explorer

Filter orders and view performance metrics.

🏢 Suppliers

Supplier master data + risk ranking + risk distribution.

🧩 Supplier Segmentation

Cluster suppliers into reliable/moderate/risky groups.

🚨 Alerts & Anomalies

Detect risky orders, quality issues, price spikes, delays.

🤖 Delay Predictor

Predict whether a new order will be delayed using ML.

📄 Reports & Downloads

Download CSV reports + bulk ZIP export.

🔁 Retrain & Logs

Retrain ML models and monitor training logs.

📌 Future Scope (Optional Enhancements)

Add PostgreSQL/SQL database integration

Role-based authentication (Admin / Analyst)

Real-time supplier alerts via Email/SMS

PowerBI/Tableau connector exports

Explainable AI (SHAP) for prediction reasoning

Deployment on Streamlit Cloud / AWS / Azure

👨‍💻 Author

Built by Raka 💙
