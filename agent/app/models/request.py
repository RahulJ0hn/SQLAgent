from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Incoming query request from the orchestrator."""

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Natural language question about the database",
    )
    session_id: str | None = Field(default=None, description="Optional session ID for context")


class SchemaReflectRequest(BaseModel):
    """Request to trigger schema reflection into ChromaDB."""

    force: bool = Field(
        default=False, description="Force re-reflection even if metadata already exists"
    )
