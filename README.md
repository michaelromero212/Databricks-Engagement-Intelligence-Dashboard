# Databricks PS Intelligence Dashboard

A modern, enterprise-grade data visualization platform for analyzing Databricks Professional Services engagements. This dashboard provides real-time insights into customer sentiment, engagement risks, and trending technical topics using a React + Plotly frontend and a FastAPI backend.

![Dashboard Overview](docs/images/dashboard_overview.png)

## 🚀 Overview

The **Databricks PS Intelligence Dashboard** is designed to help Field Engineering teams proactively manage customer engagements. It aggregates data from engagement logs, applies AI-driven sentiment analysis and topic extraction, and presents actionable insights through an interactive, professional interface.

### Key Features
- **Real-time KPI Tracking**: Monitor Total Engagements, Average Sentiment, At-Risk Accounts, and Topic Trends.
- **Interactive Visualizations**: Dynamic charts including trend lines, account health tables, and topic analytics.
- **Databricks SQL Integration**: Query data directly from Delta Tables via SQL Warehouse.
- **Advanced Filtering**: Client-side filtering by Search, Status (At-Risk, Completed), and Sentiment.
- **Responsive Design**: Fully functional on desktop, tablet, and mobile devices.
- **Accessibility**: Color-blind friendly palette (Teal/Orange) and clear chart explanations.

---

## 📸 Dashboard Views

### 1. Executive Overview
The landing page provides a high-level summary of the business.
- **Sentiment Distribution**: Quickly see the ratio of Positive vs. Negative engagements.
- **Top Topics**: Identify the most discussed technical areas (e.g., "Streaming", "Unity Catalog").

![Dashboard Overview](docs/images/dashboard_overview.png)
*Figure 1: The Overview tab showing KPIs and high-level charts.*

### 2. Engagement Details
A detailed, sortable data grid for deep dives into specific customer interactions.
- **Status Badges**: Color-coded indicators for quick status checks.
- **Sentiment Bars**: Visual representation of sentiment scores (0.0 to 1.0).

![Engagement Details](docs/images/dashboard_engagements.png)
*Figure 2: The Engagements tab with a detailed, filterable data table.*

### 3. Sentiment Analysis
Advanced analytics to track customer health over time.
- **Sentiment Trend**: Linear-interpolated line chart with data markers showing rolling average sentiment.
- **Customer Account Health Table**: Aggregated view per customer showing engagement count, avg sentiment, trend direction (↑/→/↓), and status badges.

![Sentiment Analysis](docs/images/dashboard_sentiment.png)
*Figure 3: The Sentiment tab featuring trend lines and Customer Account Health table.*

### 4. Topic Trends
Track how discussion topics evolve over time.
- **Topic Trend Lines**: Multi-line chart showing topic frequency by month. Rising lines indicate growing focus areas.

![Topic Trends](docs/images/dashboard_topics.png)
*Figure 4: The Topics tab displaying trend lines for technical discussions.*

### 5. Executive Briefing
AI-generated weekly summary with wins and risks.

![Executive Briefing](docs/images/dashboard_briefing.png)
*Figure 5: The Briefing tab with AI-generated executive summary.*

---

## 🛠️ Technology Stack

### Frontend
- **React 18**: Component-based UI architecture.
- **Plotly.js**: Enterprise-grade data visualization library.
- **Tailwind CSS**: Utility-first styling for a clean, modern look.
- **Lucide Icons**: Professional, consistent iconography.

### Backend
- **FastAPI**: High-performance Python web framework.
- **Pandas & NumPy**: Data manipulation and analysis.
- **Scikit-learn**: Machine learning utilities (clustering, etc.).
- **Hugging Face Transformers**: Local LLMs for sentiment and topic extraction.

### Data
- **JSON / Delta Lake**: Simulated engagement logs (extensible to real Delta Tables).

---

## 🚀 Quick Start

### Option 1: Standalone Dashboard (Recommended)
No Node.js required. Just run the backend and open the HTML file.

1. **Start Backend**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Launch Dashboard**
   - Open `dashboard.html` in your browser.

### Option 2: Full React Development
For developers who want to customize the frontend code.

1. **Start Backend** (same as above)
2. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

## 🔮 Future Deployment Strategy

To move this from a local prototype to a production internal tool at Databricks:

1.  **Containerization**:
    - Build Docker images for Backend (`backend/Dockerfile`) and Frontend (`frontend/Dockerfile`).
    - Orchestrate with Kubernetes (EKS/AKS) or Databricks Apps.

2.  **Data Integration**:
    - Replace the JSON sample data with a direct connection to **Databricks SQL**.
    - Use the Databricks SDK to fetch real-time engagement logs from Delta Tables.

## 🧱 Databricks Integration

This project supports **direct integration with Databricks SQL Warehouses** for real-time data access.

### Features
- **SQL Warehouse Connectivity**: Query Delta Tables directly via `databricks-sql-connector`
- **Embedded Sample Data**: Ingestion notebook includes sample data for quick demos
- **Automatic Fallback**: Uses local JSON when Databricks credentials unavailable

### One-Time Setup
1. **Generate Token**: In Databricks, go to User Settings → Developer → Access Tokens
2. **Create `.env`**: Add credentials to `backend/.env`:
   ```bash
   DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
   DATABRICKS_TOKEN=dapi...
   DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
   ```
3. **Run Ingestion Notebook**: Import and run `notebooks/ingest_engagements.py` **once** to create the `engagements` table
4. **Start Dashboard**: Data persists in Delta Lake - no need to re-run the notebook!

### CLI Setup (Optional)
```bash
./scripts/setup_databricks.sh  # Uploads notebook and sample data
```

---

## 🔮 Future Deployment Strategy

To move this from a local prototype to a production internal tool at Databricks:

1. **Containerization**: Build Docker images and deploy with Kubernetes or Databricks Apps
2. **Authentication**: Integrate SSO using Databricks OAuth or Okta
3. **CI/CD**: Set up GitHub Actions for automated testing and deployment
