class Summarizer:
    def __init__(self):
        pass

    def generate_weekly_summary(self, analytics_results):
        """
        Generates a weekly executive summary based on analytics results.
        """
        num_engagements = len(analytics_results)
        
        # Calculate sentiment stats
        sentiments = [r.get("sentiment", {}).get("sentiment_type", "neutral") for r in analytics_results]
        positive_count = sentiments.count("positive")
        negative_count = sentiments.count("negative")
        
        # Calculate top topics
        topics = [r.get("topic", {}).get("topic", "general") for r in analytics_results]
        top_topic = max(set(topics), key=topics.count) if topics else "N/A"
        
        summary = f"""WEEKLY PS EXEC SUMMARY
- {num_engagements} engagements analyzed this week
- Top topic: {top_topic}
- Sentiment: {positive_count} positive, {negative_count} negative
- Recommended focus: Address recurring issues in {top_topic} and ensure team is upskilled.
"""
        return summary
