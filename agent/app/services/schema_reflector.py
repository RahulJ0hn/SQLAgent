import logging

from app.services.database import DatabaseService
from app.services.chroma import ChromaService

logger = logging.getLogger(__name__)


class SchemaReflector:
    """Introspects PostgreSQL schema, generates descriptions via LLM,
    and stores them in ChromaDB for the RAG discovery layer."""

    def __init__(self, db: DatabaseService, chroma: ChromaService, llm):
        self.db = db
        self.chroma = chroma
        self.llm = llm

    async def reflect_and_store(self, force: bool = False):
        """Pull schema from Postgres, generate descriptions, store in ChromaDB.

        Args:
            force: If True, re-reflect even if metadata already exists.
        """
        if not force and self.chroma.get_collection_count() > 0:
            logger.info("Schema metadata already exists in ChromaDB, skipping reflection")
            return {"status": "skipped", "reason": "metadata already exists"}

        schema_info = await self.db.get_schema_info()

        # Group columns by table
        tables: dict[str, list[dict]] = {}
        for row in schema_info:
            tables.setdefault(row["table_name"], []).append(row)

        reflected_tables = []
        for table_name, columns in tables.items():
            col_text = "\n".join(
                f"  {c['column_name']} {c['data_type']} "
                f"{'(nullable)' if c['is_nullable'] == 'YES' else '(not null)'}"
                for c in columns
            )

            prompt = (
                f"You are a database documentation expert. Given this PostgreSQL table, "
                f"write a concise 1-2 sentence description of what it stores and its "
                f"business purpose. Then briefly describe each column.\n\n"
                f"Table: {table_name}\nColumns:\n{col_text}"
            )

            response = await self.llm.ainvoke(prompt)
            description = response.content

            self.chroma.upsert_table_metadata(
                table_name=table_name,
                description=description,
                columns=[
                    {"name": c["column_name"], "type": c["data_type"]}
                    for c in columns
                ],
            )
            reflected_tables.append(table_name)
            logger.info(f"Reflected schema for table '{table_name}'")

        return {
            "status": "completed",
            "tables_reflected": reflected_tables,
            "count": len(reflected_tables),
        }
