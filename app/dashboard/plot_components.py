import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Color-blind friendly palette (Okabe-Ito inspired) with semantic meaning
COLORS = {
    'positive': '#009E73',  # Green - success, healthy
    'neutral': '#999999',   # Grey - stable, neutral
    'negative': '#D55E00',  # Vermilion - danger, needs attention
    'primary': '#0072B2',   # Blue - information, neutral data
    'secondary': '#E69F00', # Orange - warning, demand
    'tertiary': '#56B4E9',  # Sky Blue - secondary info
    'gap_positive': '#009E73',  # Surplus (team exceeds demand)
    'gap_negative': '#D55E00',  # Deficit (demand exceeds team)
}

# Semantic zones for sentiment scoring
SENTIMENT_ZONES = {
    'danger': {'range': [0, 0.35], 'color': '#FFEBE6', 'border': '#DE350B'},
    'warning': {'range': [0.35, 0.55], 'color': '#FFF4E5', 'border': '#FF991F'},
    'healthy': {'range': [0.55, 1.0], 'color': '#E3FCEF', 'border': '#00875A'}
}

# Improved layout with better readability
COMMON_LAYOUT = {
    "template": "plotly_white",
    "font": {"size": 16, "family": "Arial, sans-serif", "color": "#1D1D1F"},  # Increased from 15
    "title_font": {"size": 20, "family": "Arial, sans-serif", "color": "#1D1D1F", "weight": 600},
    "legend_font": {"size": 14},
    "margin": {"l": 60, "r": 40, "t": 80, "b": 60},
    "hoverlabel": {
        "bgcolor": "white",
        "font_size": 15,
        "font_family": "Arial, sans-serif",
        "bordercolor": "#E8E8ED"
    },
    "plot_bgcolor": "white",
    "paper_bgcolor": "white",
}

