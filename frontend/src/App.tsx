import React, { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppLayout } from './layouts/AppLayout';
import { DashboardPage } from './pages/DashboardPage';
import { HistoryPage } from './pages/HistoryPage';
import { SessionDetailPage } from './pages/SessionDetailPage';
import { NewResearchModal } from './features/research/NewResearchModal';
import { INITIAL_MOCK_SESSIONS } from './services/mockData';
import { ResearchSession, ResearchDepth } from './types/research';

const queryClient = new QueryClient();

export function App() {
  const [sessions, setSessions] = useState<ResearchSession[]>(INITIAL_MOCK_SESSIONS);
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'history'>('dashboard');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const selectedSession = sessions.find((s) => s.id === selectedSessionId);

  // Launch a new research session and simulate real-time LangGraph step progression
  const handleLaunchResearch = ({
    query,
    instructions,
    depth,
  }: {
    query: string;
    instructions: string;
    depth: ResearchDepth;
  }) => {
    const newId = `session_${Date.now()}`;
    const newSession: ResearchSession = {
      id: newId,
      title: query.slice(0, 70) + (query.length > 70 ? '...' : ''),
      user_query: query,
      additional_instructions: instructions,
      research_depth: depth,
      status: 'running',
      current_node: 'planner',
      retry_count: 0,
      max_retries: 2,
      research_objective: `Analyze and synthesize empirical evidence regarding: ${query}`,
      created_at: new Date().toISOString(),
      subtasks: [
        {
          id: 'st_1',
          title: 'Primary Domain Formulation',
          description: 'Extract core architectural questions and isolate search keywords.',
          status: 'in_progress',
          queries: [query.slice(0, 50)],
        },
        {
          id: 'st_2',
          title: 'Evidence Gathering & Cross-Comparison',
          description: 'Collect multi-source benchmarks and evaluate discrepancies.',
          status: 'pending',
          queries: [`${query.slice(0, 30)} benchmarks 2026`],
        },
      ],
      collected_sources: [],
    };

    setSessions((prev) => [newSession, ...prev]);
    setSelectedSessionId(newId);

    // Simulate LangGraph node stepping for interactive visual feedback
    setTimeout(() => {
      setSessions((prev) =>
        prev.map((s) =>
          s.id === newId
            ? {
                ...s,
                current_node: 'researcher',
                subtasks: s.subtasks.map((st, i) =>
                  i === 0 ? { ...st, status: 'completed' } : { ...st, status: 'in_progress' }
                ),
                collected_sources: [
                  {
                    id: 'src_live_1',
                    title: `Primary Benchmark Report: ${query.slice(0, 40)}`,
                    url: 'https://research.techbenchmarks.org/analysis-2026',
                    source_type: 'web',
                    summary: `Empirical evaluation on ${query.slice(0, 30)} shows 30% performance divergence under stress testing.`,
                    relevance_score: 0.94,
                    retrieved_at: new Date().toISOString(),
                  },
                ],
              }
            : s
        )
      );
    }, 2500);

    setTimeout(() => {
      setSessions((prev) =>
        prev.map((s) =>
          s.id === newId
            ? {
                ...s,
                current_node: 'analyzer',
                subtasks: s.subtasks.map((st) => ({ ...st, status: 'completed' })),
                collected_sources: [
                  ...s.collected_sources,
                  {
                    id: 'src_live_2',
                    title: `Security & Compliance Audit: ${query.slice(0, 40)}`,
                    url: 'https://infosec-journal.org/compliance-2026',
                    source_type: 'academic',
                    summary: 'Enterprise audit highlights strict governance requirements and access isolation.',
                    relevance_score: 0.91,
                    retrieved_at: new Date().toISOString(),
                  },
                ],
              }
            : s
        )
      );
    }, 5500);

    setTimeout(() => {
      setSessions((prev) =>
        prev.map((s) =>
          s.id === newId
            ? {
                ...s,
                current_node: 'validator',
                validation_result: {
                  status: 'VALID',
                  reason: 'Sufficient evidence collected across all subtasks.',
                  needs_more_research: false,
                  missing_aspects: [],
                  suggested_queries: [],
                },
              }
            : s
        )
      );
    }, 8500);

    setTimeout(() => {
      setSessions((prev) =>
        prev.map((s) =>
          s.id === newId
            ? {
                ...s,
                status: 'completed',
                current_node: 'completed',
                completed_at: new Date().toISOString(),
                final_report: {
                  title: `Research Report: ${query.slice(0, 60)}`,
                  executive_summary: `This report details key findings and empirical analysis for: ${query}.`,
                  methodology: 'Autonomous multi-query retrieval and cross-source synthesis via LangGraph.',
                  key_findings: [
                    'Multi-source evidence reveals key operational advantages in 2026 benchmarks.',
                    'Security governance and token privacy remain the primary architectural priority.',
                  ],
                  detailed_analysis: `### In-Depth Investigation\n\nAutomated analysis indicates that organizations adopting modern tools experience measurable velocity gains with disciplined governance.\n\n### Architectural Synthesis\n\nCross-examination of evidence corroborates high developer efficiency while emphasizing the need for isolated VPC gateways.`,
                  contradictions: [
                    'Discrepancies observed between early vendor marketing claims and empirical audit data.',
                  ],
                  limitations: [
                    'Research depth bounded to standard search window.',
                  ],
                  conclusion: 'Implementation should proceed with clear governance boundaries and continuous evaluation.',
                  sources_cited: [
                    'https://research.techbenchmarks.org/analysis-2026',
                    'https://infosec-journal.org/compliance-2026',
                  ],
                  raw_markdown: `# Research Report: ${query}\n\n## Executive Summary\nAnalysis completed autonomously via LangGraph.\n\n## Key Findings\n- High velocity measured.\n- Strict governance needed.`,
                },
              }
            : s
        )
      );
    }, 11500);
  };

  return (
    <QueryClientProvider client={queryClient}>
      <AppLayout
        activeTab={activeTab}
        onSelectTab={(tab) => {
          setSelectedSessionId(null);
          setActiveTab(tab);
        }}
        onOpenNewModal={() => setIsModalOpen(true)}
      >
        {selectedSession ? (
          <SessionDetailPage
            session={selectedSession}
            onBack={() => setSelectedSessionId(null)}
          />
        ) : activeTab === 'dashboard' ? (
          <DashboardPage
            sessions={sessions}
            onSelectSession={(s) => setSelectedSessionId(s.id)}
            onOpenNewModal={() => setIsModalOpen(true)}
          />
        ) : (
          <HistoryPage
            sessions={sessions}
            onSelectSession={(s) => setSelectedSessionId(s.id)}
          />
        )}

        <NewResearchModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSubmit={handleLaunchResearch}
        />
      </AppLayout>
    </QueryClientProvider>
  );
}

export default App;
