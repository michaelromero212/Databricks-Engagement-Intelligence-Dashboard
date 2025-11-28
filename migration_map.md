# Migration Map: Streamlit to React + FastAPI

This document maps the original Streamlit components to their new React/FastAPI counterparts.

## 1. UI Components

| Streamlit Component | React Component / HTML |
|---------------------|------------------------|
| `st.sidebar` | `<div className="w-80 border-r ...">` (Sidebar in `Dashboard.jsx`) |
| `st.button("Analyze")` | `<button onClick={handleAnalyze}>` |
| `st.selectbox` | `<select>` or Custom Dropdown |
| `st.markdown` | `<div className="prose">` or `RecommendationPanel.jsx` |
| `st.plotly_chart` | `<PlotlyChart />` (wraps `react-plotly.js`) |
| `st.write(df)` | Custom Table or `LogViewer.jsx` |

## 2. State Management

| Streamlit Pattern | React Pattern |
|-------------------|---------------|
| `if st.button(): ...` | `const handleAnalyze = async () => { ... }` |
| `st.session_state` | `useState` hook (e.g., `const [engagements, setEngagements] = useState([])`) |
| Rerun on interaction | `useEffect` for data fetching; State updates trigger re-renders |

## 3. Data Flow

| Streamlit | FastAPI + React |
|-----------|-----------------|
| Direct Pandas manipulation | Backend: Pandas -> JSON (Pydantic) -> API Response |
| `df = load_data()` | Frontend: `fetch('/api/engagements')` -> `setEngagements(data)` |
| `plot_func(df)` | Backend: `plot_func(df).to_dict()` -> Frontend: `<PlotlyChart figure={data} />` |

## 4. Code Examples

### Button Action
**Streamlit:**
```python
if st.button("Analyze"):
    results = analyze(data)
    st.write(results)
```

**React:**
```javascript
const handleAnalyze = async () => {
  setLoading(true);
  const results = await postAnalyze(selectedIds);
  setReport(results);
  setLoading(false);
};

return <button onClick={handleAnalyze}>Analyze</button>
```

### Plotting
**Streamlit:**
```python
fig = px.bar(df, x='a', y='b')
st.plotly_chart(fig)
```

**React:**
```javascript
// Backend returns fig.to_dict()
// Frontend:
<PlotlyChart figure={apiResponse.plotData} />
```
