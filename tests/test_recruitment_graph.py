from app.models.candidate import Candidate, WorkExperience
from app.graph.recruitment_graph import recruitment_graph


candidate = Candidate(
    candidate_id="CAND-001",
    name="Demo Candidate",
    headline="AI Engineer | Generative AI | AI Agents",
    location="Europe",
    skills=[
        "Python",
        "Generative AI",
        "AI Agents",
        "RAG",
        "LLMs",
        "Azure",
        "LangGraph",
    ],
    target_roles=[
        "AI Engineer",
        "Generative AI Engineer",
        "AI Agent Engineer",
    ],
    work_experience=[
        WorkExperience(
            company="Example Tech",
            role="AI Engineer",
            description="Built AI agent and RAG applications",
            skills=["Python", "LLMs", "RAG"],
        )
    ],
)


initial_state = {
    "candidate": candidate,
    "rag_query": "",
    "retrieved_jobs": [],
    "evaluated_matches": [],
    "failed_matches": [],
    "ranked_matches": [],
    "jobs_retrieved": 0,
    "jobs_evaluated": 0,
    "status": "started",
}


result = recruitment_graph.invoke(initial_state)


print("\n=== RECRUITMENT AGENT RESULT ===")
print("Status:", result["status"])
print("Jobs retrieved:", result["jobs_retrieved"])
print("Jobs evaluated:", result["jobs_evaluated"])
print("Failed matches:", len(result["failed_matches"]))

print("\n=== FINAL RANKING ===")

for index, item in enumerate(result["ranked_matches"], start=1):
    job = item["job"]
    match = item["match"]

    print(
        index,
        job.job_id,
        "-",
        job.title,
        "| LLM:",
        match.overall_score,
        "| RAG:",
        item["rag_score"],
        "| FINAL:",
        item["final_score"],
        "|",
        match.recommendation,
    )