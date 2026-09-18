from app.graph.state import RecruitmentState

from app.rag.candidate_query_builder import build_candidate_job_query
from app.rag.job_retriever import retrieve_jobs_for_candidate

from app.database.job_repository import get_job_by_id
from app.agents.job_match_agent import match_candidate_to_job


def retrieval_node(state: RecruitmentState) -> dict:
    """
    Retrieve semantically relevant jobs for the candidate.

    Workflow:
    Candidate
        -> Candidate Query Builder
        -> ChromaDB Vector Search
        -> Relevant Jobs
    """

    candidate = state["candidate"]

    # Build a semantic search query from the candidate profile
    rag_query = build_candidate_job_query(candidate)

    # Retrieve relevant jobs from ChromaDB
    retrieval_result = retrieve_jobs_for_candidate(
        candidate=candidate,
        top_k=5,
    )

    retrieved_jobs = retrieval_result["results"]

    return {
        "rag_query": rag_query,
        "retrieved_jobs": retrieved_jobs,
        "jobs_retrieved": retrieval_result["jobs_retrieved"],
        "status": "jobs_retrieved",
    }


def matching_node(state: RecruitmentState) -> dict:
    """
    Evaluate RAG-retrieved jobs using the LLM Job Match Agent.

    Workflow:
    Retrieved Jobs
        -> Load full Job from database
        -> Job Match Agent
        -> Structured Match Result
    """

    candidate = state["candidate"]
    retrieved_jobs = state["retrieved_jobs"]

    evaluated_matches = []
    failed_matches = []

    for retrieved_job in retrieved_jobs:
        job_id = retrieved_job["job_id"]

        try:
            # Load the complete job record from SQLite
            job = get_job_by_id(job_id)

            if job is None:
                failed_matches.append(
                    {
                        "job_id": job_id,
                        "error": "Job not found in database",
                    }
                )
                continue

            # Deep candidate-job evaluation using the LLM agent
            match = match_candidate_to_job(
                candidate=candidate,
                job=job,
            )

            evaluated_matches.append(
                {
                    "job": job,
                    "match": match,
                    "rag_distance": retrieved_job["distance"],
                }
            )

        except Exception as exc:
            failed_matches.append(
                {
                    "job_id": job_id,
                    "error": str(exc),
                }
            )

    return {
        "evaluated_matches": evaluated_matches,
        "failed_matches": failed_matches,
        "jobs_evaluated": len(evaluated_matches),
        "status": "jobs_evaluated",
    }

def ranking_node(state: RecruitmentState) -> dict:
    """
    Rank evaluated jobs using both LLM match quality
    and semantic RAG relevance.

    Final score:
    - 85% LLM job-match score
    - 15% semantic retrieval relevance
    """

    evaluated_matches = state["evaluated_matches"]

    ranked_matches = []

    for item in evaluated_matches:
        match = item["match"]
        rag_distance = item["rag_distance"]

        # Convert Chroma distance into a 0-100 relevance score.
        rag_score = max(
            0.0,
            min(100.0, (1.0 - rag_distance) * 100)
        )

        # LLM evaluation is the primary signal.
        final_score = (
            match.overall_score * 0.85
            + rag_score * 0.15
        )

        ranked_matches.append(
            {
                **item,
                "rag_score": round(rag_score, 2),
                "final_score": round(final_score, 2),
            }
        )

    ranked_matches.sort(
        key=lambda item: item["final_score"],
        reverse=True,
    )

    return {
        "ranked_matches": ranked_matches,
        "status": "jobs_ranked",
    }