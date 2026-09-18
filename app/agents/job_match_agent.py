import json

from app.core.llm import client
from app.core.config import settings
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.job_match import JobMatch


SYSTEM_PROMPT = """
You are a senior technical recruiter and AI talent matching specialist.

Your task is to evaluate how well a candidate matches a job.

Evaluate these dimensions:

1. Skills match
2. Relevant experience
3. Target-role alignment
4. Location/workplace compatibility

Scoring rules:
- Every score must be between 0 and 100.
- Do not give credit for skills the candidate does not have.
- Do not invent candidate experience.
- Required skills matter more than preferred skills.
- Transferable experience may receive partial credit.
- Missing required skills must be explicitly listed.
- Keep strengths and gaps evidence-based.
- The overall score must reflect the complete assessment.

Recommendation rules:
- strong_apply: overall score >= 85
- apply: overall score >= 70
- stretch: overall score >= 50
- skip: overall score < 50

Return ONLY valid JSON.
"""


def match_candidate_to_job(
    candidate: Candidate,
    job: Job,
) -> JobMatch:

    prompt = f"""
CANDIDATE:

{candidate.model_dump_json(indent=2)}

JOB:

{job.model_dump_json(indent=2)}

Analyze the candidate-job match.

Return JSON using exactly this structure:

{{
    "candidate_id": "{candidate.candidate_id}",
    "job_id": "{job.job_id}",
    "overall_score": 0,
    "score_breakdown": {{
        "skills_score": 0,
        "experience_score": 0,
        "role_score": 0,
        "location_score": 0
    }},
    "matched_skills": [],
    "missing_required_skills": [],
    "missing_preferred_skills": [],
    "strengths": [],
    "gaps": [],
    "recommendation": "apply",
    "reasoning": "Concise evidence-based explanation"
}}
"""

    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={
            "type": "json_object"
        },
        temperature=0,
    )

    raw_result = response.choices[0].message.content

    parsed_result = json.loads(raw_result)

    return JobMatch.model_validate(parsed_result)