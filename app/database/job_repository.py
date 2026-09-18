import json
from typing import Optional

from sqlalchemy import select

from app.database.database import get_session
from app.database.models import JobRecord
from app.models.job import Job


def _record_to_job(record: JobRecord) -> Job:
    return Job(
        job_id=record.job_id,
        title=record.title,
        company=record.company,
        location=record.location,
        employment_type=record.employment_type,
        workplace_type=record.workplace_type,
        description=record.description,
        required_skills=json.loads(record.required_skills or "[]"),
        preferred_skills=json.loads(record.preferred_skills or "[]"),
        experience_level=record.experience_level,
        salary_min=record.salary_min,
        salary_max=record.salary_max,
        currency=record.currency,
        source=record.source,
        application_url=record.application_url,
    )


def add_job(job: Job) -> Job:
    session = get_session()

    try:
        existing = session.execute(
            select(JobRecord).where(
                JobRecord.job_id == job.job_id
            )
        ).scalar_one_or_none()

        if existing:
            return _record_to_job(existing)

        record = JobRecord(
            job_id=job.job_id,
            title=job.title,
            company=job.company,
            location=job.location,
            employment_type=job.employment_type,
            workplace_type=job.workplace_type,
            description=job.description,
            required_skills=json.dumps(job.required_skills),
            preferred_skills=json.dumps(job.preferred_skills),
            experience_level=job.experience_level,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            currency=job.currency,
            source=job.source,
            application_url=job.application_url,
        )

        session.add(record)
        session.commit()
        session.refresh(record)

        return _record_to_job(record)

    finally:
        session.close()


def get_job(job_id: str) -> Optional[Job]:
    session = get_session()

    try:
        record = session.execute(
            select(JobRecord).where(
                JobRecord.job_id == job_id
            )
        ).scalar_one_or_none()

        if not record:
            return None

        return _record_to_job(record)

    finally:
        session.close()


def get_all_jobs() -> list[Job]:
    session = get_session()

    try:
        records = session.execute(
            select(JobRecord).order_by(JobRecord.id)
        ).scalars().all()

        return [
            _record_to_job(record)
            for record in records
        ]

    finally:
        session.close()

def get_job_by_id(job_id: str):
    """
    Retrieve a single job from the database by job_id.
    """

    jobs = get_all_jobs()

    for job in jobs:
        if job.job_id == job_id:
            return job

    return None