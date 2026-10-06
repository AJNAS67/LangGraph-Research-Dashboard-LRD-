import React, { useState } from 'react';
import { ResearchSession } from '../types/research';
import { GraphVisualizer } from '../features/workflow/GraphVisualizer';
import { ResearchPlanViewer } from '../features/workflow/ResearchPlanViewer';
import { SourcesExplorer } from '../features/sources/SourcesExplorer';
import { ReportViewer } from '../features/report/ReportViewer';
import { ArrowLeft, Clock, Layers, Globe, FileText, Code2, Sparkles } from 'lucide-react';

interface SessionDetailPageProps {
  session: ResearchSession;
  onBack: () => void;
}

export const SessionDetailPage: React.FC<SessionDetailPageProps> = ({ session, onBack }) => {
  const [activeTab, setActiveTab] = useState<'plan' | 'sources' | 'report' | 'state'>('plan');

  return (
    <div className="space-y-6">
      {/* Back button and Meta Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-5 rounded-2xl">
        <div className="flex items-start sm:items-center gap-3">
          <button
            onClick={onBack}
            className="p-2 rounded-xl bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors mt-0.5 sm:mt-0"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full border ${
                session.status === 'completed'
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                  : 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20 animate-pulse'
              }`}>
                {session.status}
              </span>
              <span className="text-xs text-slate-400 font-mono">Depth: {session.research_depth}</span>
            </div>
            <h1 className="text-base sm:text-lg font-bold text-slate-100 mt-1 line-clamp-2">
              {session.title}
            </h1>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs text-slate-400 font-mono">
          <Clock className="w-3.5 h-3.5" />
          <span>{new Date(session.created_at).toLocaleTimeString()}</span>
        </div>
      </div>

      {/* LangGraph State Machine Visualization Component */}
      <GraphVisualizer
        currentNode={session.current_node}
        status={session.status}
        retryCount={session.retry_count}
        maxRetries={session.max_retries}
      />

      {/* Tab Navigation */}
      <div className="flex items-center gap-2 border-b border-slate-800/80 pb-1 text-xs">
        <button
          onClick={() => setActiveTab('plan')}
          className={`flex items-center gap-1.5 px-3 py-2 rounded-lg font-medium transition-colors ${
            activeTab === 'plan'
              ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Layers className="w-3.5 h-3.5" />
          <span>Research Plan ({session.subtasks.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('sources')}
          className={`flex items-center gap-1.5 px-3 py-2 rounded-lg font-medium transition-colors ${
            activeTab === 'sources'
              ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Globe className="w-3.5 h-3.5" />
          <span>Discovered Sources ({session.collected_sources.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('report')}
          className={`flex items-center gap-1.5 px-3 py-2 rounded-lg font-medium transition-colors ${
            activeTab === 'report'
              ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <FileText className="w-3.5 h-3.5" />
          <span>Final Report</span>
        </button>

        <button
          onClick={() => setActiveTab('state')}
          className={`flex items-center gap-1.5 px-3 py-2 rounded-lg font-medium transition-colors ${
            activeTab === 'state'
              ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/30'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Code2 className="w-3.5 h-3.5" />
          <span>Raw Graph State</span>
        </button>
      </div>

      {/* Tab Panels */}
      <div>
        {activeTab === 'plan' && (
          <ResearchPlanViewer
            objective={session.research_objective}
            subtasks={session.subtasks}
          />
        )}

        {activeTab === 'sources' && (
          <SourcesExplorer sources={session.collected_sources} />
        )}

        {activeTab === 'report' && (
          <ReportViewer report={session.final_report} />
        )}

        {activeTab === 'state' && (
          <div className="glass-panel p-4 rounded-xl overflow-x-auto text-xs font-mono text-slate-300">
            <pre>{JSON.stringify(session, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
};
