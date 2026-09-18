from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.routes import recruitment_graph


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_job_search_endpoint():
    mock_result = {
        "status": "jobs_ranked",
        "candidate_id": "TEST-CAND-001",
        "jobs_retrieved": 2,
        "jobs_evaluated": 2,
        "failed_matches": [],
        "ranked_matches": []
    }

    request_body = {
        "candidate": {
            "candidate_id": "TEST-CAND-001",
            "name": "Test Candidate",
            "headline": "AI Engineer",
            "location": "Europe",
            "skills": [
                "Python",
                "LLMs",
                "RAG",
                "AI Agents",
                "Azure"
            ],
            "target_roles": [
                "AI Engineer",
                "Generative AI Engineer"
            ]
        },
        "top_k": 5
    }

    with patch.object(
        recruitment_graph,
        "invoke",
        return_value=mock_result
    ):
        response = client.post(
            "/api/v1/jobs/search",
            json=request_body
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "jobs_ranked"
    assert data["candidate_id"] == "TEST-CAND-001"
    assert data["jobs_retrieved"] == 2
    assert data["jobs_evaluated"] == 2
    assert data["failed_matches"] == 0
    assert data["matches"] == []