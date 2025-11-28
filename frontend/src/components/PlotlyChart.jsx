```
import React from 'react';
import Plot from 'react-plotly.js';

const PlotlyChart = ({ figure, title, height = 400 }) => {
  if (!figure || !figure.data) {
    return (
      <div className="h-64 flex items-center justify-center bg-white rounded-xl border border-gray-100 shadow-sm animate-pulse">
        <div className="flex flex-col items-center gap-2">
          <div className="w-8 h-8 border-2 border-blue-100 border-t-blue-500 rounded-full animate-spin"></div>
          <span className="text-xs text-gray-400 font-medium">Loading visualization...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-300">
      {title && (
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-base font-semibold text-slate-800 tracking-tight">{title}</h3>
        </div>
      )}
      <div className="rounded-lg overflow-hidden">
        <Plot
          data={figure.data}
          layout={{ 
            ...figure.layout, 
            autosize: true, 
            height: height,
            margin: { l: 50, r: 20, t: 20, b: 40 },
            font: { family: 'Inter, system-ui, sans-serif', color: '#64748b' },
            paper_bgcolor: 'white',
            plot_bgcolor: 'white',
            hoverlabel: { bgcolor: "#1e293b", font: { color: "white" } }
          }}
          useResizeHandler={true}
          style={{ width: "100%", height: "100%" }}
          config={{ 
            displayModeBar: false,
            responsive: true 
          }}
        />
      </div>
    </div>
  );
};

export default PlotlyChart;
```
