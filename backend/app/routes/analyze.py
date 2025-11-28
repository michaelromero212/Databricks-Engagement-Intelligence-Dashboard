from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List, Optional
import json
import os
import pandas as pd
from datetime import datetime, timedelta

router = APIRouter()

def load_processed_data():
    """Load processed analytics data"""
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "sample_data", "engagements_sample.json")
    
    # Check if processed data exists
    processed_path = "../data/processed/analytics_results.json"
    if os.path.exists(processed_path):
        with open(processed_path, 'r') as f:
            return json.load(f)
    
    # Otherwise load and process raw sample
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Sample data not found at {data_path}")
    
    with open(data_path, 'r') as f:
        raw_engagements = json.load(f)
    
    # Quick processing to add missing fields
    for eng in raw_engagements:
        if 'sentiment' not in eng:
            # Simple sentiment heuristic
            notes = eng.get('notes', '').lower()
            if 'great' in notes or 'success' in notes:
                eng['sentiment'] = {'sentiment_type': 'positive', 'sentiment_score': 0.7}
            elif 'issue' in notes or 'problem' in notes:
                eng['sentiment'] = {'sentiment_type': 'negative', 'sentiment_score': 0.3}
            else:
                eng['sentiment'] = {'sentiment_type': 'neutral', 'sentiment_score': 0.5}
        
        if 'topic' not in eng:
            # Simple topic extraction
            notes = eng.get('notes', '').lower()
            if 'streaming' in notes:
                eng['topic'] = {'topic': 'streaming', 'confidence': 0.8}
            elif 'unity' in notes or 'governance' in notes:
                eng['topic'] = {'topic': 'governance', 'confidence': 0.8}
            elif 'performance' in notes:
                eng['topic'] = {'topic': 'performance', 'confidence': 0.8}
            else:
                eng['topic'] = {'topic': 'general', 'confidence': 0.6}
    
    return {
        'engagements': raw_engagements,
        'weekly_summary': 'Analysis of customer engagements showing trends and insights.'
    }

@router.get("/dashboard/data")
async def get_dashboard_data():
    """Get all dashboard data including engagements and analytics"""
    try:
        data = load_processed_data()
        
        engagements = data['engagements']
        df = pd.DataFrame(engagements)
        
        # Flatten nested fields
        df['sentiment_type'] = df['sentiment'].apply(lambda x: x.get('sentiment_type') if isinstance(x, dict) else 'neutral')
        df['sentiment_score'] = df['sentiment'].apply(lambda x: x.get('sentiment_score') if isinstance(x, dict) else 0.5)
        df['topic'] = df['topic'].apply(lambda x: x.get('topic') if isinstance(x, dict) else 'general')
        
        # Calculate KPIs
        total_engagements = len(df)
        avg_sentiment = float(df['sentiment_score'].mean())
        positive_count = int(len(df[df['sentiment_type'] == 'positive']))
        at_risk_count = int(len(df[df['status'] == 'at-risk']))
        
        # Sentiment distribution
        sentiment_counts = df['sentiment_type'].value_counts().to_dict()
        
        # Top topics
        topic_counts = df['topic'].value_counts().head(10).to_dict()
        
        # Sentiment over time
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        sentiment_by_date = df.groupby('date')['sentiment_score'].mean().reset_index()
        sentiment_timeline = [
            {'date': str(row['date'].date()), 'sentiment': float(row['sentiment_score'])}
            for _, row in sentiment_by_date.iterrows()
        ]
        
        return {
            'kpis': {
                'total_engagements': total_engagements,
                'avg_sentiment': round(avg_sentiment, 2),
                'positive_count': positive_count,
                'at_risk_count': at_risk_count
            },
            'sentiment_distribution': sentiment_counts,
            'top_topics': topic_counts,
            'sentiment_timeline': sentiment_timeline,
            'engagements': engagements[:20],  # Return subset for detail view
            'summary': data.get('weekly_summary', 'No summary available')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/engagements/recent")
async def get_recent_engagements(page: int = 1, page_size: int = 20):
    """Get recent engagements with pagination"""
    try:
        data = load_processed_data()
        engagements = data['engagements']
        start = (page - 1) * page_size
        end = start + page_size
        return engagements[start:end]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

