import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
    DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    # Modes: 'auto' (try local, fail to api), 'local', 'huggingface_api'
    MODEL_MODE = os.getenv("MODEL_MODE", "auto")
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SAMPLE_DATA_PATH = os.path.join(BASE_DIR, "..", "sample_data", "engagements_sample.json")

settings = Config()
