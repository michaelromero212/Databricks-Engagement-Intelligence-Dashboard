# Databricks Engagement Intelligence Dashboard

A realistic internal PS (Professional Services) analytics tool for Databricks leadership. This project simulates an AI-powered pipeline that ingests unstructured engagement data (notes, feedback) and produces strategic insights.

## Problem
Databricks PS teams generate large volumes of unstructured data. Leadership needs to know:
- What problems customers are facing most frequently?
- Which solutions work well?
- Which skills are missing on the team?
- Which engagements may be at risk?

## Solution
An AI + Databricks analytics pipeline that ingests sample engagement data and produces:
1.  **Sentiment Analysis**: Score customer feedback and notes.
2.  **Topic Modeling**: Identify themes like "Streaming", "Governance", etc.
3.  **Skills Gap Analysis**: Compare tech frequency vs. team proficiency.
4.  **Weekly Executive Summary**: LLM-generated strategic memo.
5.  **Dashboard**: A clean Streamlit interface to visualize outcomes.

## Visual Tour

### Main Dashboard
![Main Dashboard](docs/images/01_main_dashboard.png)
*Dashboard overview with Key Performance Indicators and Executive Snapshot showing overall engagement health status with color-coded indicator.*

### Priority Table
![Priority Table](docs/images/02_priority_table.png)
*Actionable priority table displaying engagements requiring attention, sorted by priority score with progress bars for sentiment and urgency visualization.*

### Sentiment Analysis
![Sentiment Analysis](docs/images/03_sentiment_analysis.png)
*Horizontal stacked bar chart showing sentiment distribution and trend line with color-coded context zones (danger/warning/healthy) for instant interpretation.*

### Topics & Issues
![Topics & Issues](docs/images/04_topics_issues.png)
*Enhanced bar chart with topic concentration metrics displaying the most frequent engagement topics with direct labels and percentage breakdowns.*

### Skills Gap Analysis
![Skills Gap](docs/images/05_skills_gap.png)
*Diverging bar chart comparing market demand vs. team proficiency, with red bars indicating training priorities and green bars showing surplus capacity.*

### Executive Report
![Executive Report](docs/images/06_executive_report.png)
*AI-generated weekly briefing with comprehensive insights and recommended leadership actions based on engagement patterns and trends.*

## Architecture
```mermaid
graph LR
    A[Raw Data (JSON)] --> B[Analysis Pipeline];
    B --> C{AI Models};
    C -->|Sentiment| D[Enriched Data];
    C -->|Topic Extraction| D;
    C -->|Summarization| E[Executive Summary];
    D --> F[Delta Lake / Processed JSON];
    F --> G[Streamlit Dashboard];
    E --> G;
```

## Tech Stack
-   **Python 3.11+**
-   **Streamlit**: Interactive dashboard
-   **Plotly**: Data visualization
-   **TextBlob**: Sentiment analysis
-   **Pandas**: Data manipulation
-   **Databricks SDK**: (Optional) For Delta Lake integration

## Setup & Usage

1.  **Create Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Generate Synthetic Data**
    ```bash
    python -m app.utils.data_generator
    ```

3.  **Run Analysis Pipeline**
    ```bash
    python -m app.main_pipeline
    ```

4.  **Launch Dashboard**
    ```bash
    streamlit run app/dashboard/streamlit_dashboard.py
    ```

## Project Structure
-   `app/utils/data_generator.py`: Generates realistic synthetic engagement records.
-   `app/main_pipeline.py`: Orchestrates the data loading and analysis.
-   `app/llm/`: Contains modules for sentiment, topic extraction, and summarization.
-   `app/dashboard/`: Contains the Streamlit app and plot components.
-   `data/`: Stores raw and processed JSON data.

## Demo Walkthrough
1.  **Data Generation**: Creates 500 records with varying industries, technologies, and statuses.
2.  **Analysis**: The pipeline processes text to extract sentiment and topics, and generates a weekly summary.
3.  **Dashboard**:
    -   **Engagement Sentiment**: View sentiment distribution and trends.
    -   **Top Issues**: Identify recurring technical challenges.
    -   **Skills Gap**: Visualize demand vs. team proficiency.
    -   **Executive Summary**: Read the AI-generated weekly briefing.

## Features

### Data Visualization Best Practices
- **Optimized Chart Types**: Replaced pie charts with stacked bars for easier comparison (2-3x better comprehension)
- **Context Zones**: Color-coded background zones on trends for instant health interpretation
- **Diverging Bar Charts**: Shows skills gap magnitude and direction intuitively
- **Direct Labels**: All charts include inline values reducing cognitive load
- **Clear Explanations**: Every chart has "What this shows" and "What to look for" guidance

### Modern, Accessible Design
- **WCAG AA Compliant**: All colors meet accessibility standards with verified contrast ratios
- **Responsive Layout**: Fully responsive design that works on desktop, tablet, and mobile
- **Color-blind Friendly**: Uses carefully selected color palettes safe for all users
- **Professional UI**: Clean, modern interface with consistent styling and no decorative elements

### AI-Powered Insights
- **Sentiment Analysis**: Automatically scores customer feedback using TextBlob
- **Topic Extraction**: Identifies recurring themes and technical challenges
- **Executive Summaries**: Generates strategic insights for leadership
- **Priority Scoring**: Automatic calculation of engagement urgency based on sentiment and staleness

### Interactive Visualizations
- **Dynamic Charts**: Interactive Plotly charts with responsive containers
- **Filterable Data**: Sidebar controls to filter by engagement status
- **Sortable Tables**: Priority table with progress bar visualization
- **Real-time Updates**: Dashboard responds instantly to filter changes
