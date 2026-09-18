from app.models.candidate import Candidate


def build_candidate_job_query(candidate: Candidate) -> str:
    """
    Convert a candidate profile into a semantic job-search query
    suitable for vector retrieval.
    """

    target_roles = ", ".join(candidate.target_roles or [])
    skills = ", ".join(candidate.skills or [])

    experience_parts = []

    for experience in candidate.work_experience or []:
        if experience.role:
            experience_parts.append(experience.role)

        if experience.skills:
            experience_parts.extend(experience.skills)

    experience_text = ", ".join(
        dict.fromkeys(experience_parts)
    )

    query_parts = []

    if target_roles:
        query_parts.append(
            f"Target roles: {target_roles}"
        )

    if skills:
        query_parts.append(
            f"Skills: {skills}"
        )

    if experience_text:
        query_parts.append(
            f"Relevant experience: {experience_text}"
        )

    if candidate.location:
        query_parts.append(
            f"Preferred location: {candidate.location}"
        )

    return ". ".join(query_parts)