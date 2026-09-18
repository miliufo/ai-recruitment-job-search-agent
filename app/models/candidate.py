from typing import List, Optional
from pydantic import BaseModel, Field


class WorkExperience(BaseModel):
    company: str
    role: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    skills: List[str] = Field(default_factory=list)


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    graduation_year: Optional[int] = None


class Candidate(BaseModel):
    candidate_id: str

    name: str
    headline: Optional[str] = None
    location: Optional[str] = None

    summary: Optional[str] = None

    skills: List[str] = Field(default_factory=list)

    work_experience: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)

    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)

    target_roles: List[str] = Field(default_factory=list)

    years_of_experience: Optional[float] = None

    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None