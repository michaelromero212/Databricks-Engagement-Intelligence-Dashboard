import json
import os
import logging
from typing import List, Dict
from app.config import settings

logger = logging.getLogger(__name__)

class DatabricksClient:
    """
    Client for Databricks workspace integration.
    
    NOTE: Databricks Free Edition Limitations (as of Dec 2024):
    - Personal Access Token generation may not be available in UI
    - Limited to serverless compute only
    - No account-level APIs
    - Max 5 concurrent job tasks per account
    - One SQL warehouse (2X-Small)
    
    For demo purposes, this client falls back to local sample data
    when credentials are not available.
    """
    def __init__(self):
        self.host = settings.DATABRICKS_HOST
        self.token = settings.DATABRICKS_TOKEN

    def fetch_recent_engagements(self, since_days: int = 7) -> List[Dict]:
        """
        Fetches recent engagements. 
        Tries to fetch from Databricks 'engagements' table.
        Falls back to local sample data if connection fails or table missing.
        """
        if not self.host or not self.token:
            logger.info("No Databricks credentials found. Using local sample data.")
            return self._load_local_sample()
            
        try:
            from databricks import sql
            http_path = os.getenv("DATABRICKS_HTTP_PATH")
            
            if not http_path:
                logger.warning("DATABRICKS_HTTP_PATH not set. Cannot connect to SQL Warehouse. Using sample data.")
                return self._load_local_sample()

            logger.info(f"Connecting to Databricks SQL Warehouse at {self.host}...")
            with sql.connect(server_hostname=self.host.replace("https://", ""),
                             http_path=http_path,
                             access_token=self.token) as connection:
                
                with connection.cursor() as cursor:
                    # Query columns matching our schema
                    cursor.execute("SELECT * FROM engagements LIMIT 100")
                    # Convert to dict
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    data = [dict(zip(columns, row)) for row in rows]
                    
                    if not data:
                         logger.warning("Engagements table is empty or missing. Using sample data.")
                         return self._load_local_sample()
                         
                    logger.info(f"Successfully fetched {len(data)} engagements from Databricks.")
                    return data
                    
        except ImportError:
            logger.error("databricks-sql-connector not installed. Using sample data.")
            return self._load_local_sample()
        except Exception as e:
            logger.error(f"Failed to fetch from Databricks: {e}. Using sample data.")
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
