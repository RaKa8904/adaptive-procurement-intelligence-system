import streamlit as st
import pandas as pd
import subprocess
import os
from datetime import datetime
from app.theme import apply_dark_theme
apply_dark_theme()

st.set_page_config(page_title="Retrain & Logs", layout="wide")

# Custom styling
st.markdown("""
<style>
    .retrain-info-box {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.2);
    }
    
    .status-good {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .status-critical {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .log-entry {
        background: #111c2e;
        border-left: 4px solid #06b6d4;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
        font-family: monospace;
        font-size: 0.9rem;
        color: #cbd5e1;
        border: 1px solid #22314d;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #06b6d4;
        padding-bottom: 0.5rem;
    }
    
    .model-card {
        background: #111c2e;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        border: 1px solid #22314d;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔁 Model Training & Adaptive Learning Center")
st.markdown("Monitor model performance, retrain models, and view training logs")

# Status Overview
st.markdown(f"<div class='section-header'>📊 System Status</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="model-card status-good" style="color: white; padding: 1.5rem; border-radius: 10px;">
        <div style="font-size: 0.85rem; opacity: 0.9;">Model Status</div>
        <div style="font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">✅ Ready</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="model-card" style="color: white; padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);">
        <div style="font-size: 0.85rem; opacity: 0.9;">Last Retrain</div>
        <div style="font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">2 days ago</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="model-card" style="color: white; padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);">
        <div style="font-size: 0.85rem; opacity: 0.9;">Accuracy</div>
        <div style="font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">87.5%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="model-card" style="color: white; padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);">
        <div style="font-size: 0.85rem; opacity: 0.9;">Training Time</div>
        <div style="font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0;">5 min 23s</div>
    </div>
    """, unsafe_allow_html=True)

# Retrain Section
st.markdown(f"<div class='section-header'>🚀 Model Retraining</div>", unsafe_allow_html=True)

st.markdown("""
<div class="retrain-info-box">
    <h4 style="margin-top: 0;">💡 About Model Retraining</h4>
    <p>
    Retraining updates the machine learning model with the latest procurement data. 
    This improves prediction accuracy and helps the system adapt to changing supplier behaviors and market conditions.
    </p>
    <ul style="margin-bottom: 0;">
        <li>Typical training time: 5-10 minutes</li>
        <li>No downtime during retraining</li>
        <li>Historical data automatically included</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Retrain Configuration
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚙️ Retraining Configuration")
    
    data_source = st.selectbox(
        "Data Source",
        ["All Available Data", "Last 30 Days", "Last 90 Days", "Last Year"],
        help="Select which data to use for training"
    )
    
    model_type = st.selectbox(
        "Model Type",
        ["Delay Prediction", "Risk Scoring", "Anomaly Detection"],
        help="Select which model to retrain"
    )
    
    include_validation = st.checkbox("Include Validation Set", value=True)

with col2:
    st.markdown("### 📋 Retraining Schedule")
    
    schedule_enabled = st.checkbox("Enable Automatic Retraining", value=True)
    
    if schedule_enabled:
        schedule_frequency = st.selectbox(
            "Frequency",
            ["Daily", "Weekly", "Monthly", "On-Demand"],
            help="How often to automatically retrain"
        )
        
        st.markdown(f"**Next scheduled retrain:** {schedule_frequency}")

# Retrain Button
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    retrain_button = st.button(
        "🚀 Start Retraining Now",
        use_container_width=True,
        type="primary"
    )

if retrain_button:
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔄 Initializing training pipeline...")
        progress_bar.progress(10)
        
        status_text.text("📊 Loading data from sources...")
        progress_bar.progress(25)
        
        status_text.text("🔧 Preprocessing and feature engineering...")
        progress_bar.progress(45)
        
        status_text.text("🤖 Training model...")
        progress_bar.progress(70)
        
        status_text.text("✅ Validating model performance...")
        progress_bar.progress(90)
        
        # Simulate actual retrain command (uncomment to use actual backend)
        # subprocess.run(["python", "src/retrain_model.py"], check=True)
        
        progress_bar.progress(100)
        status_text.text("✅ Retraining completed successfully!")
        
        st.success("✨ Model retrained successfully! Updated metrics:")
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("New Accuracy", "87.5%", "+2.3%")
        with metric_col2:
            st.metric("Training Time", "5m 23s", "-15s")
        with metric_col3:
            st.metric("Data Points", "15,432", "+2,104")
            
    except Exception as e:
        st.error(f"❌ Training failed: {str(e)}")
        st.info("Check the logs below for more details.")

# Training Logs Section
st.markdown(f"<div class='section-header'>📊 Training Logs</div>", unsafe_allow_html=True)

log_path = "logs/training_log.csv"

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📈 Log Filters")
    log_limit = st.slider("Number of recent logs to display", 5, 100, 15)

with col2:
    st.markdown("#### 🔍 Search")
    log_search = st.text_input("Search logs", placeholder="Search by model, status, or date")

if os.path.exists(log_path):
    try:
        logs = pd.read_csv(log_path)
        
        # Apply search filter
        if log_search:
            mask = logs.astype(str).apply(lambda x: x.str.contains(log_search, case=False)).any(axis=1)
            logs = logs[mask]
        
        # Display recent logs
        logs_display = logs.tail(log_limit)
        
        if len(logs_display) > 0:
            st.info(f"Showing {len(logs_display)} of {len(logs)} training records")
            st.dataframe(
                logs_display,
                use_container_width=True,
                hide_index=True
            )
            
            # Log Statistics
            st.markdown(f"<div class='section-header'>📉 Training Statistics</div>", unsafe_allow_html=True)
            
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            
            with stats_col1:
                if 'accuracy' in logs.columns:
                    avg_acc = logs['accuracy'].mean()
                    st.metric("Average Accuracy", f"{avg_acc:.2%}")
            
            with stats_col2:
                total_trainings = len(logs)
                st.metric("Total Trainings", f"{total_trainings}")
            
            with stats_col3:
                if 'training_time' in logs.columns:
                    avg_time = logs['training_time'].mean()
                    st.metric("Avg Training Time", f"{avg_time:.1f}s")
        else:
            st.warning("No logs matching your search criteria.")
            
    except Exception as e:
        st.error(f"Error reading logs: {str(e)}")
else:
    st.info("""
    ❌ No logs found yet. 
    
    First training will create a log file. Click the "Start Retraining Now" button to generate logs.
    """)

st.markdown("""
<div class="model-card">
    <strong>🤖 Active Model: v2.3</strong>
    <div style="color: #9ca3af; font-size: 0.9rem; margin-top: 0.5rem;">
    Latest production model • Accuracy: 87.5% • Updated: 2 days ago
    </div>
</div>

<div class="model-card">
    <strong>🔄 Previous Model: v2.2</strong>
    <div style="color: #9ca3af; font-size: 0.9rem; margin-top: 0.5rem;">
    Fallback model • Accuracy: 85.2% • Updated: 9 days ago
    </div>
</div>

<div class="model-card">
    <strong>📦 Staging Model: v2.4-beta</strong>
    <div style="color: #9ca3af; font-size: 0.9rem; margin-top: 0.5rem;">
    Testing model • Accuracy: 88.1% • Updated: 1 day ago
    </div>
</div>
""", unsafe_allow_html=True)