def plot_sentiment_distribution(df):
    """
    REDESIGNED: Horizontal stacked bar instead of pie chart.
    
    Why this is better:
    - Easier to compare exact proportions (length vs. angle/area)
    - More accessible on mobile devices
    - Can add direct labels without overlap
    - Better for colorblind users
    - Easier to see small categories
    
    Research: Cleveland & McGill (1984) showed bar length is decoded 
    2-3x more accurately than pie slice angles.
    """
    sentiment_counts = df['sentiment_type'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    
    total = sentiment_counts['Count'].sum()
    sentiment_counts['Percentage'] = (sentiment_counts['Count'] / total * 100).round(1)
    
    # Sort by sentiment type for consistent ordering
    order = ['positive', 'neutral', 'negative']
    sentiment_counts['Sentiment'] = pd.Categorical(sentiment_counts['Sentiment'], categories=order, ordered=True)
    sentiment_counts = sentiment_counts.sort_values('Sentiment')
    
    fig = go.Figure()
    
    # Create stacked horizontal bar
    cumulative = 0
    for _, row in sentiment_counts.iterrows():
        percentage = row['Percentage']
        sentiment = row['Sentiment']
        count = row['Count']
        
        fig.add_trace(go.Bar(
            name=sentiment.capitalize(),
            y=['Sentiment Distribution'],
            x=[percentage],
            orientation='h',
            marker_color=COLORS.get(sentiment, COLORS['neutral']),
            text=f"{sentiment.capitalize()}<br>{count} ({percentage}%)",
            textposition='inside',
            textfont=dict(size=15, color='white', family='Arial, sans-serif'),
            hovertemplate=f'<b>{sentiment.capitalize()}</b><br>Count: {count}<br>Percentage: {percentage}%<extra></extra>',
            insidetextanchor='middle'
        ))
    
    fig.update_layout(
        title='Engagement Sentiment Distribution',
        barmode='stack',
        showlegend=True,
        height=180,
        **COMMON_LAYOUT
    )
    
    fig.update_layout(
        xaxis=dict(
            title="Percentage (%)",
            showgrid=False,
            range=[0, 100]
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5
        ),
        margin={"l": 20, "r": 20, "t": 60, "b": 60}
    )
    
    return fig

def plot_top_topics(df):
    """
    Enhanced horizontal bar chart with direct labels and priority sorting.
    
    Improvements:
    - Sorted by frequency (most important first)
    - Direct labels reduce cognitive load
    - Color intensity shows relative importance
    - Clear axis labels with units
    """
    topic_counts = df['topic'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    topic_counts = topic_counts.head(10)  # Top 10 for clarity
    topic_counts = topic_counts.sort_values(by='Count', ascending=True)  # Ascending for horizontal
    
    # Calculate percentage for context
    total_engagements = len(df)
    topic_counts['Percentage'] = (topic_counts['Count'] / total_engagements * 100).round(1)
    
    # Create color gradient based on frequency
    max_count = topic_counts['Count'].max()
    colors = [f'rgba(0, 114, 178, {0.4 + (count/max_count)*0.6})' for count in topic_counts['Count']]
    
    fig = px.bar(
        topic_counts, 
        x='Count', 
        y='Topic', 
        orientation='h', 
        title='Top 10 Engagement Topics',
        text='Count'
    )
    
    # Customize bars with gradient and labels
    fig.update_traces(
        marker_color=colors,
        texttemplate='%{text} <span style="color:#6B6B6B;">(%{customdata}%)</span>',
        textposition='outside',
        textfont=dict(size=14, color='#1D1D1F'),
        customdata=topic_counts['Percentage'],
        hovertemplate='<b>%{y}</b><br>Engagements: %{x}<br>Percentage: %{customdata}%<extra></extra>',
        marker_line_width=0
    )
    
    fig.update_layout(**COMMON_LAYOUT)
    fig.update_layout(
        xaxis_title="Number of Engagements",
        yaxis_title="",
        yaxis={'categoryorder': 'total ascending'},
        height=500,
        xaxis=dict(showgrid=True, gridcolor='#F0F0F0', gridwidth=1)
    )
    
    return fig

def plot_sentiment_over_time(df):
    """
    ENHANCED: Sentiment trend with context zones and reference lines.
    
    Key improvements:
    - Background zones (danger/warning/healthy) for instant interpretation
    - Reference line at neutral (0.5) with annotation
    - 7-day rolling average to reduce noise
    - Clear visual hierarchy
    
    Why zones matter: Pre-attentive processing allows users to see 
    "good" vs "bad" instantly without reading numbers.
    """
    # Ensure date is datetime and sort
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Calculate rolling average
    df['rolling_sentiment'] = df['sentiment_score'].rolling(window=7, min_periods=1).mean()
    
    fig = go.Figure()
    
    # Add background zones (bottom to top)
    # Danger zone (0 - 0.35)
    fig.add_hrect(
        y0=0, y1=0.35,
        fillcolor=SENTIMENT_ZONES['danger']['color'],
        layer="below",
        line_width=0,
        annotation_text="Danger Zone",
        annotation_position="left",
        annotation=dict(font_size=11, font_color="#6B6B6B")
    )
    
    # Warning zone (0.35 - 0.55)
    fig.add_hrect(
        y0=0.35, y1=0.55,
        fillcolor=SENTIMENT_ZONES['warning']['color'],
        layer="below",
        line_width=0,
        annotation_text="Warning",
        annotation_position="left",
        annotation=dict(font_size=11, font_color="#6B6B6B")
    )
    
    # Healthy zone (0.55 - 1.0)
    fig.add_hrect(
        y0=0.55, y1=1.0,
        fillcolor=SENTIMENT_ZONES['healthy']['color'],
        layer="below",
        line_width=0,
        annotation_text="Healthy",
        annotation_position="left",
        annotation=dict(font_size=11, font_color="#6B6B6B")
    )
    
    # Add sentiment line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['rolling_sentiment'],
        mode='lines+markers',
        name='7-Day Average',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8, color=COLORS['primary'], line=dict(width=2, color='white')),
        hovertemplate='<b>Date:</b> %{x|%b %d, %Y}<br><b>Sentiment:</b> %{y:.3f}<extra></extra>',
        fill='tonexty'
    ))
    
    fig.update_layout(**COMMON_LAYOUT)
    fig.update_layout(
        title='Sentiment Trend Over Time (7-Day Average)',
        yaxis_title="Sentiment Score",
        xaxis_title="Date",
        yaxis=dict(
            range=[0, 1.0],
            tickmode='linear',
            tick0=0,
            dtick=0.2,
            showgrid=True,
            gridcolor='#E8E8ED'
        ),
        xaxis=dict(
            showgrid=False
        ),
        height=400,
        showlegend=False,
        margin=dict(l=80, r=40, t=80, b=60)
    )
    
    # Add neutral reference line
    fig.add_hline(
        y=0.5,
        line_dash="dash",
        line_color="#999999",
        line_width=2,
        annotation_text="Neutral (0.5)",
        annotation_position="right",
        annotation=dict(font_size=12, font_color="#999999")
    )
    
    return fig

