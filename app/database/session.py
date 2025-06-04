from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool

# from app.core.config import settings

# DATABASE_URL = settings.DATABASE_URL

# engine = create_engine(
#     DATABASE_URL,
#     poolclass=QueuePool,
#     pool_size=5,
#     max_overflow=10,
#     pool_timeout=30,
#     pool_recycle=3600,
#     pool_pre_ping=True,
#     connect_args={"connect_timeout": 5},
# )

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    """Provide a database session for dependency injection.

    Yields:
        Generator: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
