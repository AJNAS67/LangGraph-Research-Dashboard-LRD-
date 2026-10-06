import os
from typing import Optional, Any, Type, Union
from pydantic import BaseModel
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.runnables import RunnableLambda

from app.config.settings import settings
from app.schemas.research import (
    ResearchPlanOutput,
    Subtask,
    AnalysisResult,
    FinalReport,
    ValidationResult,
)


class MockStructuredChatModel:
    """Mock LLM that intercepts with_structured_output calls for deterministic offline execution."""

    def __init__(self, responses: Optional[dict] = None):
        self._responses = responses or {}

    def with_structured_output(self, schema: Type[BaseModel], **kwargs: Any):
        def _mock_invoke(input_data: Any) -> BaseModel:
            # Check if an explicit response was injected for this schema
            if schema in self._responses:
                return self._responses[schema]

            if schema == ResearchPlanOutput:
                return ResearchPlanOutput(
                    objective="Investigate the impact, adoption benchmarks, and risk factors of AI technologies.",
                    subtasks=[
                        Subtask(
                            id="subtask_1",
                            title="State of AI Tools and Capabilities",
                            description="Evaluate state-of-the-art AI tooling and velocity metrics.",
                            queries=["AI coding tools velocity benchmark 2026", "AI software engineering impact"],
                        ),
                        Subtask(
                            id="subtask_2",
                            title="Enterprise Adoption & Security Risks",
                            description="Investigate data privacy, code leaks, and intellectual property.",
                            queries=["AI code generation security risks", "enterprise AI code governance 2026"],
                        ),
                    ],
                )

            elif schema == AnalysisResult:
                return AnalysisResult(
                    synthesized_findings=[
                        "AI coding assistants provide measurable 25-35% developer velocity improvements on routine tasks.",
                        "Enterprise adoption requires strict governance around private VPC deployments and token privacy.",
                    ],
                    agreements=[
                        "Both benchmark studies and industry reports agree that automated unit testing is the primary velocity driver.",
                    ],
                    contradictions=[
                        "Vendor claims assert 50%+ gains, whereas peer reviews find benefits plateau on complex legacy refactoring.",
                    ],
                    observed_gaps=[
                        "Longitudinal data on technical debt accumulation remains limited.",
                    ],
                )

            elif schema == ValidationResult:
                return ValidationResult(
                    status="VALID",
                    reason="Sufficient multi-source evidence was gathered to address core velocity and security questions.",
                    needs_more_research=False,
                    missing_aspects=[],
                    suggested_queries=[],
                )

            elif schema == FinalReport:
                return FinalReport(
                    title="Comprehensive Research Report: State of AI in Software Engineering",
                    executive_summary="This investigation evaluates the empirical impact, enterprise adoption trends, and risk governance requirements of AI software development tools in 2026.",
                    methodology="Multi-query web retrieval and automated cross-source synthesis.",
                    key_findings=[
                        "Developer velocity accelerates by 25-35% on greenfield and boilerplate code.",
                        "Security governance and IP protection represent the chief enterprise barrier.",
                    ],
                    detailed_analysis="### 1. Velocity Analysis\nEmpirical benchmarks indicate significant reductions in cycle time...\n\n### 2. Enterprise Governance\nOrganizations require isolated token gateways...",
                    contradictions=[
                        "Vendor marketing claims 55% speedup vs independent 25-35% measured reality.",
                    ],
                    limitations=[
                        "Long-term impact on maintenance cost requires multi-year observation.",
                    ],
                    conclusion="AI assistance is transitioning from experimental novelty to standard infrastructure with disciplined governance.",
                    sources_cited=[
                        "https://research.techbenchmarks.org/ai-coding-2026",
                        "https://infosec-journal.org/ai-risks-governance-2026",
                    ],
                    raw_markdown="# Comprehensive Research Report: State of AI in Software Engineering\n\n...",
                )

            # Fallback instantiate default
            return schema()

        return RunnableLambda(_mock_invoke)

    def invoke(self, messages: Any, **kwargs: Any) -> AIMessage:
        return AIMessage(content="Mock LLM response")


def get_llm(custom_model: Optional[str] = None) -> Union[BaseChatModel, MockStructuredChatModel]:
    """Factory function providing configured BaseChatModel or Mock Chat Model."""
    api_key = settings.OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY")

    if settings.LLM_PROVIDER == "openai" and api_key and not api_key.startswith("your_"):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=custom_model or settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            api_key=api_key,
            base_url=settings.LLM_BASE_URL,
        )

    # Return mock structured model for offline testing / missing key
    return MockStructuredChatModel()
