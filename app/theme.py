import streamlit as st

def apply_dark_theme():
    st.markdown("""
    <style>
    :root{
        --bg: #0b1220;
        --card: #111c2e;
        --card2: #0f1a2c;
        --border: #22314d;
        --text: #e5e7eb;
        --muted: #9ca3af;
        --accent: #22d3ee;
        --accent2: #3b82f6;
    }

    [data-testid="stAppViewContainer"]{
        background: radial-gradient(circle at top left, #0f172a 0%, var(--bg) 60%);
        color: var(--text);
    }

    [data-testid="stSidebar"]{
        background: linear-gradient(180deg, var(--bg) 0%, #0f172a 100%);
        border-right: 1px solid var(--border);
    }

    h1,h2,h3,h4,h5,h6,p,span,label{
        color: var(--text) !important;
    }

    .stMarkdown, .stText{
        color: var(--text);
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input, textarea{
        background-color: var(--card) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }

    /* Selectbox / multiselect */
    div[data-baseweb="select"] > div{
        background-color: var(--card) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }

    /* Default buttons */
.stButton button{
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #061018 !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    padding: 0.6rem 1rem !important;
}

.apis-navbar .stButton button{
    background: rgba(15, 26, 44, 0.40) !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(34, 49, 77, 0.75) !important;
}

    [data-testid="stMetric"]{
    background: var(--card);
    border: 1px solid var(--border);
    padding: 1rem;
    border-radius: 14px;
}

[data-testid="stMetric"] *{
    background: transparent !important;
}


    /* Dataframe */
    [data-testid="stDataFrame"]{
        background: var(--card);
        border-radius: 14px;
        border: 1px solid var(--border);
        overflow: hidden;
    }

    /* Tabs */
    button[data-baseweb="tab"]{
        color: var(--muted) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"]{
        color: var(--text) !important;
        border-bottom: 2px solid var(--accent) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    
