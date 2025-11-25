import json
import os
from app.llm.sentiment_model import SentimentModel
from app.llm.topic_extractor import TopicExtractor
from app.llm.summarizer import Summarizer

RAW_DATA_PATH = "data/raw/engagements_sample.json"
PROCESSED_DATA_PATH = "data/processed/analytics_results.json"

def main():
    print("Starting analysis pipeline...")
    
    # Load raw data
    if not os.path.exists(RAW_DATA_PATH):
        print(f"Error: Raw data not found at {RAW_DATA_PATH}")
        return

    with open(RAW_DATA_PATH, "r") as f:
        engagements = json.load(f)
        
    print(f"Loaded {len(engagements)} engagements.")
    
    # Initialize models
    sentiment_model = SentimentModel()
    topic_extractor = TopicExtractor()
    summarizer = Summarizer()
    
    processed_data = []
    
    # Process each engagement
    for eng in engagements:
        # Combine notes and feedback for analysis
        full_text = f"{eng['notes']} {eng['feedback']}"
        
        # Run analysis
        sentiment = sentiment_model.analyze(full_text)
        topic = topic_extractor.extract(full_text)
        
        # Enrich record
        eng["sentiment"] = sentiment
        eng["topic"] = topic
        
        processed_data.append(eng)
        
    # Generate weekly summary
    summary = summarizer.generate_weekly_summary(processed_data)
    
    # Save results
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    
    output = {
        "engagements": processed_data,
        "weekly_summary": summary
    }
    
    with open(PROCESSED_DATA_PATH, "w") as f:
        json.dump(output, f, indent=4)
        
    print(f"Analysis complete. Results saved to {PROCESSED_DATA_PATH}")
    print("\n=== Weekly Summary ===\n")
    print(summary)

if __name__ == "__main__":
    main()
