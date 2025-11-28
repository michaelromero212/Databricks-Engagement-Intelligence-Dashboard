import React, { useState } from 'react';
import { Search, FileText, Calendar } from 'lucide-react';

const LogViewer = ({ engagements, selectedIds, onToggleSelection }) => {
    const [searchTerm, setSearchTerm] = useState("");

    const filtered = engagements.filter(e =>
        e.customer.toLowerCase().includes(searchTerm.toLowerCase()) ||
        e.notes.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="h-full flex flex-col bg-white">
            <div className="p-4 border-b border-gray-100 bg-white sticky top-0 z-10">
                <div className="relative">
                    <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Search logs..."
                        className="w-full pl-9 pr-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all placeholder:text-gray-400"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <div className="mt-2 text-xs text-gray-400 font-medium px-1">
                    {filtered.length} engagements found
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-2 space-y-1">
                {filtered.map(eng => (
                    <div
                        key={eng.id}
                        onClick={() => onToggleSelection(eng.id)}
                        className={`group p-3 rounded-md cursor-pointer transition-all border border-transparent ${selectedIds.includes(eng.id)
                                ? "bg-blue-50 border-blue-200 shadow-sm"
                                : "hover:bg-gray-50 hover:border-gray-100"
                            }`}
                    >
                        <div className="flex justify-between items-start mb-1.5">
                            <span className={`font-semibold text-sm ${selectedIds.includes(eng.id) ? 'text-blue-700' : 'text-slate-700'}`}>
                                {eng.customer}
                            </span>
                            <span className="flex items-center text-[10px] text-gray-400 bg-gray-50 px-1.5 py-0.5 rounded border border-gray-100">
                                {eng.date}
                            </span>
                        </div>
                        <p className={`text-xs line-clamp-2 leading-relaxed ${selectedIds.includes(eng.id) ? 'text-blue-600/80' : 'text-gray-500'}`}>
                            {eng.notes}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default LogViewer;
