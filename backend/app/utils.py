import logging
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Plotting Helpers (Adapted from app/dashboard/plot_components.py) ---

COLORS = {
    'primary': '#2962FF',  # Databricks Blue
    'secondary': '#FF991F', # Warning Orange
    'positive': '#00875A', # Success Green
    'negative': '#DE350B', # Danger Red
    'neutral': '#42526E',  # Neutral Grey
    'background': '#FFFFFF',
    'text': '#172B4D',
    'gap_positive': '#00875A',
    'gap_negative': '#DE350B'
}

COMMON_LAYOUT = dict(
    font=dict(family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif", color=COLORS['text']),
    plot_bgcolor=COLORS['background'],
    paper_bgcolor=COLORS['background'],
    margin=dict(l=40, r=40, t=60, b=40),
    showlegend=True
)

def plot_top_topics(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {}
        
    topic_counts = df['topic'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    
    # Calculate average sentiment per topic
    topic_sentiment = df.groupby('topic')['sentiment_score'].mean().reset_index()
    topic_counts = topic_counts.merge(topic_sentiment, left_on='Topic', right_on='topic')
    
    fig = px.bar(
        topic_counts,
        x='Count',
        y='Topic',
        orientation='h',
        color='sentiment_score',
        color_continuous_scale=['#DE350B', '#FF991F', '#00875A'],
        range_color=[-0.5, 0.5],
        title='Top Technical Topics by Frequency & Sentiment'
    )
    
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=400,
        **COMMON_LAYOUT
    )
    
    return fig.to_dict()

def plot_skills_gap(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {}
        
    # Mock demand vs capacity logic for demo
    # In reality, this would come from a skills database
    
    tech_stack = df['topic'].unique()
    
    data = []
    for tech in tech_stack:
        demand = len(df[df['topic'] == tech])
        # Mock capacity: random but consistent for same tech
        capacity = max(1, demand + (hash(tech) % 5 - 2)) 
        gap = demand - capacity
        
        data.append({
            'Technology': tech,
            'Demand': demand,
            'Capacity': capacity,
            'Gap': gap
        })
    
    tech_counts = pd.DataFrame(data).sort_values('Gap', ascending=True)
    
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        y=tech_counts['Technology'],
        x=tech_counts['Gap'],
        orientation='h',
        marker=dict(
            color=tech_counts['Gap'].apply(lambda x: COLORS['gap_negative'] if x > 0 else COLORS['gap_positive']),
            showscale=False
        ),
        text=tech_counts['Gap'].apply(lambda x: f"Need {x}" if x > 0 else f"Surplus {abs(x)}"),
        textposition='auto',
        showlegend=False
    ))
    
    fig.add_vline(x=0, line_width=2, line_color="#1D1D1F")
    
    fig.update_layout(
        title='Skills Gap Analysis: Demand vs Capacity',
        xaxis_title="Surplus Capacity <--- | ---> Training Needed",
        height=500,
        **COMMON_LAYOUT
    )
    
    return fig.to_dict()

def plot_sentiment_time_series(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {}
        
    df['date'] = pd.to_datetime(df['date'])
    daily_sentiment = df.groupby('date')['sentiment_score'].mean().reset_index()
    
    fig = px.line(
        daily_sentiment,
        x='date',
        y='sentiment_score',
        title='Sentiment Trend Over Time',
        markers=True
    )
    
    fig.update_traces(line_color=COLORS['primary'], line_width=3)
    fig.update_layout(
        yaxis_range=[-1, 1],
        height=350,
        **COMMON_LAYOUT
    )
    
    return fig.to_dict()
