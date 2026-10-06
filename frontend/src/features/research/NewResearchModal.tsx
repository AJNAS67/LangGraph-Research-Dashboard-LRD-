import React, { useState } from 'react';
import { X, Sparkles, Zap, Layers, Compass, Upload, AlertCircle } from 'lucide-react';
import { ResearchDepth } from '../../types/research';

interface NewResearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: { query: string; instructions: string; depth: ResearchDepth }) => void;
}

export const NewResearchModal: React.FC<NewResearchModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
}) => {
  const [query, setQuery] = useState('');
  const [instructions, setInstructions] = useState('');
  const [depth, setDepth] = useState<ResearchDepth>('standard');
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || query.trim().length < 10) {
      setError('Please enter a research question of at least 10 characters.');
      return;
    }
    setError('');
    onSubmit({ query: query.trim(), instructions: instructions.trim(), depth });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="glass-panel-elevated w-full max-w-xl rounded-2xl p-6 relative shadow-2xl animate-in fade-in zoom-in-95 duration-150">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 text-slate-400 hover:text-slate-200 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-5">
          <div className="p-2 rounded-xl bg-indigo-600/30 text-indigo-400 border border-indigo-500/40">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-100">Initialize Autonomous Research</h3>
            <p className="text-xs text-slate-400">Launch a multi-step LangGraph research investigation</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Query input */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              Research Question <span className="text-indigo-400">*</span>
            </label>
            <textarea
              rows={3}
              placeholder="e.g. Research the impact of AI coding assistants on software developer productivity in 2026, compare major tools, and evaluate enterprise risks."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-xs text-slate-100 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 resize-none"
            />
            {error && (
              <p className="text-[11px] text-rose-400 mt-1 flex items-center gap-1">
                <AlertCircle className="w-3.5 h-3.5" /> {error}
              </p>
            )}
          </div>

          {/* Additional Instructions */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              Additional Scope & Guidance (Optional)
            </label>
            <input
              type="text"
              placeholder="e.g. Focus specifically on enterprise data governance and token leakage benchmarks."
              value={instructions}
              onChange={(e) => setInstructions(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl bg-slate-900/90 border border-slate-700 text-xs text-slate-100 placeholder-slate-400 focus:outline-none focus:border-indigo-500"
            />
          </div>

          {/* Research Depth Selection */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
              Research Depth
            </label>
            <div className="grid grid-cols-3 gap-2.5">
              {[
                { id: 'quick', label: 'Quick', desc: '2 subtasks • ~4 sources', icon: <Zap className="w-3.5 h-3.5 text-amber-400" /> },
                { id: 'standard', label: 'Standard', desc: '3 subtasks • ~8 sources', icon: <Layers className="w-3.5 h-3.5 text-indigo-400" /> },
                { id: 'deep', label: 'Deep', desc: '5 subtasks • ~15 sources', icon: <Compass className="w-3.5 h-3.5 text-emerald-400" /> },
              ].map((lvl) => (
                <button
                  type="button"
                  key={lvl.id}
                  onClick={() => setDepth(lvl.id as ResearchDepth)}
                  className={`p-3 rounded-xl border text-left transition-all ${
                    depth === lvl.id
                      ? 'bg-indigo-950/60 border-indigo-500 text-white glow-primary'
                      : 'bg-slate-900/40 border-slate-800 text-slate-300 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center gap-1.5 text-xs font-semibold">
                    {lvl.icon} {lvl.label}
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1">{lvl.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Optional Document Upload Placeholder (Phase 9 preview) */}
          <div className="p-3 rounded-xl border border-dashed border-slate-800 text-center bg-slate-900/20">
            <Upload className="w-4 h-4 mx-auto text-slate-400 mb-1" />
            <div className="text-[11px] text-slate-400">
              <span className="text-indigo-400 font-medium">Attach PDF/Doc</span> for RAG grounding (Phase 9 preview)
            </div>
          </div>

          {/* Submit CTA */}
          <div className="pt-2 flex items-center justify-end gap-2.5">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white transition-all shadow-md shadow-indigo-600/30"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Launch Research Workflow</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
