from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models.candidate import Candidate
from app.graph.recruitment_graph import recruitment_graph


router = APIRouter(
    prefix="/api/v1",
    tags=["Recruitment"],
)


class JobSearchRequest(BaseModel):
    """
    API request containing the candidate profile
    and optional search configuration.
    """

    candidate: Candidate
    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum number of jobs to return.",
    )


class JobSearchResponse(BaseModel):
    """
    High-level API response metadata.
    """

    status: str
    candidate_id: str
    jobs_retrieved: int
    jobs_evaluated: int
    failed_matches: int
    matches: list[dict]


@router.get("/health")
def health_check():
    """
    Lightweight API health check.
    """

    return {
        "status": "healthy",
        "service": "AI Recruitment & Job Search Agent",
    }


@router.post(
    "/jobs/search",
    response_model=JobSearchResponse,
)
def search_jobs(request: JobSearchRequest):
    """
    Run the complete AI recruitment workflow.

    Candidate
        -> RAG Retrieval
        -> LLM Matching
        -> Hybrid Ranking
        -> Ranked Job Opportunities
    """

    candidate = request.candidate

    initial_state = {
        "candidate": candidate,
        "rag_query": "",
        "retrieved_jobs": [],
        "evaluated_matches": [],
        "failed_matches": [],
        "ranked_matches": [],
        "jobs_retrieved": 0,
        "jobs_evaluated": 0,
        "status": "started",
    }

    try:
        result = recruitment_graph.invoke(initial_state)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Recruitment workflow failed: {exc}",
        ) from exc

    serialized_matches = []

    for item in result["ranked_matches"][: request.top_k]:
        job = item["job"]
        match = item["match"]

        serialized_matches.append(
            {
                "job": job.model_dump(),
                "match": match.model_dump(),
                "rag_score": item["rag_score"],
                "final_score": item["final_score"],
            }
        )

    return JobSearchResponse(
        status=result["status"],
        candidate_id=candidate.candidate_id,
        jobs_retrieved=result["jobs_retrieved"],
        jobs_evaluated=result["jobs_evaluated"],
        failed_matches=len(result["failed_matches"]),
        matches=serialized_matches,
    )