import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings
from app.services.database import DatabaseService
from app.services.chroma import ChromaService
from app.services.llm import get_llm, get_planner_llm, get_error_llm
from app.services.schema_reflector import SchemaReflector
from app.guardrails.sql_validator import SQLValidator
from app.graph.pipeline import build_agent_graph
from app.api.router import api_router
from app.utils.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize and tear down services."""
    setup_logging()
    settings = Settings()

    # --- Initialize services ---
    db = DatabaseService()
    await db.connect(settings)

    chroma = ChromaService()
    chroma.connect(settings)

    validator = SQLValidator(settings)
    planner_llm = get_planner_llm(settings)
    error_llm = get_error_llm(settings)
    base_llm = get_llm(settings)

    # Schema reflector (uses base LLM for generating descriptions)
    schema_reflector = SchemaReflector(db=db, chroma=chroma, llm=base_llm)

    # --- Build agent graph ---
    agent = build_agent_graph(
        chroma=chroma,
        db=db,
        validator=validator,
        planner_llm=planner_llm,
        error_llm=error_llm,
        max_attempts=settings.max_self_heal_attempts,
    )

    # Attach to app state for dependency injection
    app.state.agent = agent
    app.state.db = db
    app.state.chroma = chroma
    app.state.settings = settings
    app.state.schema_reflector = schema_reflector

    logger.info("Agent pipeline compiled and all services ready")
    yield

    # --- Cleanup ---
    await db.disconnect()
    logger.info("Shutdown complete")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Agentic SQL Enterprise Assistant",
        description="Production-grade natural language to SQL agent with self-healing capabilities",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