def plot_skills_gap(df):
    """
    REDESIGNED: Diverging bar chart to show skills gap analysis.
    
    Why diverging bars are superior:
    - Shows gap magnitude AND direction in one visual
    - Zero baseline makes it obvious which skills need investment
    - Sorted by gap size highlights priorities
    - Color coding reinforces meaning (red=deficit, green=surplus)
    
    Key insight: This chart answers "Where should we invest?" at a glance.
    """
    # Flatten technologies list
    all_techs = [tech for sublist in df['technologies'] for tech in sublist]
    tech_counts = pd.Series(all_techs).value_counts().reset_index()
    tech_counts.columns = ['Technology', 'Engagement_Count']
    tech_counts = tech_counts.head(10)
    
    # Mock team proficiency (0-100)
    # In production, this would come from skills database
    mock_proficiency = {
        "Delta Lake": 85, "Auto Loader": 40, "PySpark": 90, "Unity Catalog": 30, 
        "Databricks SQL": 70, "MLflow": 60, "Structured Streaming": 50, 
        "Photon": 45, "Serverless": 35, "Terraform": 25
    }
    
    tech_counts['Team_Proficiency'] = tech_counts['Technology'].map(mock_proficiency).fillna(50)
    
    # Normalize engagement count to 0-100 scale
    max_count = tech_counts['Engagement_Count'].max()
    tech_counts['Demand_Score'] = (tech_counts['Engagement_Count'] / max_count) * 100
    
    # Calculate gap: POSITIVE = need more training (demand > proficiency)
    # NEGATIVE = team exceeds demand (surplus capacity)
    tech_counts['Gap'] = tech_counts['Demand_Score'] - tech_counts['Team_Proficiency']
    
    # Sort by gap magnitude (largest needs first)
    tech_counts = tech_counts.sort_values('Gap', ascending=True)
    
    # Color code based on gap
    colors = [COLORS['gap_negative'] if gap > 0 else COLORS['gap_positive'] 
              for gap in tech_counts['Gap']]
    
    fig = go.Figure()
    
    # Create diverging bar chart
    fig.add_trace(go.Bar(
        y=tech_counts['Technology'],
        x=tech_counts['Gap'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(width=0)
        ),
        text=[f"{abs(gap):.0f}" for gap in tech_counts['Gap']],
        textposition='outside',
        textfont=dict(size=14, color='#1D1D1F'),
        hovertemplate='<b>%{y}</b><br>' +
                      'Gap: %{x:.0f}<br>' +
                      '<i>Demand: %{customdata[0]:.0f} | Proficiency: %{customdata[1]:.0f}</i>' +
                      '<extra></extra>',
        customdata=tech_counts[['Demand_Score', 'Team_Proficiency']].values,
        showlegend=False
    ))
    
    # Add zero reference line
    fig.add_vline(
        x=0,
        line_width=3,
        line_color="#1D1D1F",
        layer="below"
    )
    
    fig.update_layout(
        title='Skills Gap Analysis: Training Priorities',
        xaxis_title="← Team Exceeds Demand  |  Gap Score  |  Training Needed →",
        yaxis_title="",
        height=550,
        **COMMON_LAYOUT
    )
    
    fig.update_layout(
        xaxis=dict(
            zeroline=True,
            zerolinewidth=3,
            zerolinecolor='#1D1D1F',
            showgrid=True,
            gridcolor='#F0F0F0'
        ),
        yaxis=dict(
            categoryorder='array',
            categoryarray=tech_counts['Technology']
        ),
        margin=dict(l=150, r=100, t=80, b=80)
    )
    
    # Add annotations explaining the chart
    fig.add_annotation(
        x=max(tech_counts['Gap']) * 0.7,
        y=len(tech_counts) - 0.5,
        text="<b>Priority: Invest in training</b>",
        showarrow=False,
        font=dict(size=11, color=COLORS['gap_negative']),
        bgcolor=SENTIMENT_ZONES['danger']['color'],
        borderpad=8,
        borderwidth=1,
        bordercolor=COLORS['gap_negative']
    )
    
    if min(tech_counts['Gap']) < 0:
        fig.add_annotation(
            x=min(tech_counts['Gap']) * 0.7,
            y=0.5,
            text="<b>Surplus capacity</b>",
            showarrow=False,
            font=dict(size=11, color=COLORS['gap_positive']),
            bgcolor=SENTIMENT_ZONES['healthy']['color'],
            borderpad=8,
            borderwidth=1,
            bordercolor=COLORS['gap_positive']
        )
    
    return fig


