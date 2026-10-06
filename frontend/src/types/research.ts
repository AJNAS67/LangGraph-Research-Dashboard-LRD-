export type ResearchDepth = 'quick' | 'standard' | 'deep';

export type NodeStatus = 'pending' | 'active' | 'completed' | 'failed' | 'skipped';

export type SessionStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

export interface Subtask {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  queries: string[];
}

export interface CollectedSource {
  id: string;
  title: string;
  url: string;
  source_type: 'web' | 'academic' | 'document' | 'news';
  summary: string;
  relevance_score: number;
  retrieved_at: string;
  raw_metadata?: Record<string, any>;
}

export interface AnalysisResult {
  synthesized_findings: string[];
  agreements: string[];
  contradictions: string[];
  observed_gaps: string[];
}

export interface ValidationResult {
  status: 'VALID' | 'NEEDS_MORE_RESEARCH' | 'FAILED';
  reason: string;
  needs_more_research: boolean;
  missing_aspects: string[];
  suggested_queries: string[];
}

export interface FinalReport {
  title: string;
  executive_summary: string;
  methodology: string;
  key_findings: string[];
  detailed_analysis: string;
  contradictions: string[];
  limitations: string[];
  conclusion: string;
  sources_cited: string[];
  raw_markdown: string;
}

export interface ResearchSession {
  id: string;
  title: string;
  user_query: string;
  additional_instructions?: string;
  research_depth: ResearchDepth;
  status: SessionStatus;
  current_node: 'planner' | 'researcher' | 'analyzer' | 'validator' | 'report_generator' | 'completed';
  retry_count: number;
  max_retries: number;
  research_objective: string;
  subtasks: Subtask[];
  collected_sources: CollectedSource[];
  analysis?: AnalysisResult;
  validation_result?: ValidationResult;
  final_report?: FinalReport;
  created_at: string;
  completed_at?: string;
}
