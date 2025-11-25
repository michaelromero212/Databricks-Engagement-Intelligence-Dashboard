import random

class TopicExtractor:
    def __init__(self):
        # In a real scenario, this would initialize an LLM client
        pass

    def extract(self, text):
        """
        Extracts the main topic from the text.
        For this demo, we use a heuristic approach since we might not have API keys.
        """
        text_lower = text.lower()
        
        topics = {
            "streaming": ["streaming", "auto loader", "kafka", "real-time"],
            "governance": ["governance", "unity catalog", "permissions", "access control"],
            "performance": ["performance", "slow", "optimize", "latency", "tuning"],
            "migration": ["migration", "legacy", "convert", "move"],
            "infrastructure": ["terraform", "deployment", "setup", "configuration", "network"]
        }
        
        for topic, keywords in topics.items():
            if any(k in text_lower for k in keywords):
                return {"topic": topic, "confidence": 0.85}
                
        return {"topic": "general", "confidence": 0.5}
