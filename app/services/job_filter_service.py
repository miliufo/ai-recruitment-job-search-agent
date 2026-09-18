from app.models.candidate import Candidate
from app.models.job import Job


def normalize(value: str) -> str:
    return value.strip().lower()


def calculate_prefilter_score(
    candidate: Candidate,
    job: Job,
) -> float:

    score = 0.0

    candidate_skills = {
        normalize(skill)
        for skill in candidate.skills
    }

    required_skills = {
        normalize(skill)
        for skill in job.required_skills
    }

    preferred_skills = {
        normalize(skill)
        for skill in job.preferred_skills
    }

    target_roles = [
        normalize(role)
        for role in candidate.target_roles
    ]

    job_title = normalize(job.title)

    # ---------------------------------
    # Required skill overlap: 50 points
    # ---------------------------------

    if required_skills:
        required_overlap = (
            len(candidate_skills & required_skills)
            / len(required_skills)
        )

        score += required_overlap * 50

    # ---------------------------------
    # Preferred skill overlap: 15 points
    # ---------------------------------

    if preferred_skills:
        preferred_overlap = (
            len(candidate_skills & preferred_skills)
            / len(preferred_skills)
        )

        score += preferred_overlap * 15

    # ---------------------------------
    # Target role similarity: 25 points
    # ---------------------------------

    role_match = any(
        role in job_title or job_title in role
        for role in target_roles
    )

    if role_match:
        score += 25

    # ---------------------------------
    # Location compatibility: 10 points
    # ---------------------------------

    candidate_location = normalize(
        candidate.location or ""
    )

    job_location = normalize(
        job.location or ""
    )

    remote_terms = [
        "remote",
        "europe",
        "eu",
    ]

    location_match = (
        candidate_location in job_location
        or job_location in candidate_location
        or any(
            term in job_location
            for term in remote_terms
        )
    )

    if location_match:
        score += 10

    return round(score, 2)


def shortlist_jobs(
    candidate: Candidate,
    jobs: list[Job],
    limit: int = 5,
    minimum_score: float = 20.0,
) -> list[dict]:

    scored_jobs = []

    for job in jobs:

        score = calculate_prefilter_score(
            candidate,
            job,
        )

        if score >= minimum_score:
            scored_jobs.append(
                {
                    "job": job,
                    "prefilter_score": score,
                }
            )

    scored_jobs.sort(
        key=lambda item: item["prefilter_score"],
        reverse=True,
    )

    return scored_jobs[:limit]