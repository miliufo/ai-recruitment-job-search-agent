from typing import Any

from app.models.candidate import Candidate
from app.database.job_repository import get_all_jobs
from app.services.job_filter_service import shortlist_jobs
from app.agents.job_match_agent import match_candidate_to_job


def search_jobs_for_candidate(
    candidate: Candidate,
    top_k: int = 5,
    prefilter_limit: int = 5,
) -> dict[str, Any]:
    """
    Production-style hybrid job search pipeline.

    Pipeline:
    1. Load jobs from database.
    2. Apply deterministic pre-filtering.
    3. Run expensive LLM matching only on shortlisted jobs.
    4. Rank successful matches by final LLM score.
    """

    jobs = get_all_jobs()

    if not jobs:
        return {
            "candidate_id": candidate.candidate_id,
            "jobs_available": 0,
            "jobs_shortlisted": 0,
            "jobs_evaluated": 0,
            "failed_matches": 0,
            "matches": [],
        }

    shortlist = shortlist_jobs(
        candidate=candidate,
        jobs=jobs,
        limit=prefilter_limit,
    )

    matches = []
    failed_matches = []

    for item in shortlist:
        job = item["job"]
        prefilter_score = item["prefilter_score"]

        try:
            match = match_candidate_to_job(
                candidate=candidate,
                job=job,
            )

            matches.append(
                {
                    "job": job,
                    "prefilter_score": prefilter_score,
                    "match": match,
                }
            )

        except Exception as exc:
            failed_matches.append(
                {
                    "job_id": job.job_id,
                    "error": str(exc),
                }
            )

    matches.sort(
        key=lambda item: item["match"].overall_score,
        reverse=True,
    )

    return {
        "candidate_id": candidate.candidate_id,
        "jobs_available": len(jobs),
        "jobs_shortlisted": len(shortlist),
        "jobs_evaluated": len(matches),
        "failed_matches": len(failed_matches),
        "failures": failed_matches,
        "matches": matches[:top_k],
    }