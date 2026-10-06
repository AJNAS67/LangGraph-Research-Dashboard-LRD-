import { ResearchSession } from '../types/research';

export const INITIAL_MOCK_SESSIONS: ResearchSession[] = [
  {
    id: "session_001_active",
    title: "AI Coding Assistant Velocity & Enterprise Security Risks (2026)",
    user_query: "Compare state-of-the-art AI coding tools in 2026, their productivity benchmarks, data security trade-offs, and enterprise adoption barriers.",
    additional_instructions: "Emphasize enterprise token governance and zero-data-retention VPC options.",
    research_depth: "standard",
    status: "running",
    current_node: "researcher",
    retry_count: 0,
    max_retries: 2,
    research_objective: "Investigate developer velocity metrics, security governance protocols, and benchmark empirical productivity gains of 2026 AI coding assistants.",
    created_at: new Date(Date.now() - 45000).toISOString(),
    subtasks: [
      {
        id: "subtask_1",
        title: "Developer Velocity & Throughput Benchmarks",
        description: "Analyze empirical measurements of pull request cycle times, boilerplate automation, and unit test generation.",
        status: "completed",
        queries: ["ai coding assistant developer velocity benchmarks 2026", "empirical productivity metrics code generation"],
      },
      {
        id: "subtask_2",
        title: "Enterprise Data Governance & Token Privacy",
        description: "Investigate token leakage vectors, SOC2 Type II LLM compliance, and private VPC deployment strategies.",
        status: "in_progress",
        queries: ["enterprise AI code generation data leaks governance", "air-gapped LLM code assistant compliance"],
      },
      {
        id: "subtask_3",
        title: "Comparative Architectural Trade-offs",
        description: "Cross-reference context window limitations, AST-aware caching, and local vs cloud model trade-offs.",
        status: "pending",
        queries: ["local vs cloud AI coding models 2026 comparison", "context window code repository indexing"],
      },
    ],
    collected_sources: [
      {
        id: "src_101",
        title: "Empirical Developer Velocity Study: AI Code Pairings in 2026",
        url: "https://research.techbenchmarks.org/ai-developer-velocity-2026",
        source_type: "academic",
        summary: "Controlled cohort analysis of 1,200 engineers across 14 enterprise codebases demonstrated a 28% median acceleration in routine feature delivery, primarily driven by automated unit test scaffolding.",
        relevance_score: 0.96,
        retrieved_at: new Date(Date.now() - 30000).toISOString(),
      },
      {
        id: "src_102",
        title: "State of Enterprise Infosec in AI Assisted Development",
        url: "https://infosec-journal.org/ai-risks-governance-2026",
        source_type: "news",
        summary: "Over 52% of enterprise CISOs surveyed require zero-data-retention guarantees or self-hosted model inference due to compliance constraints regarding proprietary intellectual property.",
        relevance_score: 0.91,
        retrieved_at: new Date(Date.now() - 15000).toISOString(),
      },
      {
        id: "src_103",
        title: "Code Review Quality & Silent Bug Injection Rates",
        url: "https://ieee-software.org/code-quality-ai-assistants",
        source_type: "academic",
        summary: "Analysis indicates a 14% rise in subtle edge-case bugs that pass automated test suites, highlighting the critical importance of rigorous human code review.",
        relevance_score: 0.89,
        retrieved_at: new Date(Date.now() - 5000).toISOString(),
      },
    ],
  },
  {
    id: "session_002_completed",
    title: "Kubernetes vs Nomad: Modern Cloud Orchestration Trade-offs",
    user_query: "Compare Kubernetes and HashiCorp Nomad for high-scale microservices, operational complexity, and cloud cost efficiency in 2026.",
    research_depth: "standard",
    status: "completed",
    current_node: "completed",
    retry_count: 1,
    max_retries: 2,
    research_objective: "Provide an objective comparative evaluation of Kubernetes vs Nomad across operational cognitive load, control plane scalability, resource utilization, and ecosystem maturity.",
    created_at: new Date(Date.now() - 3600000).toISOString(),
    completed_at: new Date(Date.now() - 3420000).toISOString(),
    subtasks: [
      {
        id: "st_1",
        title: "Operational Complexity and Maintenance Footprint",
        description: "Compare control plane operational overhead, upgrades, and required SRE staffing.",
        status: "completed",
        queries: ["kubernetes vs nomad operational overhead 2026"],
      },
      {
        id: "st_2",
        title: "Resource Efficiency and Infrastructure Cost",
        description: "Evaluate scheduler memory footprints, binary size, and bare-metal density.",
        status: "completed",
        queries: ["nomad scheduler bare metal density cost efficiency"],
      },
    ],
    collected_sources: [
      {
        id: "src_201",
        title: "SRE Benchmark: Orchestration Overhead in Production",
        url: "https://cloud-native-systems.io/nomad-k8s-benchmark",
        source_type: "academic",
        summary: "Nomad clusters demonstrated 70% lower control-plane memory consumption compared to equivalent K8s control planes, while Kubernetes offered superior CRD ecosystem extensibility.",
        relevance_score: 0.95,
        retrieved_at: new Date(Date.now() - 3550000).toISOString(),
      },
      {
        id: "src_202",
        title: "Enterprise Microservices Infrastructure Survey 2026",
        url: "https://devops-metrics.org/cloud-orchestration-trends",
        source_type: "web",
        summary: "88% of Fortune 500 engineering teams standardize on Kubernetes due to managed cloud offerings (EKS/GKE), while Nomad maintains strong adoption in low-latency bare-metal clusters.",
        relevance_score: 0.92,
        retrieved_at: new Date(Date.now() - 3500000).toISOString(),
      },
    ],
    analysis: {
      synthesized_findings: [
        "Kubernetes remains the industry standard for cloud-native ecosystems due to managed offerings.",
        "Nomad provides significantly lower operational overhead and memory consumption for teams running hybrid or bare-metal environments.",
      ],
      agreements: [
        "Both systems provide robust automated rescheduling and high-availability workload placement.",
      ],
      contradictions: [
        "Vendor documentation claims equivalent setup effort, whereas third-party audits show K8s requires 3x higher SRE specialization.",
      ],
      observed_gaps: [
        "Edge computing benchmarks remain fragmented across hardware classes.",
      ],
    },
    validation_result: {
      status: "VALID",
      reason: "Comprehensive multi-axis evidence collected across operational cost, ecosystem maturity, and developer experience.",
      needs_more_research: false,
      missing_aspects: [],
      suggested_queries: [],
    },
    final_report: {
      title: "Strategic Evaluation: Kubernetes vs Nomad for Modern Cloud Orchestration",
      executive_summary: "This report examines the operational, architectural, and financial trade-offs between Kubernetes and HashiCorp Nomad. While Kubernetes dominates managed cloud environments, Nomad offers compelling advantages in simplicity and resource density for specialized and bare-metal workloads.",
      methodology: "Cross-source synthesis of 2026 production benchmarks, telemetry reports, and SRE surveys.",
      key_findings: [
        "Nomad control planes require up to 70% less memory overhead than Kubernetes.",
        "Kubernetes benefits from universal ecosystem support, Helm charts, and cloud-native operators.",
        "Nomad drastically reduces operational cognitive load for teams lacking dedicated platform engineering teams.",
      ],
      detailed_analysis: "### 1. Architectural Architecture\nNomad operates as a single unified binary combining scheduling and cluster orchestration...\n\n### 2. Operational Cost & Cognitive Load\nKubernetes requires dedicated management of API servers, etcd, kubelets, and ingress controllers...",
      contradictions: [
        "Vendor claims of turnkey Kubernetes management contradict independent survey data showing significant ongoing operational drag.",
      ],
      limitations: [
        "Long-term license implications following HashiCorp's BSL licensing model must be continuously evaluated.",
      ],
      conclusion: "Organizations with dedicated SRE teams and heavy reliance on cloud-managed services should continue with Kubernetes. Teams operating hybrid infrastructure or seeking minimal operational overhead should strongly evaluate Nomad.",
      sources_cited: [
        "https://cloud-native-systems.io/nomad-k8s-benchmark",
        "https://devops-metrics.org/cloud-orchestration-trends",
      ],
      raw_markdown: `# Strategic Evaluation: Kubernetes vs Nomad for Modern Cloud Orchestration

## Executive Summary
This report examines the operational, architectural, and financial trade-offs between Kubernetes and HashiCorp Nomad. While Kubernetes dominates managed cloud environments, Nomad offers compelling advantages in simplicity and resource density for specialized and bare-metal workloads.

## Key Findings
- **Operational Density**: Nomad control planes require up to 70% less memory overhead than Kubernetes.
- **Ecosystem Dominance**: Kubernetes benefits from universal ecosystem support, Helm charts, and cloud-native operators.
- **Platform Simplicity**: Nomad drastically reduces operational cognitive load for teams lacking dedicated platform engineering teams.

## Detailed Analysis
### Architectural Comparison
Nomad operates as a single lightweight binary combining scheduling and cluster orchestration. Kubernetes employs a distributed control plane with etcd, kube-apiserver, kube-scheduler, and kube-controller-manager.

### SRE Overhead & Cognitive Load
Organizations utilizing Nomad report median onboarding durations of under 2 days for application developers, compared to 2-3 weeks for developers configuring Kubernetes manifests.

## Discrepancies & Contradictions
- Vendor claims of turnkey Kubernetes management contradict independent survey data showing significant ongoing operational maintenance burden.

## Conclusion
Organizations with dedicated platform teams should maintain Kubernetes standardization. Lean teams operating bare-metal or hybrid fleets can achieve higher density and faster velocity with Nomad.`,
    },
  },
];
