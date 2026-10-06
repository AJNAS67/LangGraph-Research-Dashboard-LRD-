import React from 'react';
import { CheckCircle2, Clock, RotateCcw, AlertCircle, Sparkles, Database, Search, Cpu, FileText } from 'lucide-react';

interface GraphVisualizerProps {
  currentNode: string;
  status: string;
  retryCount?: number;
  maxRetries?: number;
}

interface NodeDef {
  id: string;
  label: string;
  sublabel: string;
  icon: React.ReactNode;
  order: number;
}

const NODES: NodeDef[] = [
  { id: 'planner', label: 'Planner', sublabel: 'Decomposes query', icon: <Sparkles className="w-4 h-4" />, order: 0 },
  { id: 'researcher', label: 'Researcher', sublabel: 'Web search & sources', icon: <Search className="w-4 h-4" />, order: 1 },
  { id: 'analyzer', label: 'Analyzer', sublabel: 'Cross-analysis', icon: <Cpu className="w-4 h-4" />, order: 2 },
  { id: 'validator', label: 'Validator', sublabel: 'Sufficiency check', icon: <AlertCircle className="w-4 h-4" />, order: 3 },
  { id: 'report_generator', label: 'Report Generator', sublabel: 'Synthesizes report', icon: <FileText className="w-4 h-4" />, order: 4 },
];

export const GraphVisualizer: React.FC<GraphVisualizerProps> = ({
  currentNode,
  status,
  retryCount = 0,
  maxRetries = 2,
}) => {
  const currentOrder = currentNode === 'completed' 
    ? 99 
    : (NODES.find(n => n.id === currentNode)?.order ?? -1);

  return (
    <div className="glass-panel rounded-2xl p-6 relative overflow-hidden">
      {/* Background ambient lighting */}
      <div className="absolute top-0 right-1/4 w-96 h-32 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-1/4 w-96 h-32 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="flex items-center justify-between mb-8">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <h3 className="text-base font-semibold text-slate-100 tracking-wide uppercase text-xs">
              LangGraph State Machine Topology
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time execution graph with cyclical validation feedback
          </p>
        </div>

        {retryCount > 0 && (
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs">
            <RotateCcw className="w-3.5 h-3.5 animate-spin-slow" />
            <span>Refinement Loop: {retryCount} / {maxRetries}</span>
          </div>
        )}
      </div>

      {/* Workflow nodes container */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative">
        {NODES.map((node, idx) => {
          const isCompleted = currentOrder > node.order || status === 'completed';
          const isActive = currentNode === node.id && status !== 'completed';
          const isPending = currentOrder < node.order && status !== 'completed';

          return (
            <div key={node.id} className="relative group">
              {/* Card node */}
              <div
                className={`p-4 rounded-xl transition-all duration-300 border relative ${
                  isActive
                    ? 'bg-indigo-950/60 border-indigo-500 glow-primary scale-105 z-10'
                    : isCompleted
                    ? 'bg-slate-900/80 border-emerald-500/40 hover:border-emerald-500/70'
                    : 'bg-slate-900/40 border-slate-800/80 opacity-60'
                }`}
              >
                {/* Node header with status badge */}
                <div className="flex items-center justify-between mb-3">
                  <div
                    className={`p-2 rounded-lg ${
                      isActive
                        ? 'bg-indigo-600 text-white'
                        : isCompleted
                        ? 'bg-emerald-500/20 text-emerald-400'
                        : 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {node.icon}
                  </div>

                  {isCompleted && (
                    <span className="flex items-center gap-1 text-[11px] font-medium text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                      <CheckCircle2 className="w-3 h-3" /> Done
                    </span>
                  )}
                  {isActive && (
                    <span className="flex items-center gap-1 text-[11px] font-medium text-indigo-300 bg-indigo-500/20 px-2 py-0.5 rounded-full border border-indigo-500/30 animate-pulse">
                      <Clock className="w-3 h-3 animate-spin" /> Running
                    </span>
                  )}
                  {isPending && (
                    <span className="text-[11px] text-slate-400 bg-slate-800/60 px-2 py-0.5 rounded-full">
                      Pending
                    </span>
                  )}
                </div>

                {/* Node titles */}
                <div className="font-medium text-sm text-slate-100">{node.label}</div>
                <div className="text-xs text-slate-400 mt-1">{node.sublabel}</div>

                {/* Step indicator */}
                <div className="mt-3 pt-2.5 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-400">
                  <span>Step {idx + 1} of 5</span>
                  {isActive && <span className="text-indigo-400 font-semibold">Active</span>}
                </div>
              </div>

              {/* Connecting forward line between cards (desktop view) */}
              {idx < NODES.length - 1 && (
                <div className="hidden md:block absolute top-1/2 -right-3 transform -translate-y-1/2 z-0">
                  <div className={`w-3 h-0.5 ${isCompleted ? 'bg-emerald-500/60' : 'bg-slate-800'}`} />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Visual representation of the conditional feedback loop */}
      <div className="mt-6 pt-4 border-t border-slate-800/60 flex flex-wrap items-center justify-between text-xs text-slate-400">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-indigo-500" />
          <span>Conditional Routing:</span>
          <span className="text-slate-300 font-mono">Validator ➔ Researcher</span>
          <span className="text-slate-400">if information gaps detected & retries &lt; {maxRetries}</span>
        </div>

        <div className="flex items-center gap-4 text-[11px]">
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <span>Completed</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
            <span>Active</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-slate-700" />
            <span>Queued</span>
          </div>
        </div>
      </div>
    </div>
  );
};
