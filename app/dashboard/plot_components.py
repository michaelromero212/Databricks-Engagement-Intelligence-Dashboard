import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Color-blind friendly palette (Okabe-Ito inspired)
COLORS = {
    'positive': '#009E73',  # Green
    'neutral': '#999999',   # Grey
    'negative': '#D55E00',  # Vermilion
    'primary': '#0072B2',   # Blue
    'secondary': '#E69F00', # Orange
    'tertiary': '#56B4E9'   # Sky Blue
}

COMMON_LAYOUT = {
    "template": "plotly_white",
    "font": {"size": 14, "family": "Arial, sans-serif"},
    "title_font": {"size": 18},
    "legend_font": {"size": 14}
}

def plot_sentiment_distribution(df):
    """
    Plots the distribution of sentiment types.
    """
    sentiment_counts = df['sentiment_type'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    
    fig = px.pie(
        sentiment_counts, 
        values='Count', 
        names='Sentiment', 
        title='Engagement Sentiment Distribution',
        color='Sentiment',
        color_discrete_map={
            'positive': COLORS['positive'],
            'neutral': COLORS['neutral'],
            'negative': COLORS['negative']
        },
        hole=0.4
    )
    fig.update_layout(**COMMON_LAYOUT)
    fig.update_traces(textinfo='percent+label', textfont_size=14)
    return fig

def plot_top_topics(df):
    """
    Plots the top topics extracted from engagements.
    """
    topic_counts = df['topic'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    topic_counts = topic_counts.sort_values(by='Count', ascending=True)
    
    fig = px.bar(
        topic_counts, 
        x='Count', 
        y='Topic', 
        orientation='h', 
        title='Top Engagement Topics',
        color='Count',
        color_continuous_scale='Blues' # Sequential scales are usually safe, but let's stick to simple
    )
    fig.update_traces(marker_color=COLORS['primary'])
    fig.update_layout(**COMMON_LAYOUT)
    return fig

def plot_sentiment_over_time(df):
    """
    Plots sentiment score over time.
    """
    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Calculate rolling average
    df['rolling_sentiment'] = df['sentiment_score'].rolling(window=7, min_periods=1).mean()
    
    fig = px.line(
        df, 
        x='date', 
        y='rolling_sentiment', 
        title='Sentiment Trend (7-Day Rolling Avg)',
        markers=True
    )
    fig.update_traces(line_color=COLORS['primary'], line_width=3, marker_size=8)
    fig.update_layout(**COMMON_LAYOUT, yaxis_title="Sentiment Score")
    return fig

def plot_skills_gap(df):
    """
    Plots a mock skills gap analysis.
    """
    # Flatten technologies list
    all_techs = [tech for sublist in df['technologies'] for tech in sublist]
    tech_counts = pd.Series(all_techs).value_counts().reset_index()
    tech_counts.columns = ['Technology', 'Engagement_Count']
    
    # Mock team proficiency (0-100)
    mock_proficiency = {
        "Delta Lake": 85, "Auto Loader": 40, "PySpark": 90, "Unity Catalog": 30, 
        "Databricks SQL": 70, "MLflow": 60, "Structured Streaming": 50, 
        "Photon": 45, "Serverless": 35, "Terraform": 25
    }
    
    tech_counts['Team_Proficiency'] = tech_counts['Technology'].map(mock_proficiency).fillna(50)
    
    # Normalize engagement count to 0-100 scale for comparison
    max_count = tech_counts['Engagement_Count'].max()
    tech_counts['Demand_Score'] = (tech_counts['Engagement_Count'] / max_count) * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=tech_counts['Technology'],
        y=tech_counts['Demand_Score'],
        name='Market Demand (Engagements)',
        marker_color=COLORS['secondary']
    ))
    
    fig.add_trace(go.Bar(
        x=tech_counts['Technology'],
        y=tech_counts['Team_Proficiency'],
        name='Team Proficiency',
        marker_color=COLORS['primary']
    ))
    
    fig.update_layout(
        title='Skills Gap Analysis: Demand vs. Proficiency',
        barmode='group',
        xaxis_tickangle=-45,
        **COMMON_LAYOUT
    )
    
    return fig
