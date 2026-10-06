import React from 'react';
import { Subtask } from '../../types/research';
import { CheckCircle2, Clock, CircleDot, Search, Target } from 'lucide-react';

interface ResearchPlanViewerProps {
  objective: string;
  subtasks: Subtask[];
}

export const ResearchPlanViewer: React.FC<ResearchPlanViewerProps> = ({
  objective,
  subtasks,
}) => {
  return (
    <div className="space-y-6">
      {/* Objective Card */}
      <div className="glass-panel rounded-xl p-5 border-l-4 border-l-indigo-500">
        <div className="flex items-center gap-2 text-indigo-400 font-medium text-xs uppercase tracking-wider mb-1">
          <Target className="w-4 h-4" /> Synthesized Research Objective
        </div>
        <p className="text-slate-200 text-sm leading-relaxed">
          {objective || "Decomposing user research query..."}
        </p>
      </div>

      {/* Subtasks List */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs text-slate-400 px-1">
          <span className="font-semibold uppercase tracking-wider">Planned Subtasks ({subtasks.length})</span>
          <span>Sequential execution</span>
        </div>

        {subtasks.map((st, index) => {
          const isDone = st.status === 'completed';
          const isInProgress = st.status === 'in_progress';

          return (
            <div
              key={st.id || index}
              className={`glass-panel rounded-xl p-4 transition-all duration-200 ${
                isInProgress
                  ? 'border-indigo-500/50 bg-indigo-950/20 glow-primary'
                  : 'hover:border-slate-700'
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-start gap-3">
                  <div className="mt-0.5">
                    {isDone ? (
                      <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    ) : isInProgress ? (
                      <Clock className="w-5 h-5 text-indigo-400 animate-spin" />
                    ) : (
                      <CircleDot className="w-5 h-5 text-slate-400" />
                    )}
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
                      <span className="text-xs text-slate-400 font-mono">#{index + 1}</span>
                      {st.title}
                    </h4>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                      {st.description}
                    </p>

                    {/* Queries chips */}
                    {st.queries && st.queries.length > 0 && (
                      <div className="flex flex-wrap items-center gap-1.5 mt-3">
                        <span className="text-[11px] text-slate-400 flex items-center gap-1 mr-1">
                          <Search className="w-3 h-3" /> Search Queries:
                        </span>
                        {st.queries.map((q, qIdx) => (
                          <span
                            key={qIdx}
                            className="text-[11px] font-mono px-2 py-0.5 rounded-md bg-slate-800 text-sky-300 border border-slate-700/60"
                          >
                            "{q}"
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* Status Badge */}
                <div>
                  {isDone && (
                    <span className="text-[11px] font-medium text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20 whitespace-nowrap">
                      Completed
                    </span>
                  )}
                  {isInProgress && (
                    <span className="text-[11px] font-medium text-indigo-300 bg-indigo-500/20 px-2.5 py-1 rounded-full border border-indigo-500/30 whitespace-nowrap animate-pulse">
                      In Progress
                    </span>
                  )}
                  {st.status === 'pending' && (
                    <span className="text-[11px] text-slate-400 bg-slate-800/80 px-2.5 py-1 rounded-full whitespace-nowrap">
                      Queued
                    </span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
