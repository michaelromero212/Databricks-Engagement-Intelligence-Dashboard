import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import { getDashboardData, getHealth } from '../api';
import { Activity, TrendingUp, Users, AlertTriangle, BarChart3, PieChart, LineChart, Target } from 'lucide-react';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('overview');
    const [modelMode, setModelMode] = useState('unknown');

    useEffect(() => {
        fetchData();
        checkHealth();
    }, []);

    const fetchData = async () => {
        try {
            setLoading(true);
            const dashboardData = await getDashboardData();
            setData(dashboardData);
        } catch (e) {
            console.error("Failed to fetch dashboard data", e);
        } finally {
            setLoading(false);
        }
    };

    const checkHealth = async () => {
        try {
            const health = await getHealth();
            setModelMode(health.mode);
        } catch (e) {
            console.error("Health check failed", e);
        }
    };

    if (loading || !data) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-50">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading dashboard...</p>
                </div>
            </div>
        );
    }

    const { kpis, sentiment_distribution, top_topics, sentiment_timeline, engagements, summary } = data;

    // Prepare chart data
    const sentimentDistData = Object.entries(sentiment_distribution).map(([key, value]) => ({
        type: key,
        count: value,
        percentage: ((value / kpis.total_engagements) * 100).toFixed(1)
    }));

    const topicsData = Object.entries(top_topics).map(([topic, count]) => ({
        topic,
        count
    })).sort((a, b) => b.count - a.count);

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
                <div className="max-w-7xl mx-auto px-6 py-4">
                    <div className="flex justify-between items-center">
                        <div>
                            <div className="flex items-center gap-3">
                                <Activity className="w-7 h-7 text-blue-600" />
                                <h1 className="text-2xl font-bold text-gray-900">Databricks Engagement Intelligence</h1>
                            </div>
                            <p className="text-sm text-gray-500 mt-1">Real-time insights into customer engagement, sentiment trends, and team capabilities</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg border border-gray-200">
                                <div className={`w-2 h-2 rounded-full ${modelMode !== 'unknown' ? 'bg-green-500' : 'bg-gray-300'}`}></div>
                                <span className="text-xs font-medium text-gray-600">AI: {modelMode.replace('_', ' ')}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <div className="max-w-7xl mx-auto px-6 py-8">
                {/* KPIs */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-3">
                            <div className="p-2 bg-blue-50 rounded-lg">
                                <Users className="w-5 h-5 text-blue-600" />
                            </div>
                        </div>
                        <div className="text-3xl font-bold text-gray-900">{kpis.total_engagements}</div>
                        <div className="text-sm text-gray-500 mt-1">Total Engagements</div>
                    </div>

                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-3">
                            <div className="p-2 bg-green-50 rounded-lg">
                                <TrendingUp className="w-5 h-5 text-green-600" />
                            </div>
                        </div>
                        <div className="text-3xl font-bold text-gray-900">{kpis.avg_sentiment}</div>
                        <div className="text-sm text-gray-500 mt-1">Avg Sentiment</div>
                        <div className="text-xs text-green-600 mt-2">+{(kpis.avg_sentiment - 0.5).toFixed(2)} vs neutral</div>
                    </div>

                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-3">
                            <div className="p-2 bg-green-50 rounded-lg">
                                <Target className="w-5 h-5 text-green-600" />
                            </div>
                        </div>
                        <div className="text-3xl font-bold text-gray-900">{kpis.positive_count}</div>
                        <div className="text-sm text-gray-500 mt-1">Positive Feedback</div>
                        <div className="text-xs text-green-600 mt-2">{((kpis.positive_count / kpis.total_engagements) * 100).toFixed(1)}%</div>
                    </div>

                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-3">
                            <div className="p-2 bg-red-50 rounded-lg">
                                <AlertTriangle className="w-5 h-5 text-red-600" />
                            </div>
                        </div>
                        <div className="text-3xl font-bold text-gray-900">{kpis.at_risk_count}</div>
                        <div className="text-sm text-gray-500 mt-1">At Risk</div>
                        <div className="text-xs text-red-600 mt-2">{((kpis.at_risk_count / kpis.total_engagements) * 100).toFixed(1)}%</div>
                    </div>
                </div>

                {/* Tabs */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 mb-8">
                    <div className="border-b border-gray-200">
                        <nav className="flex gap-8 px-6" aria-label="Tabs">
                            {[
                                { id: 'overview', label: 'Overview', icon: BarChart3 },
                                { id: 'sentiment', label: 'Sentiment Analysis', icon: LineChart },
                                { id: 'topics', label: 'Topic Analysis', icon: PieChart },
                                { id: 'summary', label: 'Executive Summary', icon: Target }
                            ].map((tab) => (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === tab.id
                                            ? 'border-blue-600 text-blue-600'
                                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                        }`}
                                >
                                    <tab.icon className="w-4 h-4" />
                                    {tab.label}
                                </button>
                            ))}
                        </nav>
                    </div>

                    <div className="p-8">
                        {/* Overview Tab */}
                        {activeTab === 'overview' && (
                            <div className="space-y-8">
                                <div>
                                    <h2 className="text-xl font-semibold text-gray-900 mb-6">Sentiment Distribution</h2>
                                    <Plot
                                        data={[{
                                            type: 'bar',
                                            x: sentimentDistData.map(d => d.type),
                                            y: sentimentDistData.map(d => d.count),
                                            text: sentimentDistData.map(d => `${d.count} (${d.percentage}%)`),
                                            textposition: 'auto',
                                            marker: {
                                                color: sentimentDistData.map(d =>
                                                    d.type === 'positive' ? '#10B981' : d.type === 'negative' ? '#EF4444' : '#6B7280'
                                                )
                                            }
                                        }]}
                                        layout={{
                                            title: '',
                                            xaxis: { title: 'Sentiment Type' },
                                            yaxis: { title: 'Count' },
                                            height: 400,
                                            margin: { l: 60, r: 40, t: 20, b: 60 },
                                            plot_bgcolor: 'white',
                                            paper_bgcolor: 'white'
                                        }}
                                        config={{ displayModeBar: false, responsive: true }}
                                        style={{ width: '100%' }}
                                    />
                                </div>

                                <div>
                                    <h2 className="text-xl font-semibold text-gray-900 mb-6">Top Topics</h2>
                                    <Plot
                                        data={[{
                                            type: 'bar',
                                            x: topicsData.map(d => d.count),
                                            y: topicsData.map(d => d.topic),
                                            orientation: 'h',
                                            text: topicsData.map(d => d.count),
                                            textposition: 'outside',
                                            marker: {
                                                color: '#3B82F6',
                                                opacity: 0.8
                                            }
                                        }]}
                                        layout={{
                                            title: '',
                                            xaxis: { title: 'Number of Engagements' },
                                            yaxis: { title: '', automargin: true },
                                            height: 500,
                                            margin: { l: 150, r: 40, t: 20, b: 60 },
                                            plot_bgcolor: 'white',
                                            paper_bgcolor: 'white'
                                        }}
                                        config={{ displayModeBar: false, responsive: true }}
                                        style={{ width: '100%' }}
                                    />
                                </div>
                            </div>
                        )}

                        {/* Sentiment Tab */}
                        {activeTab === 'sentiment' && (
                            <div>
                                <h2 className="text-xl font-semibold text-gray-900 mb-6">Sentiment Trend Over Time</h2>
                                <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
                                    <p className="text-sm text-gray-700">
                                        <strong>What this chart shows:</strong> Daily average sentiment scores across all engagements. Values range from 0 (very negative) to 1 (very positive). The neutral baseline is 0.5.
                                    </p>
                                </div>
                                <Plot
                                    data={[{
                                        type: 'scatter',
                                        mode: 'lines+markers',
                                        x: sentiment_timeline.map(d => d.date),
                                        y: sentiment_timeline.map(d => d.sentiment),
                                        line: { color: '#3B82F6', width: 3 },
                                        marker: { size: 8, color: '#3B82F6' },
                                        fill: 'tozeroy',
                                        fillcolor: 'rgba(59, 130, 246, 0.1)'
                                    }]}
                                    layout={{
                                        title: '',
                                        xaxis: { title: 'Date' },
                                        yaxis: { title: 'Sentiment Score', range: [0, 1] },
                                        height: 450,
                                        margin: { l: 60, r: 40, t: 20, b: 60 },
                                        plot_bgcolor: 'white',
                                        paper_bgcolor: 'white',
                                        shapes: [{
                                            type: 'line',
                                            x0: sentiment_timeline[0]?.date,
                                            x1: sentiment_timeline[sentiment_timeline.length - 1]?.date,
                                            y0: 0.5,
                                            y1: 0.5,
                                            line: { color: '#9CA3AF', width: 2, dash: 'dash' }
                                        }]
                                    }}
                                    config={{ displayModeBar: false, responsive: true }}
                                    style={{ width: '100%' }}
                                />
                            </div>
                        )}

                        {/* Topics Tab */}
                        {activeTab === 'topics' && (
                            <div>
                                <h2 className="text-xl font-semibold text-gray-900 mb-6">Topic Deep Dive</h2>
                                <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
                                    <p className="text-sm text-gray-700">
                                        <strong>About this view:</strong> Identify the most frequently discussed topics and technical challenges across customer engagements. Topics appearing frequently may indicate systemic issues requiring knowledge base articles, training, or product improvements.
                                    </p>
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    {topicsData.map((topic, idx) => (
                                        <div key={idx} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                                            <div className="flex justify-between items-start mb-2">
                                                <h3 className="font-semibold text-gray-900 capitalize">{topic.topic}</h3>
                                                <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">{topic.count} engagements</span>
                                            </div>
                                            <div className="w-full bg-gray-200 rounded-full h-2">
                                                <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${(topic.count / kpis.total_engagements) * 100}%` }}></div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Summary Tab */}
                        {activeTab === 'summary' && (
                            <div>
                                <h2 className="text-xl font-semibold text-gray-900 mb-6">Weekly Executive Briefing</h2>
                                <div className="bg-white border-2 border-blue-100 rounded-xl p-6">
                                    <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{summary}</p>
                                </div>
                                <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="bg-green-50 border-l-4 border-green-500 p-6 rounded-lg">
                                        <h3 className="font-semibold text-green-800 mb-3">Key Wins</h3>
                                        <ul className="list-disc list-inside text-green-700 space-y-1 text-sm">
                                            <li>Strong positive sentiment trends</li>
                                            <li>Increasing engagement frequency</li>
                                            <li>Improved response times</li>
                                        </ul>
                                    </div>
                                    <div className="bg-orange-50 border-l-4 border-orange-500 p-6 rounded-lg">
                                        <h3 className="font-semibold text-orange-800 mb-3">Action Items</h3>
                                        <ul className="list-disc list-inside text-orange-700 space-y-1 text-sm">
                                            <li>Address at-risk engagements immediately</li>
                                            <li>Schedule training for top gap areas</li>
                                            <li>Review and update KB articles</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
