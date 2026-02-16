import chromadb
import logging

from app.config import Settings

logger = logging.getLogger(__name__)


class ChromaService:
    """ChromaDB client for storing and retrieving schema metadata embeddings."""

    def __init__(self):
        self.client = None
        self.collection = None

    def connect(self, settings: Settings):
        if settings.chroma_mode == "http":
            # Docker deployment — connect to ChromaDB container
            self.client = chromadb.HttpClient(
                host=settings.chroma_host,
                port=settings.chroma_port,
            )
            logger.info(f"ChromaDB HttpClient connected to {settings.chroma_host}:{settings.chroma_port}")
        else:
            # Cloud / embedded deployment — persist locally
            self.client = chromadb.PersistentClient(
                path=settings.chroma_persist_dir,
            )
            logger.info(f"ChromaDB PersistentClient at {settings.chroma_persist_dir}")

        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(f"ChromaDB collection '{settings.chroma_collection}' ready")

    def upsert_table_metadata(
        self, table_name: str, description: str, columns: list[dict]
    ):
        """Store table + column descriptions as vector embeddings."""
        doc_text = f"Table: {table_name}\n{description}\n\nColumns:\n"
        for col in columns:
            doc_text += f"  - {col['name']} ({col['type']}): {col.get('description', '')}\n"

        self.collection.upsert(
            ids=[f"table_{table_name}"],
            documents=[doc_text],
            metadatas=[{"table_name": table_name, "type": "table_schema"}],
        )
        logger.info(f"Upserted metadata for table '{table_name}'")

    def search_relevant_tables(self, query: str, n_results: int = 5) -> list[dict]:
        """Retrieve the most relevant table metadata for a natural language query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
        )

        if not results["documents"] or not results["documents"][0]:
            return []

        return [
            {"document": doc, "metadata": meta, "distance": dist}
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def get_collection_count(self) -> int:
        """Return the number of documents in the collection."""
        return self.collection.count() if self.collection else 0
