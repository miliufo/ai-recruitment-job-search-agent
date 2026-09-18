from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "data" / "recruitment.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def init_database() -> None:
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    Base.metadata.create_all(
        bind=engine
    )


def get_session():
    return SessionLocal()