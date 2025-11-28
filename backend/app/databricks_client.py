import json
import os
import logging
from typing import List, Dict
from app.config import settings

logger = logging.getLogger(__name__)

class DatabricksClient:
    def __init__(self):
        self.host = settings.DATABRICKS_HOST
        self.token = settings.DATABRICKS_TOKEN
        
    def fetch_recent_engagements(self, since_days: int = 7) -> List[Dict]:
        """
        Fetches recent engagements. 
        If no credentials, returns local sample data.
        """
        if not self.host or not self.token:
            logger.info("No Databricks credentials found. Using local sample data.")
            return self._load_local_sample()
            
        # In a real app, use databricks-sdk or requests to query a Delta table
        # For now, we'll just return sample data even if creds exist (as this is a demo transformation)
        # But we log that we would have connected.
        logger.info(f"Connected to Databricks at {self.host}. Fetching data (simulated)...")
        return self._load_local_sample()

    def _load_local_sample(self) -> List[Dict]:
        path = settings.SAMPLE_DATA_PATH
        if not os.path.exists(path):
            logger.error(f"Sample data not found at {path}")
            return []
            
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    def commit_notebook_cell(self, notebook_path: str, markdown: str):
        if not self.host or not self.token:
            raise Exception("Databricks credentials not configured.")
            
        # Stub for Databricks Workspace API
        # POST /api/2.0/workspace/import or similar to append
        logger.info(f"Committing to notebook {notebook_path}: {markdown[:50]}...")
        return {"status": "success", "message": "Cell appended (simulated)"}

db_client = DatabricksClient()
