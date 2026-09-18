from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class JobRecord(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    job_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
        index=True,
    )

    company = Column(
        String(200),
        nullable=False,
    )

    location = Column(
        String(200),
        nullable=False,
    )

    employment_type = Column(
        String(100),
        nullable=True,
    )

    workplace_type = Column(
        String(100),
        nullable=True,
    )

    description = Column(
        Text,
        nullable=False,
    )

    required_skills = Column(
        Text,
        nullable=False,
        default="[]",
    )

    preferred_skills = Column(
        Text,
        nullable=False,
        default="[]",
    )

    experience_level = Column(
        String(100),
        nullable=True,
    )

    salary_min = Column(
        Float,
        nullable=True,
    )

    salary_max = Column(
        Float,
        nullable=True,
    )

    currency = Column(
        String(20),
        nullable=True,
    )

    source = Column(
        String(100),
        nullable=True,
    )

    application_url = Column(
        Text,
        nullable=True,
    )