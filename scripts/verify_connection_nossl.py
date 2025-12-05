import os
import logging
from dotenv import load_dotenv
from databricks import sql
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verify_connection")

# Load environment variables
load_dotenv("backend/.env")

def verify_connection():
    host = os.getenv("DATABRICKS_HOST", "").replace("https://", "")
    token = os.getenv("DATABRICKS_TOKEN")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")

    if not all([host, token, http_path]):
        logger.error("❌ Missing configuration! Check backend/.env")
        return

    logger.info(f"Connecting to {host}...")
    
    # Create unverified SSL context for dev testing
    ssl_context = ssl._create_unverified_context()
    
    try:
        # Pass _tls_verify_hostname=False and _ssl_context
        with sql.connect(server_hostname=host, 
                         http_path=http_path, 
                         access_token=token,
                         _tls_verify_hostname=False,
                         _ssl_context=ssl_context) as connection:
                         
            with connection.cursor() as cursor:
                # Check for table existence and count
                logger.info("Executing query: SELECT count(*) FROM engagements")
                cursor.execute("SELECT count(*) FROM engagements")
                result = cursor.fetchone()
                count = result[0]
                
                logger.info(f"✅ SUCCESS! Found 'engagements' table with {count} records.")
                
                # Fetch a sample
                cursor.execute("SELECT customer, sentiment_score, date FROM engagements LIMIT 3")
                rows = cursor.fetchall()
                logger.info("Sample data:")
                for row in rows:
                    logger.info(f" - {row.customer}: {row.sentiment_score} ({row.date})")
                    
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    verify_connection()
