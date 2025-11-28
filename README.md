# Databricks Engagement Intelligence Dashboard

A modern data visualization platform for analyzing Databricks Professional Services engagements with interactive charts and real-time insights.

## Architecture

- **Backend**: FastAPI (Python 3.8+) with REST API
- **Frontend**: React + Plotly.js for data visualizations
- **Dashboard**: Standalone HTML (no build required) or React app
- **AI/ML**: Local Hugging Face models with TextBlob fallback
- **Data**: JSON-based sample data (simulated Delta Lake)

## Quick Start

### Option 1: Standalone Dashboard (No Node.js Required)

1. **Start the Backend**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open Dashboard**
   - Simply open `dashboard.html` in your browser
   - The dashboard will automatically connect to http://localhost:8000

### Option 2: React Development Setup

1. **Start Backend** (same as above)

2. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## Features

- **📊 KPI Metrics**: Total engagements, sentiment scores, positive feedback, and at-risk tracking
- **📈 Interactive Charts**: 
  - Sentiment distribution (bar chart)
  - Top topics analysis (horizontal bar)
  - Sentiment timeline (line chart with trend)
  - Topic deep dive with progress indicators
- **🎯 Executive Summary**: Weekly briefing with key wins and action items
- **🔄 Real-time Data**: Live API connection with automatic updates
- **📱 Responsive Design**: Works on desktop, tablet, and mobile

## Dashboard Views

The dashboard provides 4 tabbed views:

1. **Overview**: Sentiment distribution and top topics charts
2. **Sentiment Analysis**: Timeline trend with neutral reference line
3. **Topic Analysis**: Frequency breakdown with visual progress bars
4. **Executive Summary**: Weekly briefing and action recommendations

## API Endpoints

- `GET /api/dashboard/data` - Complete dashboard data (KPIs, charts, timeline)
- `GET /api/engagements/recent` - Paginated engagement list
- `GET /health` - Backend health check

Full API documentation: http://localhost:8000/docs

## Project Structure

```
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── routes/        # API endpoints
│   │   ├── main.py        # FastAPI app
│   │   └── config.py      # Configuration
│   └── requirements.txt   # Python dependencies
├── frontend/              # React application (optional)
│   ├── src/
│   │   ├── pages/         # Dashboard components
│   │   └── api.js         # API client
│   └── package.json       # Node dependencies
├── dashboard.html         # Standalone dashboard (recommended)
├── data/                  # Sample engagement data
└── README.md
```

## Technology Stack

- **Backend**: FastAPI, Pandas, Plotly (chart generation)
- **Frontend**: React 18, Plotly.js, Tailwind CSS
- **Data Processing**: Pandas, NumPy, scikit-learn
- **AI Models**: Transformers, TextBlob, sentence-transformers

## Development Notes

- Uses sample JSON data for demonstration
- Production deployment would connect to Databricks Delta tables
- All visualizations use Plotly for consistency and interactivity
- Backend includes CORS support for local development
