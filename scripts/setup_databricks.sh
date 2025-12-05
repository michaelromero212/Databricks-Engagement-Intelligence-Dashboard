#!/bin/bash
# Setup script for Databricks Integration

# 1. Load credentials from backend/.env
if [ -f backend/.env ]; then
    export $(grep -v '^#' backend/.env | xargs)
else
    echo "Error: backend/.env not found!"
    exit 1
fi

echo "Connecting to Databricks at $DATABRICKS_HOST..."

# 2. Upload Sample Data to DBFS
echo "Uploading sample data to DBFS..."
databricks fs mkdirs dbfs:/FileStore/ps_intelligence
databricks fs cp --overwrite backend/sample_data/engagements_sample.json dbfs:/FileStore/ps_intelligence/engagements_sample.json
echo "Data uploaded to dbfs:/FileStore/ps_intelligence/engagements_sample.json"

# 3. Import Notebook to Workspace
TARGET_PATH="/Shared/ps_intelligence/ingest_engagements"
echo "Importing ingestion notebook to $TARGET_PATH..."
databricks workspace mkdirs /Shared/ps_intelligence
# Legacy CLI requires -l PYTHON for source files
databricks workspace import --format SOURCE --language PYTHON --overwrite notebooks/ingest_engagements.py $TARGET_PATH
echo "Notebook imported."

echo "------------------------------------------------"
echo "Setup Complete! Next Steps:"
echo "1. Go to your Databricks Workspace: $DATABRICKS_HOST"
echo "2. Open the notebook at: $TARGET_PATH"
echo "3. Run the notebook to create the 'engagements' Delta Table."
echo "------------------------------------------------"
