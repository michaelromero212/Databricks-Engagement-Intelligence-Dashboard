import pytest
from app.inference import InferenceEngine
from app.schemas import AnalysisReport

@pytest.fixture
def sample_engagements():
    return [
        {"id": "1", "customer": "A", "notes": "We are having issues with slow shuffle performance in Spark.", "date": "2023-01-01"},
        {"id": "2", "customer": "B", "notes": "Unity Catalog permissions are confusing.", "date": "2023-01-02"},
        {"id": "3", "customer": "C", "notes": "Great success with Delta Live Tables.", "date": "2023-01-03"}
    ]

def test_analyze_engagements_structure(sample_engagements):
    engine = InferenceEngine()
    # Mock loading to avoid heavy download in tests
    engine.models_loaded = True 
    
    report = engine.analyze_engagements(sample_engagements)
    
    assert isinstance(report, AnalysisReport)
    assert len(report.plotly_data) == 3
    assert "Performance" in str(report.plotly_data) or "Governance" in str(report.plotly_data)
    assert len(report.fixes) > 0

def test_sentiment_fallback():
    engine = InferenceEngine()
    res = engine._get_sentiment("I love this!")
    assert res['sentiment_type'] == 'positive'
    assert res['sentiment_score'] > 0
