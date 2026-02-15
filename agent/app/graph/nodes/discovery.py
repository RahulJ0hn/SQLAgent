import logging

from app.models.response import ReasoningStep
from app.services.chroma import ChromaService

logger = logging.getLogger(__name__)


async def discovery_node(state: dict, *, chroma: ChromaService) -> dict:
    """Node 1: RAG-based metadata discovery.

    Searches ChromaDB for table/column metadata relevant to the user's
    natural language query. This ensures the LLM only sees relevant
    schema context, preventing hallucination of non-existent tables.
    """
    query = state["user_query"]
    results = chroma.search_relevant_tables(query, n_results=5)

    table_names = [r["metadata"]["table_name"] for r in results if "metadata" in r]
    logger.info(f"Discovery found {len(results)} relevant tables: {table_names}")

    return {
        "relevant_tables": results,
        "reasoning": [
            ReasoningStep(
                step="Discovery",
                thought=f"Searched schema metadata and found {len(results)} relevant tables: {', '.join(table_names)}",
                action="Semantic search over ChromaDB schema embeddings",
            )
        ],
    }
