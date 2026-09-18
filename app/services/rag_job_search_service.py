from app.models.candidate import Candidate
from app.database.job_repository import get_all_jobs
from app.rag.job_retriever import retrieve_jobs_for_candidate
from app.agents.job_match_agent import match_candidate_to_job


def search_and_match_jobs(
    candidate: Candidate,
    retrieval_limit: int = 5,
    top_k: int = 3,
) -> dict:
    """
    Production-style hybrid job search pipeline.

    Pipeline:
    Candidate Profile
        -> RAG Semantic Retrieval
        -> Job Database Lookup
        -> LLM Deep Matching
        -> Ranking
    """

    retrieval = retrieve_jobs_for_candidate(
        candidate=candidate,
        top_k=retrieval_limit,
    )

    all_jobs = get_all_jobs()

    jobs_by_id = {
        job.job_id: job
        for job in all_jobs
    }

    evaluated_matches = []
    failed_matches = []

    for retrieved in retrieval["results"]:
        job_id = retrieved["job_id"]

        job = jobs_by_id.get(job_id)

        if job is None:
            failed_matches.append(
                {
                    "job_id": job_id,
                    "error": "Retrieved job was not found in SQLite.",
                }
            )
            continue

        try:
            match = match_candidate_to_job(
                candidate,
                job,
            )

            evaluated_matches.append(
                {
                    "job": job,
                    "match": match,
                    "rag_distance": retrieved["distance"],
                }
            )

        except Exception as exc:
            failed_matches.append(
                {
                    "job_id": job_id,
                    "error": str(exc),
                }
            )

    evaluated_matches.sort(
        key=lambda item: item["match"].overall_score,
        reverse=True,
    )

    ranked_matches = evaluated_matches[:top_k]

    return {
        "candidate_id": candidate.candidate_id,
        "rag_query": retrieval["query"],
        "jobs_retrieved": retrieval["jobs_retrieved"],
        "jobs_evaluated": len(evaluated_matches),
        "failed_matches": len(failed_matches),
        "failures": failed_matches,
        "matches": ranked_matches,
    }