import React from 'react';
import { Layers, Activity, CheckCircle2, Globe, TrendingUp } from 'lucide-react';
import { ResearchSession } from '../../types/research';

interface DashboardStatsProps {
  sessions: ResearchSession[];
}

export const DashboardStats: React.FC<DashboardStatsProps> = ({ sessions }) => {
  const total = sessions.length;
  const running = sessions.filter(s => s.status === 'running').length;
  const completed = sessions.filter(s => s.status === 'completed').length;
  const totalSources = sessions.reduce((acc, s) => acc + (s.collected_sources?.length || 0), 0);

  const stats = [
    { label: 'Total Research Tasks', value: total, icon: <Layers className="w-4 h-4 text-indigo-400" />, change: '+100% autonomous' },
    { label: 'Active Workflows', value: running, icon: <Activity className="w-4 h-4 text-sky-400 animate-pulse" />, change: 'LangGraph engine' },
    { label: 'Completed Reports', value: completed, icon: <CheckCircle2 className="w-4 h-4 text-emerald-400" />, change: 'Fully cited' },
    { label: 'Total Verified Sources', value: totalSources, icon: <Globe className="w-4 h-4 text-amber-400" />, change: 'Web & academic' },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {stats.map((stat, idx) => (
        <div key={idx} className="glass-panel p-4 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400 font-medium">{stat.label}</span>
            <div className="p-1.5 rounded-lg bg-slate-800/80">{stat.icon}</div>
          </div>
          <div className="text-2xl font-bold text-slate-100">{stat.value}</div>
          <div className="text-[11px] text-slate-400 mt-1 flex items-center gap-1 font-mono">
            <TrendingUp className="w-3 h-3 text-indigo-400" /> {stat.change}
          </div>
        </div>
      ))}
    </div>
  );
};
