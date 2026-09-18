from typing import Any, TypedDict

from app.models.candidate import Candidate


class RecruitmentState(TypedDict):
    """
    Shared state passed between nodes in the
    recruitment LangGraph workflow.
    """

    candidate: Candidate

    # Semantic retrieval
    rag_query: str
    retrieved_jobs: list[dict[str, Any]]

    # Deep LLM matching
    evaluated_matches: list[dict[str, Any]]
    failed_matches: list[dict[str, Any]]

    # Final ranking
    ranked_matches: list[dict[str, Any]]

    # Workflow metadata
    jobs_retrieved: int
    jobs_evaluated: int
    status: str