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
        --color-success-bg: #E3FCEF;        /* Success background */
        --color-warning: #FF991F;           /* Neutral sentiment */
        --color-warning-bg: #FFF4E5;        /* Warning background */
        --color-danger: #DE350B;            /* Negative sentiment */
        --color-danger-bg: #FFEBE6;         /* Danger background */
        --color-info: #0065FF;
        --color-info-bg: #E6F2FF;           /* Info background */
        
        /* Status Colors */
        --color-status-healthy: #00875A;
        --color-status-at-risk: #DE350B;
        --color-status-warning: #FF991F;
        
        /* Container Colors */
        --color-card-bg: #FFFFFF;
        --color-card-border: #E8E8ED;
        
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
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        
        /* Max Widths */
        --container-max-width: 1400px;
        --content-max-width: 800px;
        
        /* Icon Sizes */
        --icon-sm: 1rem;
        --icon-md: 1.5rem;
        --icon-lg: 2rem;
        
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
        background-color: var(--color-card-bg);
        padding: var(--space-lg);
        border-radius: var(--radius-lg);
        border: 2px solid var(--color-card-border);
        box-shadow: var(--shadow-sm);
        transition: all var(--transition-base);
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .stMetric:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--color-primary);
        transform: translateY(-2px);
    }
    
    .stMetric label {
        font-size: var(--font-size-sm) !important;
        color: var(--color-text-tertiary) !important;
        font-weight: var(--font-weight-semibold) !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: var(--space-sm);
    }
    
    .stMetric div[data-testid="stMetricValue"] {
        font-size: clamp(2rem, 1.75rem + 1.25vw, 3rem) !important;
        color: var(--color-text-primary) !important;
        font-weight: var(--font-weight-bold) !important;
        line-height: 1.1 !important;
        margin-bottom: var(--space-xs);
    }
    
    .stMetric div[data-testid="stMetricDelta"] {
        font-size: var(--font-size-sm) !important;
        font-weight: var(--font-weight-medium) !important;
    }
    
    /* Responsive metric layout */
    @media (max-width: 768px) {
        .stMetric {
            margin-bottom: var(--space-md);
            min-height: 120px;
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
    
    /* ========================================
       NEW COMPONENT STYLES
       ======================================== */
    
    /* Alert Container - For prominent warnings/info */
    .alert-container {
        background: linear-gradient(135deg, var(--color-danger-bg) 0%, #FFF 100%);
        border-left: 5px solid var(--color-danger);
        border-radius: var(--radius-lg);
        padding: var(--space-lg) var(--space-xl);
        margin-bottom: var(--space-xl);
        box-shadow: var(--shadow-md);
    }
    
    .alert-container.info {
        background: linear-gradient(135deg, var(--color-info-bg) 0%, #FFF 100%);
        border-left-color: var(--color-info);
    }
    
    .alert-container.warning {
        background: linear-gradient(135deg, var(--color-warning-bg) 0%, #FFF 100%);
        border-left-color: var(--color-warning);
    }
    
    .alert-container h3 {
        margin-top: 0;
        margin-bottom: var(--space-sm);
        font-size: var(--font-size-lg);
        color: var(--color-text-primary);
    }
    
    /* Section Header - Clear visual dividers */
    .section-header {
        display: flex;
        align-items: center;
        gap: var(--space-md);
        margin-top: var(--space-2xl);
        margin-bottom: var(--space-lg);
        padding-bottom: var(--space-sm);
        border-bottom: 3px solid var(--color-primary);
    }
    
    .section-header h2 {
        margin: 0;
        font-size: var(--font-size-xl);
        font-weight: var(--font-weight-bold);
        color: var(--color-text-primary);
    }
    
    .section-header .icon {
        font-size: var(--icon-md);
        color: var(--color-primary);
    }
    
    /* Insight Card - Executive summary highlights */
    .insight-card {
        background-color: var(--color-card-bg);
        border: 2px solid var(--color-primary-light);
        border-radius: var(--radius-lg);
        padding: var(--space-xl);
        margin-bottom: var(--space-lg);
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
    }
    
    .insight-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
    }
    
    .insight-card h3 {
        margin-top: 0;
        margin-bottom: var(--space-md);
        color: var(--color-primary);
        font-size: var(--font-size-lg);
    }
    
    .insight-card ul {
        margin: 0;
        padding-left: var(--space-lg);
    }
    
    .insight-card li {
        margin-bottom: var(--space-sm);
        line-height: var(--line-height-relaxed);
    }
    
    /* Enhanced Data Table */
    .data-table-enhanced {
        width: 100%;
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        margin-bottom: var(--space-xl);
    }
    
    .data-table-enhanced table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .data-table-enhanced thead {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
        color: white;
    }
    
    .data-table-enhanced th {
        padding: var(--space-md) var(--space-lg);
        text-align: left;
        font-weight: var(--font-weight-semibold);
        font-size: var(--font-size-sm);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .data-table-enhanced td {
        padding: var(--space-md) var(--space-lg);
        border-bottom: 1px solid var(--color-bg-tertiary);
        font-size: var(--font-size-base);
    }
    
    .data-table-enhanced tbody tr:hover {
        background-color: var(--color-bg-secondary);
        transition: background-color var(--transition-fast);
    }
    
    .data-table-enhanced tbody tr:nth-child(even) {
        background-color: rgba(245, 245, 247, 0.5);
    }
    
    /* Status Badge */
    .stat-badge {
        display: inline-block;
        padding: var(--space-xs) var(--space-sm);
        border-radius: var(--radius-md);
        font-size: var(--font-size-xs);
        font-weight: var(--font-weight-semibold);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stat-badge.positive {
        background-color: var(--color-success-bg);
        color: var(--color-success);
    }
    
    .stat-badge.negative {
        background-color: var(--color-danger-bg);
        color: var(--color-danger);
    }
    
    .stat-badge.neutral {
        background-color: var(--color-warning-bg);
        color: var(--color-warning);
    }
    
    .stat-badge.at-risk {
        background-color: var(--color-danger-bg);
        color: var(--color-danger);
        font-weight: var(--font-weight-bold);
    }
    
    /* Help Text / Explanatory Content */
    .help-text {
        background-color: var(--color-info-bg);
        border-left: 4px solid var(--color-info);
        padding: var(--space-md) var(--space-lg);
        border-radius: var(--radius-md);
        margin-bottom: var(--space-lg);
        font-size: var(--font-size-sm);
        color: var(--color-text-secondary);
        line-height: var(--line-height-relaxed);
    }
    
    .help-text strong {
        color: var(--color-text-primary);
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
    # Header
    st.title("Databricks Engagement Intelligence Dashboard")
    st.markdown("""
    <p style='font-size: 1.1rem; color: var(--color-text-secondary); margin-bottom: 2rem;'>
        Real-time insights into customer engagement, sentiment trends, and team capabilities
    </p>
    """, unsafe_allow_html=True)
    
    df, summary = load_data()
    
    if df is None:
        return

    # Sidebar with Enhanced Filters
    st.sidebar.header("Dashboard Filters")
    st.sidebar.markdown("---")
    
    selected_status = st.sidebar.multiselect(
        "Filter by Engagement Status", 
        options=sorted(df['status'].unique()), 
        default=list(df['status'].unique()),
        help="Select one or more engagement statuses to filter the dashboard data"
    )
    
    # Apply filters
    if selected_status:
        df_filtered = df[df['status'].isin(selected_status)]
    else:
        df_filtered = df
    
    # Sidebar stats
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filter Results")
    total_records = len(df)
    filtered_records = len(df_filtered)
    st.sidebar.info(f"Showing **{filtered_records}** of **{total_records}** engagements")
    
    if filtered_records < total_records:
        st.sidebar.caption(f"{total_records - filtered_records} engagements hidden by filters")

    # Key Metrics Section
    st.markdown("## Key Performance Indicators")
    st.markdown("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    avg_sentiment = df_filtered['sentiment_score'].mean()
    positive_count = len(df_filtered[df_filtered['sentiment_type'] == 'positive'])
    at_risk_count = len(df_filtered[df_filtered['status'] == 'at-risk'])
    
    with col1:
        st.metric(
            "Total Engagements", 
            f"{len(df_filtered):,}",
            help="Total number of customer engagements in the selected period"
        )
    
    with col2:
        sentiment_delta = avg_sentiment - 0.5  # Compare to neutral
        st.metric(
            "Average Sentiment", 
            f"{avg_sentiment:.2f}",
            delta=f"{sentiment_delta:+.2f} vs neutral",
            delta_color="normal" if sentiment_delta >= 0 else "inverse",
            help="Average sentiment score (0=very negative, 1=very positive)"
        )
    
    with col3:
        positive_pct = (positive_count / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        st.metric(
            "Positive Feedback", 
            positive_count,
            delta=f"{positive_pct:.1f}%",
            help="Number of engagements with positive sentiment"
        )
    
    with col4:
        st.metric(
            "At Risk", 
            at_risk_count,
            delta=f"{(at_risk_count/len(df_filtered)*100):.1f}%" if len(df_filtered) > 0 else "0%",
            delta_color="inverse",
            help="Engagements flagged as at-risk requiring immediate attention"
        )

    st.markdown("---")

    # Alert Section - At-Risk Engagements (if any)
    if at_risk_count > 0:
        st.markdown("""
        <div class="alert-container">
            <h3>Action Required: At-Risk Engagements</h3>
            <p>The following engagements require immediate attention from leadership:</p>
        </div>
        """, unsafe_allow_html=True)
        
        at_risk_df = df_filtered[df_filtered['status'] == 'at-risk'][['customer', 'sentiment_score', 'feedback', 'date']].head(5)
        at_risk_df = at_risk_df.sort_values('sentiment_score')
        
        for idx, row in at_risk_df.iterrows():
            sentiment_color = "#DE350B" if row['sentiment_score'] < 0.3 else "#FF991F"
            st.markdown(f"""
            <div style="background-color: #FFEBE6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.75rem; border-left: 4px solid {sentiment_color};">
                <strong style="font-size: 1.1rem; color: #1D1D1F;">{row['customer']}</strong> 
                <span style="background-color: #FFF; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.85rem; margin-left: 0.5rem;">Sentiment: {row['sentiment_score']:.2f}</span>
                <br/>
                <span style="color: #6B6B6B; font-size: 0.9rem;">{row['date']}</span>
                <p style="margin-top: 0.5rem; color: #4A4A4A;">{row['feedback'][:200]}...</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")

    # ============================================================================
    # EXECUTIVE SNAPSHOT - Critical Information First
    # ============================================================================
    # Design rationale: Decision-makers need to see health status and priorities
    # immediately without scrolling or clicking tabs. This section answers:
    # "What needs my attention RIGHT NOW?"
    
    st.markdown("## Executive Snapshot")
    st.markdown("""
    <div class="help-text">
        <strong>Quick Decision View:</strong> Critical metrics, engagement health status, and action priorities at a glance.
    </div>
    """, unsafe_allow_html=True)
    
    # Visual health indicator
    avg_sentiment_pct = avg_sentiment * 100
    if avg_sentiment >= 0.55:
        health_status = "HEALTHY"
        health_color = "#00875A"
        health_bg = "#E3FCEF"
        health_icon = "✓"
    elif avg_sentiment >= 0.35:
        health_status = "WARNING"
        health_color = "#FF991F"
        health_bg = "#FFF4E5"
        health_icon = "⚠"
    else:
        health_status = "AT RISK"
        health_color = "#DE350B"
        health_bg = "#FFEBE6"
        health_icon = "!"
    
    # Three-column snapshot
    snap_col1, snap_col2, snap_col3 = st.columns([1, 1, 1])
    
    with snap_col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {health_bg} 0%, #FFF 100%); 
                    padding: 1.5rem; border-radius: 0.75rem; 
                    border: 3px solid {health_color}; min-height: 160px;
                    display: flex; flex-direction: column; justify-content: center;">
            <div style="text-align: center;">
                <div style="font-size: 3rem; color: {health_color}; font-weight: bold;">{health_icon}</div>
                <div style="font-size: 1.5rem; font-weight: bold; color: {health_color}; margin-top: 0.5rem;">
                    {health_status}
                </div>
                <div style="font-size: 0.9rem; color: #6B6B6B; margin-top: 0.5rem;">
                    Overall Engagement Health
                </div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #1D1D1F; margin-top: 0.5rem;">
                    {avg_sentiment_pct:.1f}% Sentiment Score
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with snap_col2:
        most_common_topic = df_filtered['topic'].mode()[0] if len(df_filtered) > 0 else "N/A"
        topic_count = len(df_filtered[df_filtered['topic'] == most_common_topic])
        topic_pct = (topic_count / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        
        st.markdown(f"""
        <div style="background-color: #F5F5F7; padding: 1.5rem; border-radius: 0.75rem; 
                    border: 2px solid #E8E8ED; min-height: 160px;">
            <h4 style="margin-top: 0; color: #0072B2; font-size: 1.1rem;">Top Issue Requiring Attention</h4>
            <div style="font-size: 1.3rem; font-weight: 600; color: #1D1D1F; margin: 0.75rem 0;">
                {most_common_topic}
            </div>
            <div style="color: #6B6B6B; font-size: 0.95rem;">
                {topic_count} engagements ({topic_pct:.1f}%)
            </div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #E8E8ED; font-size: 0.85rem; color: #4A4A4A;">
                <strong>Action:</strong> Review detailed analytics in Topics & Issues tab
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with snap_col3:
        positive_rate = (positive_count / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        at_risk_rate = (at_risk_count / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        
        st.markdown(f"""
        <div style="background-color: #F5F5F7; padding: 1.5rem; border-radius: 0.75rem; 
                    border: 2px solid #E8E8ED; min-height: 160px;">
            <h4 style="margin-top: 0; color: #0072B2; font-size: 1.1rem;">Engagement Breakdown</h4>
            <div style="margin: 0.5rem 0;">
                <span style="color: #00875A; font-weight: 600; font-size: 1.1rem;">{positive_count}</span>
                <span style="color: #6B6B6B; font-size: 0.9rem;"> Positive ({positive_rate:.1f}%)</span>
            </div>
            <div style="margin: 0.5rem 0;">
                <span style="color: #DE350B; font-weight: 600; font-size: 1.1rem;">{at_risk_count}</span>
                <span style="color: #6B6B6B; font-size: 0.9rem;"> At Risk ({at_risk_rate:.1f}%)</span>
            </div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #E8E8ED; font-size: 0.85rem; color: #4A4A4A;">
                <strong>Total Engagements:</strong> {len(df_filtered):,}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    
    # At-Risk Engagements Overview - Simple and actionable
    st.markdown("### Engagements Requiring Attention")
    st.markdown("""
    <div class="help-text">
        <strong>What this shows:</strong> This table displays all engagements that need immediate attention, sorted by priority. 
        Focus on engagements with low sentiment scores (below 0.35) and those that haven't been updated recently (7+ days).
        <br><br>
        <strong>How to use:</strong> Review the top rows first—these are your highest priorities. Click through to the detailed 
        tabs below to investigate specific issues and develop action plans.
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate priority score: lower sentiment + older = higher priority
    df_priority = df_filtered.copy()
    df_priority['date'] = pd.to_datetime(df_priority['date'])
    today = df_priority['date'].max()
    df_priority['days_stale'] = (today - df_priority['date']).dt.days
    
    # Priority score: sentiment inverted (lower is worse) + staleness
    # Normalize to 0-100 scale
    df_priority['priority_score'] = (1 - df_priority['sentiment_score']) * 50 + (df_priority['days_stale'] / df_priority['days_stale'].max() * 50)
    
    # Filter to concerning engagements (sentiment < 0.55 OR stale > 7 days OR at-risk status)
    df_concerning = df_priority[
        (df_priority['sentiment_score'] < 0.55) | 
        (df_priority['days_stale'] > 7) |
        (df_priority['status'] == 'at-risk')
    ].sort_values('priority_score', ascending=False).head(10)
    
    if len(df_concerning) > 0:
        # Create display dataframe
        display_df = pd.DataFrame({
            'Customer': df_concerning['customer'],
            'Status': df_concerning['status'].str.capitalize(),
            'Sentiment': df_concerning['sentiment_score'].round(3),
            'Days Since Update': df_concerning['days_stale'].astype(int),
            'Top Issue': df_concerning['topic'],
            'Priority Score': df_concerning['priority_score'].round(1)
        })
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Sentiment": st.column_config.ProgressColumn(
                    "Sentiment",
                    help="Sentiment score from 0 (very negative) to 1 (very positive)",
                    format="%.3f",
                    min_value=0,
                    max_value=1,
                ),
                "Priority Score": st.column_config.ProgressColumn(
                    "Priority Score",
                    help="Combined priority based on sentiment and staleness (higher = more urgent)",
                    format="%.1f",
                    min_value=0,
                    max_value=100,
                ),
            }
        )
        
        st.caption(f"Showing top {len(df_concerning)} engagements that need attention out of {len(df_filtered)} total")
    else:
        st.success("All engagements are healthy—no immediate action required!")
    
    st.markdown("---")
    st.markdown("")

    # Detailed Analytics Tabs
    st.markdown("## Detailed Analytics")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Engagement Sentiment", 
        "Topics & Issues", 
        "Skills & Capabilities", 
        "Full Executive Report"
    ])

    with tab1:
        st.markdown("""
        <div class="help-text">
            <strong>About this view:</strong> Track customer sentiment across engagements. 
            Sentiment scores range from 0 (very negative) to 1 (very positive). 
            Scores above 0.55 are considered healthy, 0.35-0.55 warrant monitoring, and below 0.35 require immediate attention.
        </div>
        """, unsafe_allow_html=True)
        
        # ENHANCED: Single-row layout with improved stacked bar chart
        st.markdown("### Sentiment Overview")
        st.markdown("""
        <div style="background-color: #F5F5F7; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <strong>What this chart shows:</strong> The proportion of engagements with positive, neutral, and negative sentiment.
            <br>
            <strong>What to look for:</strong> A healthy engagement portfolio should have 60%+ positive sentiment. 
            If negative sentiment exceeds 20%, investigate the common issues in the Topics tab below.
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(plot_sentiment_distribution(df_filtered), use_container_width=True)
        
        st.markdown("")
        st.markdown("### Sentiment Trend Analysis")
        st.markdown("""
        <div style="background-color: #F5F5F7; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <span style="font-size: 0.9rem; color: #4A4A4A;">
                <strong>How to interpret:</strong> The chart shows a 7-day rolling average to smooth daily fluctuations. 
                Background zones indicate health: <span style="color: #00875A; font-weight: 600;">green=healthy</span>, 
                <span style="color: #FF991F; font-weight: 600;">yellow=warning</span>, 
                <span style="color: #DE350B; font-weight: 600;">red=danger</span>.
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(plot_sentiment_over_time(df_filtered), use_container_width=True)
        
        st.markdown("")
        st.markdown("### Recent Negative Feedback")
        st.caption("Review customer concerns to identify improvement opportunities")
        
        negative_feedback = df_filtered[df_filtered['sentiment_type'] == 'negative'][['customer', 'feedback', 'sentiment_score', 'date']].head(8)
        
        if len(negative_feedback) > 0:
            # Enhanced table display
            for idx, row in negative_feedback.iterrows():
                with st.container():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"**{row['customer']}** · {row['date']}")
                        st.markdown(f"{row['feedback'][:150]}..." if len(row['feedback']) > 150 else row['feedback'])
                    with col_b:
                        st.markdown(f"<span class='stat-badge negative'>Score: {row['sentiment_score']:.2f}</span>", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.success("No negative feedback in the current selection!")

    with tab2:
        st.markdown("""
        <div class="help-text">
            <strong>About this view:</strong> Identify the most frequently discussed topics and technical challenges 
            across customer engagements. Topics appearing frequently may indicate systemic issues requiring 
            knowledge base articles, training, or product improvements.
        </div>
        """, unsafe_allow_html=True)
        
        # Add topic concentration insight
        unique_topics = len(df_filtered['topic'].unique())
        total_engagements = len(df_filtered)
        top_topic = df_filtered['topic'].mode()[0] if len(df_filtered) > 0 else "N/A"
        top_topic_count = len(df_filtered[df_filtered['topic'] == top_topic])
        concentration_pct = (top_topic_count / total_engagements * 100) if total_engagements > 0 else 0
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("Unique Topics", unique_topics, help="Number of distinct technical topics identified")
        with col_stat2:
            st.metric("Top Topic", top_topic, help="Most frequently appearing topic")
        with col_stat3:
            st.metric("Concentration", f"{concentration_pct:.1f}%", 
                     help="Percentage of engagements involving the top topic")
        
        st.markdown("")
        
        st.markdown("""
        <div style="background-color: #F5F5F7; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <strong>What this chart shows:</strong> The most frequently discussed technical topics across all customer engagements.
            <br>
            <strong>What to look for:</strong> If one topic dominates (>30% of engagements), it may indicate a systemic issue 
            requiring a knowledge base article, product fix, or dedicated training. Topics with high frequency but low sentiment 
            are especially critical.
        </div>
        """, unsafe_allow_html=True)
        
        st.plotly_chart(plot_top_topics(df_filtered), use_container_width=True)
        
        st.markdown("")
        st.markdown("### Topic Deep Dive")
        st.caption("Explore detailed notes and engagement status for specific topics")
        
        selected_topic = st.selectbox(
            "Select a topic to view detailed notes:", 
            sorted(df_filtered['topic'].unique()),
            help="Choose a topic to see specific customer feedback and notes"
        )
        
        topic_notes = df_filtered[df_filtered['topic'] == selected_topic][['customer', 'notes', 'status']].head(6)
        
        for idx, row in topic_notes.iterrows():
            status_color = "#00875A" if row['status'] == 'healthy' else "#DE350B" if row['status'] == 'at-risk' else "#FF991F"
            st.markdown(f"""
            <div style="background-color: #F5F5F7; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.75rem; border-left: 3px solid {status_color};">
                <strong>{row['customer']}</strong> 
                <span style="background-color: {status_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem; margin-left: 0.5rem;">{row['status'].upper()}</span>
                <p style="margin-top: 0.5rem; color: #4A4A4A;">{row['notes']}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="help-text">
            <strong>About this view:</strong> Compare market demand (based on engagement frequency) versus current team proficiency. 
            <strong>How to interpret:</strong> Technologies on the right (red) show training gaps where demand exceeds team capability. 
            Technologies on the left (green) indicate surplus capacity. Focus investment on the largest rightward bars.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #F5F5F7; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <strong>What this chart shows:</strong> The gap between market demand (how often we encounter each technology) 
            and our team's current proficiency level.
            <br>
            <strong>How to read it:</strong> 
            <ul style="margin-top: 0.5rem; margin-bottom: 0;">
                <li><strong>Bars extending right (red):</strong> Training gaps—demand exceeds our capability. These are investment priorities.</li>
                <li><strong>Bars extending left (green):</strong> Surplus capacity—our team exceeds current demand.</li>
                <li><strong>Longest bars:</strong> Highest priority for training or hiring decisions.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.plotly_chart(plot_skills_gap(df_filtered), use_container_width=True)
        
        st.markdown("")
        st.markdown("### Recommended Actions")
        st.caption("Strategic priorities based on skills gap analysis")
        
        col_action1, col_action2 = st.columns(2)
        
        with col_action1:
            st.markdown("""
            <div style="background-color: #E3FCEF; padding: 1.25rem; border-radius: 0.75rem; border-left: 4px solid #00875A;">
                <h4 style="margin-top: 0; color: #00875A;">Training Priorities</h4>
                <ul style="margin-bottom: 0;">
                    <li>Schedule Unity Catalog deep-dive sessions</li>
                    <li>Structured Streaming workshop series</li>
                    <li>Auto Loader best practices training</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col_action2:
            st.markdown("""
            <div style="background-color: #E6F2FF; padding: 1.25rem; border-radius: 0.75rem; border-left: 4px solid #0065FF;">
                <h4 style="margin-top: 0; color: #0065FF;">Hiring Recommendations</h4>
                <ul style="margin-bottom: 0;">
                    <li>Terraform expertise for IaC needs</li>
                    <li>Senior governance specialist</li>
                    <li>Serverless architecture experience</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("### Weekly Executive Briefing")
        st.caption("AI-generated strategic summary for leadership review")
        st.markdown("")
        
        st.markdown(f"""
        <div class="insight-card">
            <pre style="
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
                font-size: 1rem; 
                white-space: pre-wrap; 
                color: var(--color-text-primary); 
                line-height: 1.75;
                margin: 0;
                background: none;
            ">{summary}</pre>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("### Next Steps")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF4E5 0%, #FFF 100%); padding: 1.5rem; border-radius: 0.75rem; border-left: 5px solid #FF991F;">
            <ol style="margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.5rem;"><strong>Training:</strong> Schedule Unity Catalog and Streaming deep-dive sessions with high-engagement teams</li>
                <li style="margin-bottom: 0.5rem;"><strong>Hiring:</strong> Prioritize candidates with Terraform, governance, and serverless experience</li>
                <li style="margin-bottom: 0.5rem;"><strong>Process:</strong> Review and streamline onboarding checklist to reduce configuration friction</li>
                <li style="margin-bottom: 0.5rem;"><strong>Follow-up:</strong> Schedule 1:1s with at-risk engagement owners to develop recovery plans</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
