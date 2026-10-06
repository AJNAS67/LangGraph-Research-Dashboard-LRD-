import React from 'react';
import { ResearchSession } from '../types/research';
import { DashboardStats } from '../features/dashboard/DashboardStats';
import { Sparkles, ArrowRight, Activity, CheckCircle2, Clock, RotateCcw } from 'lucide-react';

interface DashboardPageProps {
  sessions: ResearchSession[];
  onSelectSession: (session: ResearchSession) => void;
  onOpenNewModal: () => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  sessions,
  onSelectSession,
  onOpenNewModal,
}) => {
  const activeSession = sessions.find(s => s.status === 'running');

  return (
    <div className="space-y-8">
      {/* Hero Welcome Banner */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl relative overflow-hidden border border-slate-800">
        <div className="absolute top-0 right-0 w-80 h-80 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-medium mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Autonomous Multi-Step AI Research Engine</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight leading-snug">
            Deep Web Research Orchestrated by LangGraph
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 mt-2 leading-relaxed">
            Submit complex engineering and architectural questions. LRD creates structured subtasks, retrieves real-time sources, cross-examines findings, and validates sufficiency before report synthesis.
          </p>

          <div className="mt-5 flex items-center gap-3">
            <button
              onClick={onOpenNewModal}
              className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white transition-all shadow-lg shadow-indigo-600/25"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Start New Research</span>
            </button>
          </div>
        </div>
      </div>

      {/* Operational Metrics */}
      <DashboardStats sessions={sessions} />

      {/* Active Workflow Spotlight (if any is running) */}
      {activeSession && (
        <div className="glass-panel p-5 rounded-2xl border-l-4 border-l-sky-500 bg-sky-950/10">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-sky-400 animate-ping" />
                <span className="text-xs font-semibold uppercase text-sky-400 tracking-wider">
                  Active Workflow in Progress
                </span>
                <span className="text-xs font-mono text-slate-400">Node: [{activeSession.current_node}]</span>
              </div>
              <h3 className="text-sm font-bold text-slate-100 mt-1">{activeSession.title}</h3>
              <p className="text-xs text-slate-400 mt-0.5 line-clamp-1">{activeSession.user_query}</p>
            </div>

            <button
              onClick={() => onSelectSession(activeSession)}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-sky-600 hover:bg-sky-500 text-white transition-colors self-start sm:self-center"
            >
              <span>Inspect Workflow</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Recent Research Sessions List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300">
            Recent Research Sessions
          </h2>
          <span className="text-xs text-slate-400">{sessions.length} sessions recorded</span>
        </div>

        <div className="grid grid-cols-1 gap-3">
          {sessions.map((session) => (
            <div
              key={session.id}
              onClick={() => onSelectSession(session)}
              className="glass-panel p-4 rounded-xl hover:border-indigo-500/50 transition-all duration-200 cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full border ${
                    session.status === 'completed'
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                      : 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20 animate-pulse'
                  }`}>
                    {session.status}
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">
                    Depth: {session.research_depth}
                  </span>
                  {session.retry_count > 0 && (
                    <span className="text-[10px] text-amber-400 flex items-center gap-1 bg-amber-500/10 px-1.5 py-0.5 rounded">
                      <RotateCcw className="w-3 h-3" /> {session.retry_count} loops
                    </span>
                  )}
                </div>

                <h3 className="text-sm font-semibold text-slate-200 group-hover:text-indigo-300 transition-colors">
                  {session.title}
                </h3>
                <p className="text-xs text-slate-400 line-clamp-1">{session.user_query}</p>
              </div>

              <div className="flex items-center gap-4 text-xs text-slate-400 self-end sm:self-center font-mono">
                <span>{session.collected_sources?.length || 0} sources</span>
                <span className="hidden md:inline">{new Date(session.created_at).toLocaleDateString()}</span>
                <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-indigo-400 transition-transform group-hover:translate-x-1" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
