from typing import List
from pydantic import BaseModel, Field


class ScoreBreakdown(BaseModel):
    skills_score: float = Field(ge=0, le=100)
    experience_score: float = Field(ge=0, le=100)
    role_score: float = Field(ge=0, le=100)
    location_score: float = Field(ge=0, le=100)


class JobMatch(BaseModel):
    candidate_id: str
    job_id: str

    overall_score: float = Field(ge=0, le=100)

    score_breakdown: ScoreBreakdown

    matched_skills: List[str] = Field(default_factory=list)
    missing_required_skills: List[str] = Field(default_factory=list)
    missing_preferred_skills: List[str] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)

    recommendation: str
    reasoning: str