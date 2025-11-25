import streamlit as st
import json
import pandas as pd
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.dashboard.plot_components import (
    plot_sentiment_distribution, 
    plot_top_topics, 
    plot_sentiment_over_time,
    plot_skills_gap
)

# Page Config
st.set_page_config(
    page_title="Databricks Engagement Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Design System with Accessibility & Responsiveness
st.markdown("""
<style>
    /* ========================================
       DESIGN TOKENS (CSS Custom Properties)
       ======================================== */
    
    :root {
        /* Color Palette - WCAG AA Compliant */
        /* Primary: Blue - for interactive elements */
        --color-primary: #0066CC;           /* 4.54:1 on white (AA) */
        --color-primary-hover: #0052A3;     /* Darker for hover states */
        --color-primary-light: #E6F2FF;     /* Backgrounds */
        
        /* Neutrals - Grayscale with verified contrast */
        --color-text-primary: #1D1D1F;      /* 15.3:1 on white (AAA) */
        --color-text-secondary: #4A4A4A;    /* 9.73:1 on white (AAA) */
        --color-text-tertiary: #6B6B6B;     /* 5.74:1 on white (AA) */
        
        --color-bg-primary: #FFFFFF;
        --color-bg-secondary: #F5F5F7;      /* Subtle backgrounds */
        --color-bg-tertiary: #E8E8ED;       /* Borders, dividers */
        
        /* Semantic Colors - Color-blind safe */
        --color-success: #00875A;           /* Positive sentiment */
        --color-warning: #FF991F;           /* Neutral sentiment */
        --color-danger: #DE350B;            /* Negative sentiment */
        --color-info: #0065FF;
        
        /* Spacing Scale - Based on 4px grid */
        --space-xs: 0.25rem;    /* 4px */
        --space-sm: 0.5rem;     /* 8px */
        --space-md: 1rem;       /* 16px */
        --space-lg: 1.5rem;     /* 24px */
        --space-xl: 2rem;       /* 32px */
        --space-2xl: 3rem;      /* 48px */
        --space-3xl: 4rem;      /* 64px */
        
        /* Typography Scale - Fluid with clamp() */
        --font-size-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
        --font-size-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
        --font-size-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
        --font-size-lg: clamp(1.125rem, 1rem + 0.625vw, 1.5rem);
        --font-size-xl: clamp(1.5rem, 1.25rem + 1.25vw, 2rem);
        --font-size-2xl: clamp(2rem, 1.5rem + 2.5vw, 3rem);
        
        /* Line Heights */
        --line-height-tight: 1.2;
        --line-height-normal: 1.5;
        --line-height-relaxed: 1.75;
        
        /* Font Weights */
        --font-weight-normal: 400;
        --font-weight-medium: 500;
        --font-weight-semibold: 600;
        --font-weight-bold: 700;
        
        /* Border Radius */
        --radius-sm: 0.25rem;   /* 4px */
        --radius-md: 0.5rem;    /* 8px */
        --radius-lg: 0.75rem;   /* 12px */
        --radius-xl: 1rem;      /* 16px */
        
        /* Shadows - Subtle depth */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        
        /* Transitions */
        --transition-fast: 150ms ease;
        --transition-base: 250ms ease;
        --transition-slow: 350ms ease;
        
        /* Breakpoints (for reference in media queries) */
        --breakpoint-sm: 640px;
        --breakpoint-md: 768px;
        --breakpoint-lg: 1024px;
        --breakpoint-xl: 1280px;
    }
    
    /* ========================================
       BASE LAYOUT & TYPOGRAPHY
       ======================================== */
    
    .main {
        background-color: var(--color-bg-primary);
        color: var(--color-text-primary);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: var(--font-size-base);
        line-height: var(--line-height-normal);
        padding: var(--space-lg);
    }
    
    /* Responsive padding for main container */
    @media (max-width: 768px) {
        .main {
            padding: var(--space-md);
        }
    }
    
    /* ========================================
       SIDEBAR
       ======================================== */
    
    section[data-testid="stSidebar"] {
        background-color: var(--color-bg-secondary);
        border-right: 1px solid var(--color-bg-tertiary);
        padding: var(--space-lg);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--color-text-primary);
    }
    
    /* ========================================
       TYPOGRAPHY HIERARCHY
       ======================================== */
    
    h1 {
        font-size: var(--font-size-2xl);
        font-weight: var(--font-weight-bold);
        color: var(--color-text-primary);
        line-height: var(--line-height-tight);
        margin-bottom: var(--space-md);
    }
    
    h2 {
        font-size: var(--font-size-xl);
        font-weight: var(--font-weight-semibold);
        color: var(--color-text-primary);
        line-height: var(--line-height-tight);
        margin-bottom: var(--space-sm);
    }
    
    h3 {
        font-size: var(--font-size-lg);
        font-weight: var(--font-weight-semibold);
        color: var(--color-text-primary);
        line-height: var(--line-height-normal);
        margin-bottom: var(--space-sm);
    }
    
    p, li, .stMarkdown {
        font-size: var(--font-size-base);
        color: var(--color-text-secondary);
        line-height: var(--line-height-relaxed);
    }
    
    /* ========================================
       METRIC CARDS - Responsive Grid
       ======================================== */
    
    /* Override Streamlit's column behavior for better responsiveness */
    div[data-testid="column"] {
        padding: var(--space-sm);
    }
    
    .stMetric {
        background-color: var(--color-bg-secondary);
        padding: var(--space-lg);
        border-radius: var(--radius-lg);
        border: 1px solid var(--color-bg-tertiary);
        box-shadow: var(--shadow-sm);
        transition: all var(--transition-base);
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .stMetric:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--color-primary-light);
        transform: translateY(-2px);
    }
    
    .stMetric label {
        font-size: var(--font-size-sm) !important;
        color: var(--color-text-tertiary) !important;
        font-weight: var(--font-weight-medium) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: var(--space-xs);
    }
    
    .stMetric div[data-testid="stMetricValue"] {
        font-size: clamp(1.75rem, 1.5rem + 1vw, 2.5rem) !important;
        color: var(--color-text-primary) !important;
        font-weight: var(--font-weight-bold) !important;
        line-height: 1.2 !important;
    }
    
    /* Responsive metric layout */
    @media (max-width: 768px) {
        .stMetric {
            margin-bottom: var(--space-md);
        }
    }
    
    /* ========================================
       TABS - Modern Underline Style
       ======================================== */
    
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--space-lg);
        margin-bottom: var(--space-xl);
        border-bottom: 2px solid var(--color-bg-tertiary);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: var(--space-md) var(--space-lg);
        background-color: transparent;
        border-radius: 0;
        color: var(--color-text-tertiary);
        font-weight: var(--font-weight-medium);
        font-size: var(--font-size-base);
        border: none;
        transition: all var(--transition-fast);
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--color-text-primary);
        background-color: var(--color-bg-secondary);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--color-primary);
        font-weight: var(--font-weight-semibold);
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"]::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        right: 0;
        height: 3px;
        background-color: var(--color-primary);
        border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    }
    
    /* Responsive tabs */
    @media (max-width: 640px) {
        .stTabs [data-baseweb="tab-list"] {
            gap: var(--space-sm);
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: var(--space-sm) var(--space-md);
            font-size: var(--font-size-sm);
            white-space: nowrap;
        }
    }
    
    /* ========================================
       TABLES
       ======================================== */
    
    div[data-testid="stTable"] {
        font-size: var(--font-size-sm);
        overflow-x: auto;
    }
    
    div[data-testid="stTable"] table {
        min-width: 100%;
        border-collapse: collapse;
    }
    
    div[data-testid="stTable"] th {
        background-color: var(--color-bg-secondary);
        color: var(--color-text-primary);
        font-weight: var(--font-weight-semibold);
        padding: var(--space-md);
        text-align: left;
        border-bottom: 2px solid var(--color-bg-tertiary);
    }
    
    div[data-testid="stTable"] td {
        padding: var(--space-md);
        border-bottom: 1px solid var(--color-bg-tertiary);
        color: var(--color-text-secondary);
    }
    
    div[data-testid="stTable"] tr:hover {
        background-color: var(--color-bg-secondary);
    }
    
    /* ========================================
       INFO BOXES & ALERTS
       ======================================== */
    
    .stAlert {
        font-size: var(--font-size-base);
        padding: var(--space-md) var(--space-lg);
        border-radius: var(--radius-md);
        border-left: 4px solid var(--color-info);
        background-color: var(--color-primary-light);
        margin-bottom: var(--space-md);
    }
    
    /* ========================================
       BUTTONS & INTERACTIVE ELEMENTS
       ======================================== */
    
    .stButton > button {
        background-color: var(--color-primary);
        color: white;
        border: none;
        padding: var(--space-sm) var(--space-lg);
        border-radius: var(--radius-md);
        font-weight: var(--font-weight-medium);
        font-size: var(--font-size-base);
        transition: all var(--transition-base);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background-color: var(--color-primary-hover);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    .stButton > button:focus {
        outline: 3px solid var(--color-primary-light);
        outline-offset: 2px;
    }
    
    /* ========================================
       SELECTBOX & INPUT ELEMENTS
       ======================================== */
    
    .stSelectbox > div > div {
        border-radius: var(--radius-md);
        border-color: var(--color-bg-tertiary);
        font-size: var(--font-size-base);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--color-primary);
        box-shadow: 0 0 0 3px var(--color-primary-light);
    }
    
    /* ========================================
       MULTISELECT
       ======================================== */
    
    .stMultiSelect > div > div {
        border-radius: var(--radius-md);
        font-size: var(--font-size-base);
    }
    
    /* ========================================
       PLOTLY CHARTS - Responsive Containers
       ======================================== */
    
    div[data-testid="stPlotlyChart"] {
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        background-color: var(--color-bg-primary);
        padding: var(--space-md);
        margin-bottom: var(--space-lg);
    }
    
    /* Ensure charts are responsive */
    .js-plotly-plot {
        width: 100% !important;
    }
    
    /* ========================================
       HORIZONTAL DIVIDERS
       ======================================== */
    
    hr {
        border: none;
        height: 1px;
        background-color: var(--color-bg-tertiary);
        margin: var(--space-xl) 0;
    }
    
    /* ========================================
       ACCESSIBILITY - FOCUS STATES
       ======================================== */
    
    a:focus,
    button:focus,
    select:focus,
    input:focus {
        outline: 3px solid var(--color-primary);
        outline-offset: 2px;
    }
    
    /* ========================================
       RESPONSIVE UTILITIES
       ======================================== */
    
    /* Hide elements on mobile */
    @media (max-width: 640px) {
        .hide-mobile {
            display: none !important;
        }
    }
    
    /* Stack columns on small screens */
    @media (max-width: 768px) {
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    
    /* ========================================
       LOADING STATES & ANIMATIONS
       ======================================== */
    
    .stSpinner > div {
        border-color: var(--color-primary) transparent transparent transparent !important;
    }
    
    /* Smooth scroll behavior */
    html {
        scroll-behavior: smooth;
    }
    
    /* Reduce motion for users who prefer it */
    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    data_path = "data/processed/analytics_results.json"
    if not os.path.exists(data_path):
        st.error(f"Data file not found at {data_path}. Please run the pipeline first.")
        return None, None
        
    with open(data_path, "r") as f:
        data = json.load(f)
        
    engagements = pd.DataFrame(data["engagements"])
    
    # Flatten nested dicts
    engagements['sentiment_type'] = engagements['sentiment'].apply(lambda x: x.get('sentiment_type'))
    engagements['sentiment_score'] = engagements['sentiment'].apply(lambda x: x.get('sentiment_score'))
    engagements['topic'] = engagements['topic'].apply(lambda x: x.get('topic'))
    
    return engagements, data["weekly_summary"]

def main():
    st.title("Databricks Engagement Intelligence")
    st.markdown("### PS Leadership Dashboard")
    
    df, summary = load_data()
    
    if df is None:
        return

    # Sidebar
    st.sidebar.header("Filters")
    selected_status = st.sidebar.multiselect(
        "Status", 
        options=df['status'].unique(), 
        default=df['status'].unique()
    )
    
    if selected_status:
        df_filtered = df[df['status'].isin(selected_status)]
    else:
        df_filtered = df

    # Top Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Engagements", len(df_filtered))
    c2.metric("Avg Sentiment", f"{df_filtered['sentiment_score'].mean():.2f}")
    c3.metric("Positive Feedback", len(df_filtered[df_filtered['sentiment_type'] == 'positive']))
    c4.metric("At Risk", len(df_filtered[df_filtered['status'] == 'at-risk']))

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Engagement Sentiment", 
        "Top Issues", 
        "Skills Gap", 
        "Weekly Executive Summary"
    ])

    with tab1:
        st.subheader("Sentiment Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_sentiment_distribution(df_filtered), use_container_width=True)
        with col2:
            st.plotly_chart(plot_sentiment_over_time(df_filtered), use_container_width=True)
            
        st.markdown("#### Recent Negative Feedback")
        negative_feedback = df_filtered[df_filtered['sentiment_type'] == 'negative'][['customer', 'feedback', 'date']].head(5)
        st.table(negative_feedback)

    with tab2:
        st.subheader("Topic Modeling & Issues")
        st.plotly_chart(plot_top_topics(df_filtered), use_container_width=True)
        
        st.markdown("#### Detailed Notes by Topic")
        selected_topic = st.selectbox("Select Topic", df_filtered['topic'].unique())
        topic_notes = df_filtered[df_filtered['topic'] == selected_topic][['customer', 'notes']].head(5)
        for _, row in topic_notes.iterrows():
            st.info(f"**{row['customer']}**: {row['notes']}")

    with tab3:
        st.subheader("Skills Gap Analysis")
        st.markdown("Comparing market demand (engagement frequency) vs. estimated team proficiency.")
        st.plotly_chart(plot_skills_gap(df_filtered), use_container_width=True)

    with tab4:
        st.subheader("Weekly Executive Briefing")
        st.markdown(f"""
        <div style="
            background-color: var(--color-bg-secondary); 
            padding: var(--space-xl); 
            border-radius: var(--radius-lg); 
            border-left: 4px solid var(--color-primary); 
            box-shadow: var(--shadow-sm);
            margin-bottom: var(--space-lg);
        ">
            <pre style="
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
                font-size: var(--font-size-base); 
                white-space: pre-wrap; 
                color: var(--color-text-primary); 
                line-height: var(--line-height-relaxed);
                margin: 0;
            ">{summary}</pre>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Recommended Actions")
        st.markdown("""
        - **Training**: Schedule deep-dive sessions on Unity Catalog and Streaming.
        - **Hiring**: Prioritize candidates with strong Terraform and Governance experience.
        - **Process**: Review onboarding checklist to reduce initial configuration friction.
        """)

if __name__ == "__main__":
    main()
