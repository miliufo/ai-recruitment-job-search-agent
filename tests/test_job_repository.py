from app.database.database import init_database
from app.database.job_repository import add_job, get_all_jobs
from app.models.job import Job


def test_job_can_be_saved_and_retrieved():
    init_database()

    test_job = Job(
        job_id="TEST-DB-JOB-001",
        title="AI Platform Engineer",
        company="Test AI Company",
        location="Remote - Europe",
        description="Build production AI infrastructure.",
        required_skills=[
            "Python",
            "FastAPI",
            "Docker",
        ],
        preferred_skills=[
            "Azure",
            "RAG",
        ],
    )

    add_job(test_job)

    jobs = get_all_jobs()

    matching_jobs = [
        job
        for job in jobs
        if job.job_id == "TEST-DB-JOB-001"
    ]

    assert len(matching_jobs) >= 1

    saved_job = matching_jobs[0]

    assert saved_job.title == "AI Platform Engineer"
    assert saved_job.company == "Test AI Company"
    assert "Python" in saved_job.required_skills
    assert "Docker" in saved_job.required_skills
    assert "Azure" in saved_job.preferred_skills