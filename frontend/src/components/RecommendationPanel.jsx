```javascript
import React from 'react';
import { commitNotebook } from '../api';
import { CheckCircle, AlertTriangle, Lightbulb, BookOpen, ArrowRight } from 'lucide-react';

const RecommendationPanel = ({ report, loading }) => {
  if (loading) {
    return (
      <div className="animate-pulse space-y-4 p-4 border border-gray-100 rounded-lg bg-white">
        <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        <div className="h-32 bg-gray-100 rounded"></div>
      </div>
    );
  }

  if (!report) {
    return null;
  }

  const handleCommit = async () => {
    try {
      await commitNotebook("/Shared/Engagement_Analysis", report.notebook_markdown);
      alert("Successfully committed to Databricks notebook!");
    } catch (e) {
      alert("Failed to commit: " + e.message);
    }
  };

  return (
    <div className="space-y-6">
      {/* Summary Card */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <BookOpen className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-slate-800">Executive Summary</h3>
        </div>
        <div className="prose prose-sm max-w-none text-slate-600 leading-relaxed">
          <p>{report.summary}</p>
        </div>
      </div>

      {/* Fixes & Tuning */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-green-100 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-green-500"></div>
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <h4 className="font-semibold text-slate-800">Suggested Fixes</h4>
          </div>
          <ul className="space-y-3">
            {report.fixes.map((fix, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-slate-600">
                <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-green-400 flex-shrink-0"></span>
                {fix}
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-blue-100 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="w-5 h-5 text-blue-600" />
            <h4 className="font-semibold text-slate-800">Tuning Parameters</h4>
          </div>
          <div className="flex flex-wrap gap-2">
            {report.tuning_params.map((param, i) => (
              <code key={i} className="px-2.5 py-1.5 bg-blue-50 text-blue-700 rounded-md text-xs font-mono border border-blue-100">
                {param}
              </code>
            ))}
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex justify-end pt-2">
        <button 
          onClick={handleCommit}
          className="group px-5 py-2.5 bg-slate-800 text-white rounded-lg hover:bg-slate-700 text-sm font-medium transition-all shadow-sm hover:shadow flex items-center gap-2"
        >
          Commit to Notebook
          <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
        </button>
      </div>
    </div>
  );
};

export default RecommendationPanel;
```
