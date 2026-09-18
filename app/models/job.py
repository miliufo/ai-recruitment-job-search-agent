from typing import List, Optional
from pydantic import BaseModel, Field


class Job(BaseModel):
    job_id: str

    title: str
    company: str
    location: str

    employment_type: Optional[str] = None
    workplace_type: Optional[str] = None

    description: str

    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)

    experience_level: Optional[str] = None

    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None

    source: Optional[str] = None
    application_url: Optional[str] = None