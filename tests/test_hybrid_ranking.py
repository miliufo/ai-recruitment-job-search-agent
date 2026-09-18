from unittest.mock import patch

from app.graph.nodes import ranking_node
from app.models.job import Job
from app.models.job_match import JobMatch, ScoreBreakdown


def create_match(
    job_id: str,
    overall_score: float,
    recommendation: str,
) -> JobMatch:
    return JobMatch(
        candidate_id="TEST-CAND-001",
        job_id=job_id,
        overall_score=overall_score,
        score_breakdown=ScoreBreakdown(
            skills_score=overall_score,
            experience_score=overall_score,
            role_score=overall_score,
            location_score=overall_score,
        ),
        matched_skills=["Python", "RAG"],
        missing_required_skills=[],
        missing_preferred_skills=[],
        strengths=["Relevant AI experience"],
        gaps=[],
        recommendation=recommendation,
        reasoning="Test reasoning",
    )


def test_hybrid_ranking_combines_llm_and_rag_scores():
    job_a = Job(
        job_id="TEST-JOB-A",
        title="AI Agent Engineer",
        company="Agent Labs",
        location="Remote - Europe",
        description="Build production AI agents.",
        required_skills=["Python", "LLMs"],
        preferred_skills=["RAG"],
    )

    job_b = Job(
        job_id="TEST-JOB-B",
        title="Generative AI Engineer",
        company="GenAI Labs",
        location="Remote - Europe",
        description="Build generative AI applications.",
        required_skills=["Python", "RAG"],
        preferred_skills=["LLMs"],
    )

    state = {
        "evaluated_matches": [
            {
                "job": job_a,
                "match": create_match(
                    job_id="TEST-JOB-A",
                    overall_score=90.0,
                    recommendation="strong_apply",
                ),
                "rag_distance": 0.20,
            },
            {
                "job": job_b,
                "match": create_match(
                    job_id="TEST-JOB-B",
                    overall_score=70.0,
                    recommendation="apply",
                ),
                "rag_distance": 0.60,
            },
        ]
    }

    result = ranking_node(state)

    assert result["status"] == "jobs_ranked"

    ranked_matches = result["ranked_matches"]

    assert len(ranked_matches) == 2

    # Job A has both a stronger LLM match and better RAG similarity.
    assert ranked_matches[0]["job"].job_id == "TEST-JOB-A"

    # Ranking must be descending by final hybrid score.
    assert (
        ranked_matches[0]["final_score"]
        >= ranked_matches[1]["final_score"]
    )

    # Final scores should stay normalized.
    for item in ranked_matches:
        assert 0 <= item["final_score"] <= 100
        assert 0 <= item["rag_score"] <= 100