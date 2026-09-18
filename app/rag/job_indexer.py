from app.database.job_repository import get_all_jobs
from app.rag.vector_store import (
    get_job_collection,
    reset_job_collection,
)


def job_to_document(job) -> str:
    """
    Convert a Job object into a text document suitable
    for semantic search and retrieval.
    """

    required_skills = ", ".join(job.required_skills or [])
    preferred_skills = ", ".join(job.preferred_skills or [])

    return f"""
Job Title: {job.title}
Company: {job.company}
Location: {job.location or "Not specified"}
Employment Type: {job.employment_type or "Not specified"}
Workplace Type: {job.workplace_type or "Not specified"}
Experience Level: {job.experience_level or "Not specified"}

Job Description:
{job.description}

Required Skills:
{required_skills}

Preferred Skills:
{preferred_skills}
""".strip()


def index_jobs(reset: bool = True) -> dict:
    """
    Load jobs from SQLite and index them in ChromaDB.
    """

    jobs = get_all_jobs()

    if reset:
        collection = reset_job_collection()
    else:
        collection = get_job_collection()

    if not jobs:
        return {
            "success": True,
            "jobs_found": 0,
            "jobs_indexed": 0,
        }

    ids = []
    documents = []
    metadatas = []

    for job in jobs:
        ids.append(job.job_id)

        documents.append(
            job_to_document(job)
        )

        metadatas.append(
            {
                "job_id": job.job_id,
                "title": job.title,
                "company": job.company,
                "location": job.location or "",
            }
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    return {
        "success": True,
        "jobs_found": len(jobs),
        "jobs_indexed": len(ids),
        "collection_count": collection.count(),
    }


if __name__ == "__main__":
    result = index_jobs()
    print(result)