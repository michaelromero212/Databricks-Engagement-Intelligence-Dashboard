# Usage Guide

## API Examples (curl)

### 1. Get Recent Engagements
```bash
curl "http://localhost:8000/api/engagements/recent?page=1&page_size=5"
```

### 2. Analyze Specific Engagements
```bash
curl -X POST "http://localhost:8000/api/analyze" \
     -H "Content-Type: application/json" \
     -d '{ "engagement_ids": ["1", "2"] }'
```

### 3. Analyze Raw Text (Ad-hoc)
```bash
curl -X POST "http://localhost:8000/api/analyze" \
     -H "Content-Type: application/json" \
     -d '{ "raw_logs": "Customer is complaining about slow shuffle performance on large joins." }'
```

### 4. Stream Analysis (SSE)
```bash
curl -N "http://localhost:8000/api/stream_analyze?ids=1,2,3"
```

## Frontend Workflow

1. **Select Engagements**: Click on rows in the left sidebar to select engagements for analysis.
2. **Analyze**: Click the "Analyze" button. The system will stream progress.
3. **Review**:
   - **Charts**: View topic distribution and skills gaps.
   - **Recommendations**: Read the AI-generated summary and fixes.
4. **Action**: Click "Commit to Notebook" to save the report to Databricks.
