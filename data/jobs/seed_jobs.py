from app.database.database import init_database
from app.database.job_repository import add_job, get_all_jobs
from app.models.job import Job


JOBS = [
    Job(
        job_id="JOB-002",
        title="AI Agent Engineer",
        company="Nova Intelligence",
        location="Remote - Europe",
        employment_type="Full-time",
        workplace_type="Remote",
        experience_level="Mid-level",
        description=(
            "Build multi-agent AI systems, tool-calling workflows, "
            "RAG pipelines and production APIs."
        ),
        required_skills=[
            "Python",
            "LLMs",
            "AI Agents",
            "RAG",
            "LangGraph",
        ],
        preferred_skills=[
            "FastAPI",
            "Docker",
            "Azure",
        ],
        salary_min=65000,
        salary_max=90000,
        currency="EUR",
        source="Demo Dataset",
    ),

    Job(
        job_id="JOB-003",
        title="Generative AI Engineer",
        company="Vertex Labs",
        location="Berlin, Germany",
        employment_type="Full-time",
        workplace_type="Hybrid",
        experience_level="Mid-level",
        description=(
            "Develop production Generative AI applications using LLMs, "
            "retrieval systems, evaluation pipelines and cloud services."
        ),
        required_skills=[
            "Python",
            "Generative AI",
            "LLMs",
            "RAG",
            "FastAPI",
        ],
        preferred_skills=[
            "Azure",
            "Docker",
            "LangChain",
        ],
        salary_min=70000,
        salary_max=95000,
        currency="EUR",
        source="Demo Dataset",
    ),

    Job(
        job_id="JOB-004",
        title="Machine Learning Engineer",
        company="DataForge",
        location="Vienna, Austria",
        employment_type="Full-time",
        workplace_type="Hybrid",
        experience_level="Mid-level",
        description=(
            "Build and deploy machine learning models and scalable "
            "data-driven services."
        ),
        required_skills=[
            "Python",
            "Machine Learning",
            "scikit-learn",
            "SQL",
        ],
        preferred_skills=[
            "Docker",
            "AWS",
            "MLOps",
        ],
        salary_min=60000,
        salary_max=85000,
        currency="EUR",
        source="Demo Dataset",
    ),

    Job(
        job_id="JOB-005",
        title="LLM Application Engineer",
        company="Cognitive Systems",
        location="Remote - EU",
        employment_type="Full-time",
        workplace_type="Remote",
        experience_level="Mid-level",
        description=(
            "Design LLM-powered applications with retrieval, "
            "structured outputs, evaluation and API integrations."
        ),
        required_skills=[
            "Python",
            "LLMs",
            "RAG",
            "Prompt Engineering",
        ],
        preferred_skills=[
            "LangGraph",
            "FastAPI",
            "Docker",
        ],
        salary_min=65000,
        salary_max=92000,
        currency="EUR",
        source="Demo Dataset",
    ),

    Job(
        job_id="JOB-006",
        title="AI Solutions Engineer",
        company="CloudMind",
        location="Bratislava, Slovakia",
        employment_type="Full-time",
        workplace_type="Hybrid",
        experience_level="Mid-level",
        description=(
            "Build enterprise AI solutions using Microsoft Azure, "
            "Generative AI services and API-based architectures."
        ),
        required_skills=[
            "Python",
            "Azure",
            "Generative AI",
            "APIs",
        ],
        preferred_skills=[
            "RAG",
            "Docker",
            "FastAPI",
        ],
        salary_min=50000,
        salary_max=75000,
        currency="EUR",
        source="Demo Dataset",
    ),

    Job(
        job_id="JOB-007",
        title="Senior Backend Engineer",
        company="ScaleCore",
        location="Prague, Czech Republic",
        employment_type="Full-time",
        workplace_type="Hybrid",
        experience_level="Senior",
        description=(
            "Design distributed backend systems and production APIs "
            "for high-scale cloud applications."
        ),
        required_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
            "Kubernetes",
        ],
        preferred_skills=[
            "AWS",
            "Redis",
            "Microservices",
        ],
        salary_min=75000,
        salary_max=105000,
        currency="EUR",
        source="Demo Dataset",
    ),
]


def seed_jobs():
    init_database()

    for job in JOBS:
        add_job(job)

    jobs = get_all_jobs()

    print(f"Database contains {len(jobs)} jobs.")

    for job in jobs:
        print(
            f"{job.job_id} | "
            f"{job.title} | "
            f"{job.company} | "
            f"{job.location}"
        )


if __name__ == "__main__":
    seed_jobs()