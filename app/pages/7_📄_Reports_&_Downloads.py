import streamlit as st
import os
from datetime import datetime
import io
import zipfile
import pandas as pd
import subprocess
from utils import load_orders, load_suppliers, load_risk_report, load_clusters, load_anomalies
from app.theme import apply_dark_theme

st.set_page_config(page_title="Reports & Downloads", layout="wide")

apply_dark_theme()

def create_bulk_export_zip():
    orders = load_orders()
    suppliers = load_suppliers()
    risk = load_risk_report()
    clusters = load_clusters()
    anomalies = load_anomalies()

    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("orders.csv", orders.to_csv(index=False))
        zf.writestr("suppliers.csv", suppliers.to_csv(index=False))
        zf.writestr("supplier_risk_report.csv", risk.to_csv(index=False))
        zf.writestr("supplier_clusters.csv", clusters.to_csv(index=False))
        zf.writestr("anomaly_report.csv", anomalies.to_csv(index=False))

    buffer.seek(0)
    return buffer

# Custom styling
st.markdown("""
<style>
    .report-card {
        background: #1e293b;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
        border: 1px solid #22314d;
    }
    
    .report-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.15);
    }
    
    .report-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
    }
    
    .report-description {
        color: #cbd5e1;
        font-size: 0.9rem;
        margin-bottom: 1rem;
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
    
    .download-btn-container {
        display: grid;
        gap: 1rem;
    }
    
    .info-box {
        background: #1e293b;
        border-left: 4px solid #06b6d4;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 📄 Reports & Downloads Center")
st.markdown("Export comprehensive procurement analytics and data exports")

# Info box
st.markdown("""
<div class="info-box">
    <strong>💡 Tip:</strong> Download reports in CSV format for further analysis in Excel, Python, or BI tools.
</div>
""", unsafe_allow_html=True)

# Available Reports Section
st.markdown(f"<div class='section-header'>📥 Available Reports</div>", unsafe_allow_html=True)

reports = [
    {
        "name": "Supplier Risk Report",
        "file": "dataset/supplier_risk_report.csv",
        "description": "Complete supplier risk assessment with scores and rankings",
        "icon": "🚨"
    },
    {
        "name": "Anomaly Detection Report",
        "file": "dataset/anomaly_report.csv",
        "description": "Identified anomalies, outliers, and quality issues",
        "icon": "⚠️"
    },
    {
        "name": "Supplier Clustering Report",
        "file": "dataset/supplier_clusters.csv",
        "description": "Supplier segmentation into reliability categories",
        "icon": "🧩"
    },
    {
        "name": "Procurement Summary",
        "file": "reports/final_procurement_summary.csv",
        "description": "Executive summary of all procurement activities",
        "icon": "📊"
    }
]

# Display reports in a grid
col1, col2 = st.columns(2)

for idx, report in enumerate(reports):
    col = col1 if idx % 2 == 0 else col2
    
    with col:
        st.markdown(f"""
        <div class="report-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{report['icon']}</div>
            <div class="report-title">{report['name']}</div>
            <div class="report-description">{report['description']}</div>
        """, unsafe_allow_html=True)
        
        # Check if file exists
        if os.path.exists(report['file']):
            try:
                with open(report['file'], "rb") as f:
                    file_size = os.path.getsize(report['file'])
                    file_size_kb = file_size / 1024
                    
                    st.download_button(
                        f"⬇️ Download ({file_size_kb:.1f} KB)",
                        f,
                        report['file'].split('/')[-1],
                        "text/csv",
                        use_container_width=True,
                        key=f"download_{idx}"
                    )
                    
                    st.markdown(f"""
                    <div style="font-size: 0.8rem; color: #999; margin-top: 0.5rem;">
                    ✅ Available • Updated: {datetime.fromtimestamp(os.path.getmtime(report['file'])).strftime('%Y-%m-%d %H:%M')}
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
        else:
            st.warning(f"❌ File not found: {report['file']}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Quick Export Options
st.markdown(f"<div class='section-header'>⚙️ Export Options</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔄 Bulk Export
    Export all available reports at once for comprehensive analysis and archiving.
    """)

    zip_buffer = create_bulk_export_zip()

    st.download_button(
        label="📦 Export All Reports (ZIP)",
        data=zip_buffer,
        file_name="APIS_Bulk_Export.zip",
        mime="application/zip",
        use_container_width=True
    )

with col2:
    st.markdown("""
    ### 📧 Email Reports
    Receive generated reports directly in your email inbox on a scheduled basis.
    """)
    
    email_address = st.text_input("Email address", placeholder="your@email.com")
    
    if st.button("📨 Send Report Now", use_container_width=True):
     if email_address:
        try:
            subprocess.run(
                ["python", "src/send_email_report.py", email_address],
                check=True
            )
            st.success(f"✅ Report sent successfully to {email_address}")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
    else:
        st.error("Please enter a valid email address")

# Data Dictionary Section
st.markdown(f"<div class='section-header'>📚 Data Dictionary</div>", unsafe_allow_html=True)

with st.expander("ℹ️ Expand to view column definitions"):
    st.markdown("""
    #### Supplier Risk Report Columns
    - **supplier_id**: Unique identifier for the supplier
    - **risk_score**: Calculated risk metric (0-100)
    - **on_time_rate**: Percentage of on-time deliveries
    - **defect_rate**: Average defect rate
    - **delivery_days**: Average delivery time in days
    
    #### Anomaly Report Columns
    - **order_id**: Unique order identifier
    - **anomaly_type**: Type of detected anomaly
    - **severity**: Severity level (Low, Medium, High, Critical)
    - **timestamp**: When the anomaly was detected
    
    #### Clustering Report Columns
    - **supplier_id**: Unique identifier for the supplier
    - **cluster**: Assigned cluster (0=Reliable, 1=Moderate, 2=Risky)
    - **cluster_probability**: Confidence score for cluster assignment
    
    #### Procurement Summary Columns
    - **metric_name**: Name of the metric
    - **value**: Calculated value
    - **period**: Time period covered
    - **trend**: Direction of change (Up/Down/Stable)
    """)

# Documentation Section
st.markdown(f"<div class='section-header'>📖 Documentation</div>", unsafe_allow_html=True)

doc_col1, doc_col2, doc_col3 = st.columns(3)

with doc_col1:
    st.markdown("""
    ### 🎯 Getting Started
    [View Quick Start Guide](https://docs.google.com/document/d/1kh6DDe-Vt8pBwdIX4ubFvTROPfVm0NLq6gedqMfAxzs/edit?usp=sharing)
    - Overview of the system
    - Key metrics explained
    - Common use cases
    """)

with doc_col2:
    st.markdown("""
    ### 📊 Analytics Guide
    [View Analytics Guide](https://docs.google.com/document/d/10jIRW2ItnEfJv3ndmOa58sejWnJFSYmjbLxa0A78YDc/edit?usp=sharing)
    - How to interpret reports
    - Best practices
    - Advanced analysis
    """)

with doc_col3:
    st.markdown("""
    ### 🔧 Integration Guide
    [View API Documentation](https://docs.google.com/document/d/1B_ig9DH69l1u0uVDnB8EBx_3Qz3TTZz18SuBriMxWEQ/edit?usp=sharing)
    - API endpoints
    - Authentication
    - Integration examples
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.85rem;">
    <p>Last updated: {}</p>
    <p>For support, contact: support@apis.example.com</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)


#$env:SMTP_USER="rakaotaku8904@gmail.com"
#$env:SMTP_PASS="qycu mjgl negy nopt"