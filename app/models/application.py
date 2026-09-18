from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel, Field


ApplicationStatus = Literal[
    "discovered",
    "shortlisted",
    "preparing",
    "ready_to_apply",
    "applied",
    "interview",
    "offer",
    "rejected",
    "withdrawn",
]


class ApplicationEvent(BaseModel):
    status: ApplicationStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = None


class JobApplication(BaseModel):
    application_id: str
    candidate_id: str
    job_id: str

    status: ApplicationStatus = "discovered"

    match_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )

    tailored_resume_path: Optional[str] = None
    cover_letter_path: Optional[str] = None

    applied_at: Optional[datetime] = None
    next_action: Optional[str] = None

    events: List[ApplicationEvent] = Field(default_factory=list)