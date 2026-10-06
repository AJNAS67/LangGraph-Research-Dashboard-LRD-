import React, { useState } from 'react';
import { CollectedSource } from '../../types/research';
import { ExternalLink, Globe, BookOpen, Newspaper, FileText, Sparkles, Filter } from 'lucide-react';

interface SourcesExplorerProps {
  sources: CollectedSource[];
}

export const SourcesExplorer: React.FC<SourcesExplorerProps> = ({ sources }) => {
  const [filterType, setFilterType] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const filteredSources = sources.filter(s => {
    const matchesType = filterType === 'all' || s.source_type === filterType;
    const matchesSearch = s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          s.summary.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesType && matchesSearch;
  });

  const getSourceIcon = (type: string) => {
    switch (type) {
      case 'academic':
        return <BookOpen className="w-3.5 h-3.5 text-purple-400" />;
      case 'news':
        return <Newspaper className="w-3.5 h-3.5 text-amber-400" />;
      case 'document':
        return <FileText className="w-3.5 h-3.5 text-sky-400" />;
      default:
        return <Globe className="w-3.5 h-3.5 text-emerald-400" />;
    }
  };

  return (
    <div className="space-y-4">
      {/* Search & Filter Header */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 glass-panel p-3 rounded-xl">
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-slate-400" />
          <div className="flex items-center gap-1 text-xs">
            {['all', 'academic', 'web', 'news'].map(type => (
              <button
                key={type}
                onClick={() => setFilterType(type)}
                className={`px-2.5 py-1 rounded-lg capitalize transition-colors ${
                  filterType === type
                    ? 'bg-indigo-600 text-white font-medium'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        <input
          type="text"
          placeholder="Filter discovered sources..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full sm:w-64 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700/60 text-xs text-slate-200 placeholder-slate-400 focus:outline-none focus:border-indigo-500"
        />
      </div>

      {/* Sources Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredSources.map((source) => {
          const scorePercent = Math.round((source.relevance_score || 0.8) * 100);

          return (
            <div
              key={source.id}
              className="glass-panel rounded-xl p-4 flex flex-col justify-between hover:border-indigo-500/50 transition-all duration-200 group"
            >
              <div>
                {/* Meta header */}
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-slate-800 text-[11px] font-medium text-slate-300 border border-slate-700/50">
                    {getSourceIcon(source.source_type)}
                    <span className="capitalize">{source.source_type}</span>
                  </div>

                  {/* Relevance Score Badge */}
                  <div className="flex items-center gap-1 text-[11px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                    <Sparkles className="w-3 h-3" />
                    <span>{scorePercent}% match</span>
                  </div>
                </div>

                {/* Source Title & URL Link */}
                <h4 className="text-sm font-semibold text-slate-100 group-hover:text-indigo-300 transition-colors line-clamp-2">
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1.5 hover:underline"
                  >
                    {source.title}
                    <ExternalLink className="w-3.5 h-3.5 opacity-60 flex-shrink-0" />
                  </a>
                </h4>

                <p className="text-xs text-slate-400 font-mono mt-1 truncate">
                  {source.url}
                </p>

                {/* Extracted Summary */}
                <p className="text-xs text-slate-300 mt-2.5 leading-relaxed bg-slate-900/50 p-2.5 rounded-lg border border-slate-800/80">
                  {source.summary}
                </p>
              </div>

              {/* Timestamp footer */}
              <div className="mt-3 pt-2 border-t border-slate-800/60 text-[10px] text-slate-400 flex items-center justify-between">
                <span>Retrieved: {new Date(source.retrieved_at).toLocaleTimeString()}</span>
                <span className="font-mono text-slate-400">ID: {source.id.slice(0, 8)}</span>
              </div>
            </div>
          );
        })}
      </div>

      {filteredSources.length === 0 && (
        <div className="text-center py-12 text-slate-400 text-xs">
          No sources matching your filter.
        </div>
      )}
    </div>
  );
};
