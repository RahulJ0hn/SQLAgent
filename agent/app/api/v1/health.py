from fastapi import APIRouter, Depends

from app.dependencies import get_db, get_chroma
from app.services.database import DatabaseService
from app.services.chroma import ChromaService

router = APIRouter()


@router.get("/health")
async def health_check(
    db: DatabaseService = Depends(get_db),
    chroma: ChromaService = Depends(get_chroma),
):
    """Health check endpoint. Verifies connectivity to Postgres and ChromaDB."""
    status = {"status": "healthy", "services": {}}

    # Check Postgres
    try:
        async with db.acquire() as conn:
            await conn.fetchval("SELECT 1")
        status["services"]["postgres"] = "connected"
    except Exception as e:
        status["services"]["postgres"] = f"error: {e}"
        status["status"] = "degraded"

    # Check ChromaDB
    try:
        count = chroma.get_collection_count()
        status["services"]["chromadb"] = f"connected ({count} documents)"
    except Exception as e:
        status["services"]["chromadb"] = f"error: {e}"
        status["status"] = "degraded"

    return status
