from textblob import TextBlob

class SentimentModel:
    def __init__(self):
        pass

    def analyze(self, text):
        """
        Analyzes the sentiment of the given text.
        Returns a dictionary with sentiment_type and sentiment_score.
        """
        if not text:
            return {"sentiment_type": "neutral", "sentiment_score": 0.0}

        blob = TextBlob(text)
        score = blob.sentiment.polarity

        if score > 0.1:
            sentiment_type = "positive"
        elif score < -0.1:
            sentiment_type = "negative"
        else:
            sentiment_type = "neutral"

        return {
            "sentiment_type": sentiment_type,
            "sentiment_score": score
        }
