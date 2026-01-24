import streamlit as st
from app.utils import load_clusters
import pandas as pd
from app.theme import apply_dark_theme
apply_dark_theme()

st.set_page_config(page_title="Clustering", layout="wide")

# Custom styling
st.markdown("""
<style>
    .cluster-card {
        border-radius: 10px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .cluster-card:hover {
        transform: translateY(-5px);
    }
    
    .cluster-reliable {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .cluster-moderate {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .cluster-risky {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .cluster-value {
        font-size: 2rem;
        font-weight: 800;
        margin: 1rem 0;
    }
    
    .cluster-label {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
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
    
    .cluster-description {
        background: #111c2e;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #06b6d4;
        margin-bottom: 1rem;
        border: 1px solid #22314d;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🧩 Supplier Segmentation Analysis")
st.markdown("K-Means clustering for strategic supplier classification")

clusters = load_clusters()

# Calculate cluster statistics
if 'cluster' in clusters.columns:
    cluster_counts = clusters['cluster'].value_counts().sort_index()
else:
    # Try alternative column names
    cluster_col = None
    for col in clusters.columns:
        if 'cluster' in col.lower():
            cluster_col = col
            break
    
    if cluster_col:
        cluster_counts = clusters[cluster_col].value_counts().sort_index()
    else:
        cluster_counts = pd.Series([len(clusters)])

# Map clusters to labels
cluster_labels = {0: "🟢 Reliable", 1: "🟠 Moderate", 2: "🔴 Risky"}
cluster_descriptions = {
    0: "High reliability, low defects, consistent on-time delivery",
    1: "Medium reliability, occasional delays, moderate defect rates",
    2: "Low reliability, frequent delays, high defect rates"
}

# KPI Cards
st.markdown("### 📊 Cluster Distribution")
col1, col2, col3 = st.columns(3)

clusters_to_show = 3
for idx in range(min(clusters_to_show, len(cluster_counts))):
    with [col1, col2, col3][idx]:
        label = cluster_labels.get(idx, f"Cluster {idx}")
        count = cluster_counts.iloc[idx] if idx < len(cluster_counts) else 0
        
        cluster_class = ["cluster-reliable", "cluster-moderate", "cluster-risky"][idx]
        st.markdown(f"""
        <div class="cluster-card {cluster_class}">
            <div class="cluster-label">{label.split()[1]}</div>
            <div class="cluster-value">{int(count)}</div>
            <div class="cluster-label">Suppliers</div>
        </div>
        """, unsafe_allow_html=True)

# Clustering Information
st.markdown(f"<div class='section-header'>ℹ️ Clustering Overview</div>", unsafe_allow_html=True)

st.markdown("""
<div class="cluster-description">
    <h4 style="margin-top: 0;">K-Means Clustering Algorithm</h4>
    <p>
    Suppliers are automatically segmented into three categories based on their performance metrics:
    delivery reliability, defect rates, and compliance history. This enables strategic supplier 
    management and risk mitigation.
    </p>
</div>
""", unsafe_allow_html=True)

# Detailed Cluster Descriptions
col1, col2, col3 = st.columns(3)

cluster_info = [
    {
        "title": "🟢 Reliable Suppliers",
        "color": "#10b981",
        "traits": ["High on-time delivery rate", "Low defect rates", "Consistent quality", "Trustworthy partners"]
    },
    {
        "title": "🟠 Moderate Suppliers",
        "color": "#f59e0b",
        "traits": ["Occasional delays", "Moderate quality", "Requires monitoring", "Room for improvement"]
    },
    {
        "title": "🔴 Risky Suppliers",
        "color": "#ef4444",
        "traits": ["Frequent delays", "High defect rates", "Low reliability", "Needs intervention"]
    }
]

for idx, col in enumerate([col1, col2, col3]):
    with col:
        info = cluster_info[idx]
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {info['color']}20 0%, {info['color']}10 100%); 
                    border-left: 4px solid {info['color']}; padding: 1rem; border-radius: 8px;">
            <h4 style="color: {info['color']}; margin-top: 0;">{info['title']}</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
        """, unsafe_allow_html=True)
        
        for trait in info['traits']:
            st.markdown(f"<li>{trait}</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)

# Detailed Data Table
st.markdown(f"<div class='section-header'>📋 Complete Supplier Segmentation Data</div>", unsafe_allow_html=True)

# Add search/filter functionality
search_term = st.text_input("🔍 Search suppliers", placeholder="Search by supplier ID or name")

filtered_clusters = clusters.copy()
if search_term:
    filtered_clusters = filtered_clusters[
        filtered_clusters.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
    ]

# Display count
st.info(f"Showing {len(filtered_clusters)} of {len(clusters)} suppliers")

# Color code the cluster column
if 'cluster' in filtered_clusters.columns:
    cluster_col = 'cluster'
elif any('cluster' in col.lower() for col in filtered_clusters.columns):
    cluster_col = [col for col in filtered_clusters.columns if 'cluster' in col.lower()][0]
else:
    cluster_col = None

# Display the dataframe
st.dataframe(
    filtered_clusters,
    use_container_width=True,
    hide_index=True
)

# Cluster Statistics
st.markdown(f"<div class='section-header'>📊 Segment Statistics</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Supplier Count by Cluster")
    if cluster_col and cluster_col in clusters.columns:
        dist_data = pd.DataFrame({
            'Cluster': ['Reliable', 'Moderate', 'Risky'],
            'Count': [
                (clusters[cluster_col] == 0).sum(),
                (clusters[cluster_col] == 1).sum(),
                (clusters[cluster_col] == 2).sum()
            ]
        })
    else:
        dist_data = pd.DataFrame({
            'Cluster': ['Reliable', 'Moderate', 'Risky'],
            'Count': [0, 0, 0]
        })
    
    st.bar_chart(dist_data.set_index('Cluster'))

with col2:
    st.markdown("#### Cluster Proportion")
    st.bar_chart(dist_data.set_index('Cluster'))
