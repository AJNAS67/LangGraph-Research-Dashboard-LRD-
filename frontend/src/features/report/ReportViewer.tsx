import React, { useState } from 'react';
import { FinalReport } from '../../types/research';
import { Copy, Check, Download, AlertTriangle, FileText, CheckCircle2, BookOpen } from 'lucide-react';

interface ReportViewerProps {
  report?: FinalReport;
}

export const ReportViewer: React.FC<ReportViewerProps> = ({ report }) => {
  const [copied, setCopied] = useState(false);

  if (!report) {
    return (
      <div className="glass-panel rounded-2xl p-12 text-center text-slate-400">
        <FileText className="w-10 h-10 mx-auto mb-3 opacity-40 text-indigo-400" />
        <h4 className="text-sm font-semibold text-slate-200">Final Report in Synthesis</h4>
        <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
          The research workflow is actively collecting and analyzing data. The structured report will be automatically generated upon validation completion.
        </p>
      </div>
    );
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(report.raw_markdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([report.raw_markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${report.title.toLowerCase().replace(/[^a-z0-9]/g, '-')}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="space-y-6">
      {/* Report Header & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-5 rounded-2xl">
        <div>
          <span className="text-[11px] font-semibold uppercase tracking-wider text-indigo-400 bg-indigo-500/10 px-2.5 py-0.5 rounded-full border border-indigo-500/20">
            Validated Synthesis
          </span>
          <h2 className="text-lg font-bold text-slate-100 mt-2">{report.title}</h2>
          <p className="text-xs text-slate-400 mt-0.5">{report.methodology}</p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 text-slate-200 hover:bg-slate-700 transition-colors border border-slate-700/60"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy MD'}</span>
          </button>
          <button
            onClick={handleDownload}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-indigo-600 text-white hover:bg-indigo-500 transition-colors shadow-sm"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download</span>
          </button>
        </div>
      </div>

      {/* Executive Summary */}
      <div className="glass-panel p-5 rounded-xl border-l-4 border-l-indigo-500">
        <h3 className="text-xs font-bold uppercase tracking-wider text-indigo-300 mb-2">
          Executive Summary
        </h3>
        <p className="text-sm text-slate-200 leading-relaxed font-normal">
          {report.executive_summary}
        </p>
      </div>

      {/* Key Findings */}
      <div className="glass-panel p-5 rounded-xl">
        <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-3 flex items-center gap-1.5">
          <CheckCircle2 className="w-4 h-4" /> Key Findings & Takeaways
        </h3>
        <ul className="space-y-2">
          {report.key_findings.map((finding, idx) => (
            <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-200">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 flex-shrink-0" />
              <span>{finding}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Contradictions & Discrepancies */}
      {report.contradictions && report.contradictions.length > 0 && (
        <div className="glass-panel p-5 rounded-xl border border-amber-500/30 bg-amber-950/10">
          <h3 className="text-xs font-bold uppercase tracking-wider text-amber-400 mb-3 flex items-center gap-1.5">
            <AlertTriangle className="w-4 h-4" /> Detected Contradictions & Discrepancies
          </h3>
          <ul className="space-y-2">
            {report.contradictions.map((contra, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs text-amber-200/90">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 flex-shrink-0" />
                <span>{contra}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Detailed Analysis Content */}
      <div className="glass-panel p-6 rounded-xl">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">
          Detailed Analytical Synthesis
        </h3>
        <div className="prose prose-invert prose-sm max-w-none text-slate-300 leading-relaxed space-y-4 whitespace-pre-line font-sans">
          {report.detailed_analysis}
        </div>
      </div>

      {/* Conclusion & Strategic Outlook */}
      <div className="glass-panel p-5 rounded-xl border-l-4 border-l-sky-500">
        <h3 className="text-xs font-bold uppercase tracking-wider text-sky-400 mb-2">
          Conclusion & Strategic Outlook
        </h3>
        <p className="text-xs text-slate-200 leading-relaxed">
          {report.conclusion}
        </p>
      </div>

      {/* Cited Sources */}
      {report.sources_cited && report.sources_cited.length > 0 && (
        <div className="glass-panel p-4 rounded-xl text-xs text-slate-400">
          <div className="flex items-center gap-1.5 font-semibold text-slate-300 mb-2">
            <BookOpen className="w-3.5 h-3.5 text-indigo-400" /> Cited Reference URLs ({report.sources_cited.length})
          </div>
          <div className="flex flex-wrap gap-2">
            {report.sources_cited.map((url, idx) => (
              <a
                key={idx}
                href={url}
                target="_blank"
                rel="noreferrer"
                className="text-[11px] font-mono px-2 py-1 rounded bg-slate-900 text-sky-400 hover:underline border border-slate-800"
              >
                {url}
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
