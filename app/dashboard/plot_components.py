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

# Improved layout with better readability
COMMON_LAYOUT = {
    "template": "plotly_white",
    "font": {"size": 15, "family": "Arial, sans-serif", "color": "#1D1D1F"},
    "title_font": {"size": 20, "family": "Arial, sans-serif", "color": "#1D1D1F"},
    "legend_font": {"size": 14},
    "margin": {"l": 60, "r": 40, "t": 80, "b": 60},
    "hoverlabel": {
        "bgcolor": "white",
        "font_size": 14,
        "font_family": "Arial, sans-serif"
    }
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
        hole=0.4  # Donut chart for modern look
    )
    
    fig.update_layout(**COMMON_LAYOUT)
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    # Enhanced text display with percentages inside slices
    fig.update_traces(
        textinfo='percent+label', 
        textfont_size=16,
        textposition='inside',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    return fig

def plot_top_topics(df):
    """
    Plots the top topics extracted from engagements.
    """
    topic_counts = df['topic'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    topic_counts = topic_counts.head(10)  # Limit to top 10 for clarity
    topic_counts = topic_counts.sort_values(by='Count', ascending=True)
    
    fig = px.bar(
        topic_counts, 
        x='Count', 
        y='Topic', 
        orientation='h', 
        title='Top 10 Engagement Topics',
        text='Count'  # Show values on bars
    )
    
    # Apply consistent color
    fig.update_traces(
        marker_color=COLORS['primary'],
        textposition='outside',
        textfont_size=14,
        hovertemplate='<b>%{y}</b><br>Engagements: %{x}<extra></extra>'
    )
    
    fig.update_layout(**COMMON_LAYOUT)
    fig.update_layout(
        xaxis_title="Number of Engagements",
        yaxis_title="Topic",
        yaxis={'categoryorder': 'total ascending'},
        height=500  # Taller for better readability
    )
    
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
        title='Sentiment Trend Over Time (7-Day Average)',
        markers=True
    )
    
    fig.update_traces(
        line_color=COLORS['primary'], 
        line_width=3, 
        marker_size=8,
        hovertemplate='<b>Date:</b> %{x|%b %d, %Y}<br><b>Sentiment Score:</b> %{y:.2f}<extra></extra>'
    )
    
    fig.update_layout(**COMMON_LAYOUT)
    fig.update_layout(
        yaxis_title="Sentiment Score (0-1 scale)",
        xaxis_title="Date",
        yaxis_range=[-0.1, 1.1],  # Fixed range for context
        shapes=[
            # Add neutral reference line at 0.5
            dict(
                type='line',
                xref='paper',
                x0=0,
                x1=1,
                yref='y',
                y0=0.5,
                y1=0.5,
                line=dict(color='#999999', width=2, dash='dash')
            )
        ],
        annotations=[
            dict(
                x=0.02,
                y=0.52,
                xref='paper',
                yref='y',
                text='Neutral',
                showarrow=False,
                font=dict(size=12, color='#999999')
            )
        ]
    )
    
    return fig

def plot_skills_gap(df):
    """
    Plots a skills gap analysis comparing market demand vs. team proficiency.
    """
    # Flatten technologies list
    all_techs = [tech for sublist in df['technologies'] for tech in sublist]
    tech_counts = pd.Series(all_techs).value_counts().reset_index()
    tech_counts.columns = ['Technology', 'Engagement_Count']
    tech_counts = tech_counts.head(10)  # Top 10 technologies
    
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
    
    # Calculate gap (positive means we need more training)
    tech_counts['Gap'] = tech_counts['Demand_Score'] - tech_counts['Team_Proficiency']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=tech_counts['Technology'],
        y=tech_counts['Demand_Score'],
        name='Market Demand',
        marker_color=COLORS['secondary'],
        text=tech_counts['Demand_Score'].round(0),
        textposition='outside',
        texttemplate='%{text:.0f}',
        hovertemplate='<b>%{x}</b><br>Demand Score: %{y:.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=tech_counts['Technology'],
        y=tech_counts['Team_Proficiency'],
        name='Team Proficiency',
        marker_color=COLORS['primary'],
        text=tech_counts['Team_Proficiency'].round(0),
        textposition='outside',
        texttemplate='%{text:.0f}',
        hovertemplate='<b>%{x}</b><br>Proficiency: %{y:.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Skills Gap Analysis: Market Demand vs. Team Proficiency',
        barmode='group',
        xaxis_tickangle=-45,
        yaxis_title="Score (0-100)",
        xaxis_title="Technology",
        height=550,
        **COMMON_LAYOUT
    )
    
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig
