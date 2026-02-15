import logging

from fastapi import APIRouter, Depends

from app.dependencies import get_schema_reflector
from app.models.request import SchemaReflectRequest

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/schema/reflect")
async def reflect_schema(
    req: SchemaReflectRequest = SchemaReflectRequest(),
    reflector=Depends(get_schema_reflector),
):
    """Trigger schema reflection: introspect Postgres tables, generate
    descriptions via LLM, and store embeddings in ChromaDB.

    This must be called at least once before querying so the Discovery
    node has metadata to search against.
    """
    result = await reflector.reflect_and_store(force=req.force)
    return result
