import asyncpg
import logging
from contextlib import asynccontextmanager

from app.config import Settings

logger = logging.getLogger(__name__)


class DatabaseService:
    """Async PostgreSQL connection pool manager."""

    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self, settings: Settings):
        if settings.database_url:
            # Cloud deployment (e.g. Neon) — use connection string
            self.pool = await asyncpg.create_pool(
                dsn=settings.database_url,
                min_size=2,
                max_size=10,
                statement_cache_size=0,
                ssl="require",
            )
            logger.info("PostgreSQL pool created via DATABASE_URL")
        else:
            # Local Docker deployment — use individual params
            self.pool = await asyncpg.create_pool(
                host=settings.pg_host,
                port=settings.pg_port,
                user=settings.pg_user,
                password=settings.pg_password,
                database=settings.pg_database,
                min_size=2,
                max_size=10,
                statement_cache_size=0,
            )
            logger.info("PostgreSQL pool created via host/port params")

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL connection pool closed")

    @asynccontextmanager
    async def acquire(self):
        async with self.pool.acquire() as conn:
            yield conn

    async def execute_query(self, sql: str) -> tuple[list[dict], list[str]]:
        """Execute a read-only SQL query.

        Returns:
            Tuple of (rows_as_dicts, column_names)
        """
        async with self.acquire() as conn:
            async with conn.transaction(readonly=True):
                stmt = await conn.prepare(sql)
                columns = [a.name for a in stmt.get_attributes()]
                rows = await stmt.fetch()
                result = []
                for row in rows:
                    row_dict = {}
                    for key, value in dict(row).items():
                        # Convert non-serializable types to strings
                        if hasattr(value, "isoformat"):
                            row_dict[key] = value.isoformat()
                        elif isinstance(value, (int, float, str, bool, type(None))):
                            row_dict[key] = value
                        else:
                            row_dict[key] = str(value)
                    result.append(row_dict)
                return result, columns

    async def get_schema_info(self) -> list[dict]:
        """Introspect all public tables and columns from information_schema."""
        query = """
            SELECT table_name, column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position
        """
        async with self.acquire() as conn:
            rows = await conn.fetch(query)
            return [dict(r) for r in rows]
