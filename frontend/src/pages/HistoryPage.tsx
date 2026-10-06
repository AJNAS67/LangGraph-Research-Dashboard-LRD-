import React, { useState } from 'react';
import { ResearchSession } from '../types/research';
import { Search, ArrowRight, RotateCcw, Clock, BookOpen } from 'lucide-react';

interface HistoryPageProps {
  sessions: ResearchSession[];
  onSelectSession: (session: ResearchSession) => void;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({ sessions, onSelectSession }) => {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'completed' | 'running'>('all');

  const filtered = sessions.filter(s => {
    const matchesStatus = statusFilter === 'all' || s.status === statusFilter;
    const matchesSearch = s.title.toLowerCase().includes(search.toLowerCase()) ||
                          s.user_query.toLowerCase().includes(search.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-100">Research History & Session Archive</h1>
        <p className="text-xs text-slate-400 mt-1">Audit past investigations, inspected node transitions, and exported reports</p>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 glass-panel p-3.5 rounded-xl">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search research history..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700/60 text-xs text-slate-200 placeholder-slate-400 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div className="flex items-center gap-1.5 text-xs self-start sm:self-center">
          {(['all', 'completed', 'running'] as const).map(f => (
            <button
              key={f}
              onClick={() => setStatusFilter(f)}
              className={`px-3 py-1 rounded-lg capitalize transition-colors ${
                statusFilter === f
                  ? 'bg-indigo-600 text-white font-medium'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        {filtered.map(s => (
          <div
            key={s.id}
            onClick={() => onSelectSession(s)}
            className="glass-panel p-4 rounded-xl hover:border-indigo-500/50 transition-all duration-200 cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
          >
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full border ${
                  s.status === 'completed'
                    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                    : 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
                }`}>
                  {s.status}
                </span>
                <span className="text-xs text-slate-400 font-mono">ID: {s.id}</span>
                {s.retry_count > 0 && (
                  <span className="text-[10px] text-amber-400 flex items-center gap-1 bg-amber-500/10 px-1.5 py-0.5 rounded">
                    <RotateCcw className="w-3 h-3" /> {s.retry_count} retries
                  </span>
                )}
              </div>
              <h3 className="text-sm font-semibold text-slate-200 group-hover:text-indigo-300 transition-colors">
                {s.title}
              </h3>
              <p className="text-xs text-slate-400 line-clamp-1">{s.user_query}</p>
            </div>

            <div className="flex items-center gap-4 text-xs text-slate-400 self-end sm:self-center font-mono">
              <span className="flex items-center gap-1">
                <BookOpen className="w-3.5 h-3.5" /> {s.collected_sources?.length || 0}
              </span>
              <span>{new Date(s.created_at).toLocaleDateString()}</span>
              <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-indigo-400 transition-transform group-hover:translate-x-1" />
            </div>
          </div>
        ))}

        {filtered.length === 0 && (
          <div className="text-center py-12 text-slate-400 text-xs">
            No research sessions matching your query.
          </div>
        )}
      </div>
    </div>
  );
};
