from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel

class Engagement(BaseModel):
    id: str
    customer: str
    date: str
    notes: str
    feedback: Optional[str] = ""
    status: Optional[str] = "unknown"
    # Allow extra fields
    class Config:
        extra = "allow"

class AnalyzeRequest(BaseModel):
    engagement_ids: Optional[List[str]] = None
    raw_logs: Optional[str] = None

class SentimentResult(BaseModel):
    sentiment_type: str
    sentiment_score: float

class TopicResult(BaseModel):
    topic: str
    confidence: float

class EngagementResult(BaseModel):
    id: str
    customer: str
    sentiment: SentimentResult
    topic: TopicResult
    cluster_id: Optional[int] = None

class AnalysisReport(BaseModel):
    summary: str
    clusters: List[Dict[str, Any]]
    fixes: List[str]
    tuning_params: List[str]
    plotly_data: Dict[str, Any] # Map of plot_id -> figure dict
    notebook_markdown: str

class NotebookCommitRequest(BaseModel):
    notebook_path: str
    markdown: str
