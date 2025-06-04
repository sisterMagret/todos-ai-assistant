from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base
from app.database.session import engine
from app.routes import schedule, users


def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    create_tables()
    yield


def get_application():
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="FastAPI AI Assistant App",
        description="AI voice assistant backend.",
        version="1.0.0",
        docs_url="/",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users.router)
    app.include_router(schedule.router)

    return app


app = get_application()
