import os
import json
import logging
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Generator
from app.config import settings
from app.schemas import AnalysisReport
from app.utils import plot_top_topics, plot_skills_gap, plot_sentiment_time_series

# ML Imports
try:
    from textblob import TextBlob
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.feature_extraction.text import TfidfVectorizer
    import torch
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    print(f"Warning: ML dependencies missing: {e}")

logger = logging.getLogger(__name__)

class InferenceEngine:
    def __init__(self):
        self.mode = settings.MODEL_MODE
        self.hf_api_key = settings.HUGGINGFACE_API_KEY
        self.models_loaded = False
        self.sentiment_pipeline = None
        self.embedding_model = None
        self.summarizer_model = None
        self.summarizer_tokenizer = None
        
    def load_models(self):
        if self.models_loaded:
            return

        logger.info(f"Loading models in {self.mode} mode...")
        
        # 1. Sentiment
        try:
            # Try lightweight local first
            self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        except Exception as e:
            logger.warning(f"Failed to load sentiment model, falling back to TextBlob: {e}")
            self.sentiment_pipeline = None # Fallback to TextBlob

        # 2. Embeddings (Local is usually fine for MiniLM)
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self.embedding_model = None

        # 3. Summarization / Generation
        if self.mode == 'local' or self.mode == 'auto':
            try:
                model_name = "google/flan-t5-small"
                self.summarizer_tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.summarizer_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            except Exception as e:
                logger.warning(f"Failed to load local generation model: {e}. Switching to API/Fallback.")
                if self.mode == 'auto' and self.hf_api_key:
                    self.mode = 'huggingface_api'
        
        self.models_loaded = True
        logger.info("Models loaded.")

    def _get_sentiment(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"sentiment_type": "neutral", "sentiment_score": 0.0}
            
        if self.sentiment_pipeline:
            try:
                # Truncate to 512 tokens approx
                result = self.sentiment_pipeline(text[:2000])[0]
                score = result['score'] if result['label'] == 'POSITIVE' else -result['score']
                return {
                    "sentiment_type": result['label'].lower(),
                    "sentiment_score": score
                }
            except Exception:
                pass
        
        # Fallback
        blob = TextBlob(text)
        score = blob.sentiment.polarity
        stype = "positive" if score > 0.1 else "negative" if score < -0.1 else "neutral"
        return {"sentiment_type": stype, "sentiment_score": score}

    def _generate_text(self, prompt: str) -> str:
        # Local
        if self.summarizer_model:
            inputs = self.summarizer_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.summarizer_model.generate(**inputs, max_new_tokens=100)
            return self.summarizer_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # API (Mock implementation for now if no key)
        if self.mode == 'huggingface_api' and self.hf_api_key:
            # Call HF API (omitted for brevity, assume requests)
            pass
            
        # Fallback heuristic
        return "Analysis generated (Fallback): Check logs for details."

    def analyze_engagements(self, engagements: List[Dict]) -> AnalysisReport:
        self.load_models()
        
        df = pd.DataFrame(engagements)
        if 'notes' not in df.columns:
            df['notes'] = ""
        
        # 1. Sentiment Analysis
        sentiments = [self._get_sentiment(f"{row.get('notes', '')} {row.get('feedback', '')}") for _, row in df.iterrows()]
        df['sentiment_score'] = [s['sentiment_score'] for s in sentiments]
        df['sentiment_type'] = [s['sentiment_type'] for s in sentiments]
        
        # 2. Topic Extraction & Clustering
        # Simple heuristic topic extraction first
        topics = []
        for _, row in df.iterrows():
            text = (row.get('notes', '') + " " + row.get('feedback', '')).lower()
            if "streaming" in text or "kafka" in text: topic = "Streaming"
            elif "governance" in text or "unity" in text: topic = "Governance"
            elif "performance" in text or "slow" in text: topic = "Performance"
            elif "migration" in text: topic = "Migration"
            else: topic = "General"
            topics.append(topic)
        df['topic'] = topics
        
        # Clustering if we have embeddings
        clusters = []
        if self.embedding_model and not df.empty:
            texts = (df['notes'] + " " + df.get('feedback', '')).tolist()
            embeddings = self.embedding_model.encode(texts)
            if len(df) > 2:
                clustering = AgglomerativeClustering(n_clusters=min(5, len(df))).fit(embeddings)
                df['cluster'] = clustering.labels_
            else:
                df['cluster'] = 0
        else:
            df['cluster'] = 0

        # 3. Generate Summary
        summary_prompt = f"Summarize these issues: {df['notes'].head(5).tolist()}"
        summary = self._generate_text(summary_prompt)
        if summary == "Analysis generated (Fallback): Check logs for details.":
             # Better fallback
             summary = f"Analyzed {len(df)} engagements. Top topic: {df['topic'].mode()[0] if not df.empty else 'None'}. Average sentiment: {df['sentiment_score'].mean():.2f}."

        # 4. Generate Plots
        plots = {
            "top_topics": plot_top_topics(df),
            "skills_gap": plot_skills_gap(df),
            "sentiment_trend": plot_sentiment_time_series(df)
        }
        
        # 5. Recommendations
        fixes = [
            "Review Unity Catalog permissions for Governance issues.",
            "Optimize shuffle partitions for Performance issues.",
            "Use Auto Loader for Streaming ingestion."
        ]
        
        tuning = ["spark.sql.shuffle.partitions", "spark.databricks.delta.optimizeWrite.enabled"]

        return AnalysisReport(
            summary=summary,
            clusters=[{"id": int(c), "size": int(len(df[df['cluster'] == c]))} for c in df['cluster'].unique()] if not df.empty else [],
            fixes=fixes,
            tuning_params=tuning,
            plotly_data=plots,
            notebook_markdown=f"# Analysis Report\n\n{summary}"
        )

    def stream_analyze_generator(self, engagements: List[Dict]) -> Generator[str, None, None]:
        # Yield steps
        yield json.dumps({"event": "status", "data": "Loading models..."})
        self.load_models()
        
        yield json.dumps({"event": "status", "data": "Analyzing sentiment..."})
        # ... (In real app, chunk processing)
        
        report = self.analyze_engagements(engagements)
        
        yield json.dumps({"event": "summary_ready", "data": report.summary})
        yield json.dumps({"event": "plots_ready", "data": report.plotly_data})
        yield json.dumps({"event": "final_report", "data": report.model_dump()})

engine = InferenceEngine()
