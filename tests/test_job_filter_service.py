from app.models.candidate import Candidate
from app.models.job import Job
from app.services.job_filter_service import shortlist_jobs


def test_shortlist_jobs_filters_irrelevant_jobs():
    candidate = Candidate(
        candidate_id="TEST-CAND-001",
        name="Test Candidate",
        headline="AI Engineer",
        location="Europe",
        skills=[
            "Python",
            "Generative AI",
            "AI Agents",
            "RAG",
            "LLMs",
            "Azure",
        ],
        target_roles=[
            "AI Engineer",
            "Generative AI Engineer",
        ],
    )

    strong_job = Job(
        job_id="TEST-JOB-001",
        title="Generative AI Engineer",
        company="AI Labs",
        location="Remote - Europe",
        description="Build AI agents and RAG applications.",
        required_skills=[
            "Python",
            "LLMs",
            "RAG",
        ],
        preferred_skills=[
            "Azure",
            "AI Agents",
        ],
    )

    irrelevant_job = Job(
        job_id="TEST-JOB-002",
        title="Backend Engineer",
        company="Backend Corp",
        location="New York",
        description="Build Java backend infrastructure.",
        required_skills=[
            "Java",
            "Spring",
            "Kubernetes",
        ],
        preferred_skills=[
            "AWS",
        ],
    )

    results = shortlist_jobs(
        candidate=candidate,
        jobs=[irrelevant_job, strong_job],
        limit=2,
    )

    # The relevant AI job should survive pre-filtering.
    assert len(results) == 1

    assert results[0]["job"].job_id == "TEST-JOB-001"

    assert results[0]["prefilter_score"] > 0

    # The irrelevant backend job should be filtered out.
    returned_job_ids = [
        item["job"].job_id
        for item in results
    ]

    assert "TEST-JOB-002" not in returned_job_ids