def plot_engagement_health_matrix(df):
    """
    NEW: Priority matrix plotting engagements by sentiment vs. recency.
    
    Purpose: Help users identify which engagements need immediate attention.
    - X-axis: Sentiment (low = needs help)
    - Y-axis: Days since last update (high = stale, risky)
    - Size: Engagement value/importance (if available)
    - Color: Status (at-risk, warning, healthy)
    
    This creates a visual quadrant:
    - Top-left: URGENT (low sentiment + stale)
    - Bottom-right: GOOD (high sentiment + recent)
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    today = df['date'].max()
    df['days_since_update'] = (today - df['date']).dt.days
    
    # Color map for status
    status_colors = {
        'at-risk': COLORS['negative'],
        'warning': COLORS['secondary'],
        'healthy': COLORS['positive']
    }
    
    df['color'] = df['status'].map(status_colors)
    
    fig = go.Figure()
    
    for status in df['status'].unique():
        df_status = df[df['status'] == status]
        
        fig.add_trace(go.Scatter(
            x=df_status['sentiment_score'],
            y=df_status['days_since_update'],
            mode='markers',
            name=status.capitalize(),
            marker=dict(
                size=12,
                color=status_colors.get(status, COLORS['neutral']),
                line=dict(width=1, color='white'),
                opacity=0.8
            ),
            text=df_status['customer'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Sentiment: %{x:.2f}<br>' +
                         'Days since update: %{y}<br>' +
                         'Status: ' + status +
                         '<extra></extra>'
        ))
    
    # Add quadrant lines
    fig.add_hline(y=7, line_dash="dash", line_color="#999999", opacity=0.5)
    fig.add_vline(x=0.5, line_dash="dash", line_color="#999999", opacity=0.5)
    
    # Add quadrant labels
    fig.add_annotation(x=0.25, y=df['days_since_update'].max() * 0.9,
                      text="<b>URGENT</b><br>Low sentiment + Stale",
                      showarrow=False, font=dict(size=11, color="#DE350B"),
                      bgcolor="#FFEBE6", borderpad=6)
    
    fig.add_annotation(x=0.75, y=df['days_since_update'].max() * 0.9,
                      text="<b>MONITOR</b><br>Good sentiment but stale",
                      showarrow=False, font=dict(size=11, color="#FF991F"),
                      bgcolor="#FFF4E5", borderpad=6)
    
    fig.add_annotation(x=0.25, y=2,
                      text="<b>RECOVERY</b><br>Recent but struggling",
                      showarrow=False, font=dict(size=11, color="#FF991F"),
                      bgcolor="#FFF4E5", borderpad=6)
    
    fig.add_annotation(x=0.75, y=2,
                      text="<b>HEALTHY</b><br>Good sentiment + Active",
                      showarrow=False, font=dict(size=11, color="#00875A"),
                      bgcolor="#E3FCEF", borderpad=6)
    
    fig.update_layout(
        title='Engagement Health Matrix: Priority Identification',
        xaxis_title="Sentiment Score (0 = Poor, 1 = Excellent)",
        yaxis_title="Days Since Last Update",
        height=500,
        **COMMON_LAYOUT
    )
    
    fig.update_layout(
        xaxis=dict(range=[-0.05, 1.05], showgrid=True, gridcolor='#F0F0F0'),
        yaxis=dict(showgrid=True, gridcolor='#F0F0F0'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig
