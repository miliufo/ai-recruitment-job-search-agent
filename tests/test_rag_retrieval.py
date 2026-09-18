from app.rag.job_retriever import retrieve_jobs


def test_rag_retrieval_returns_relevant_ai_jobs():
    query = (
        "Generative AI engineer building RAG systems, "
        "LLM applications and AI agents in Europe"
    )

    results = retrieve_jobs(
        query=query,
        top_k=3,
    )

    assert len(results) > 0
    assert len(results) <= 3

    first_result = results[0]

    assert "job_id" in first_result
    assert "title" in first_result
    assert "company" in first_result
    assert "distance" in first_result

    # Chroma distance: lower means more semantically similar.
    distances = [
        result["distance"]
        for result in results
    ]

    assert distances == sorted(distances)

    # Our seeded AI jobs should dominate this AI-focused query.
    returned_ids = {
        result["job_id"]
        for result in results
    }

    expected_ai_jobs = {
        "JOB-001",
        "JOB-002",
        "JOB-003",
        "JOB-005",
        "JOB-006",
    }

    assert returned_ids.intersection(expected_ai_jobs)