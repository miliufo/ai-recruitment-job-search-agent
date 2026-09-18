from app.models.candidate import Candidate
from app.rag.vector_store import get_job_collection
from app.rag.candidate_query_builder import build_candidate_job_query


def retrieve_jobs(query: str, top_k: int = 5) -> list[dict]:
    """
    Retrieve semantically relevant jobs from ChromaDB.
    """

    if not query.strip():
        return []

    collection = get_job_collection()

    if collection.count() == 0:
        return []

    n_results = min(top_k, collection.count())

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    retrieved_jobs = []

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for job_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):
        retrieved_jobs.append(
            {
                "job_id": job_id,
                "title": metadata.get("title"),
                "company": metadata.get("company"),
                "location": metadata.get("location"),
                "distance": round(float(distance), 4),
                "document": document,
            }
        )

    return retrieved_jobs


def retrieve_jobs_for_candidate(
    candidate: Candidate,
    top_k: int = 5,
) -> dict:
    """
    Build a semantic search query from the candidate profile
    and retrieve the most relevant jobs.
    """

    query = build_candidate_job_query(candidate)

    results = retrieve_jobs(
        query=query,
        top_k=top_k,
    )

    return {
        "candidate_id": candidate.candidate_id,
        "query": query,
        "jobs_retrieved": len(results),
        "results": results,
    }