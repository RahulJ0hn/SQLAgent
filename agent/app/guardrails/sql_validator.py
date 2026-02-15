import logging

import sqlglot
from sqlglot import exp

from app.config import Settings
from app.utils.exceptions import GuardrailError

logger = logging.getLogger(__name__)


class SQLValidator:
    """Validates generated SQL using sqlglot AST parsing.

    Enforces:
    1. SELECT-only statements (blocks INSERT, UPDATE, DELETE, DROP, etc.)
    2. PII table access blocking
    3. PII column access blocking
    """

    BLOCKED_STATEMENT_TYPES = (
        exp.Insert,
        exp.Update,
        exp.Delete,
        exp.Drop,
        exp.Create,
        exp.Alter,
        exp.Grant,
        exp.Command,
    )

    def __init__(self, settings: Settings):
        self.pii_tables = {t.lower() for t in settings.pii_blocked_tables}
        self.pii_columns = {c.lower() for c in settings.pii_blocked_columns}

    def validate(self, sql: str) -> str:
        """Parse SQL, enforce SELECT-only, block PII access.

        Args:
            sql: The SQL string to validate.

        Returns:
            Normalized SQL string (pretty-printed Postgres dialect).

        Raises:
            GuardrailError: If the SQL violates any guardrail rule.
        """
        # Parse
        try:
            parsed = sqlglot.parse(sql, error_level=sqlglot.ErrorLevel.RAISE)
        except sqlglot.errors.ParseError as e:
            raise GuardrailError(f"SQL parse error: {e}", "PARSE_ERROR")

        if not parsed:
            raise GuardrailError("Empty SQL statement", "EMPTY")

        for statement in parsed:
            # Block non-SELECT statement types
            if isinstance(statement, self.BLOCKED_STATEMENT_TYPES):
                raise GuardrailError(
                    f"Only SELECT statements are allowed. Got: {type(statement).__name__}",
                    "NON_SELECT",
                )

            # Ensure it IS a Select (catches SHOW, SET, EXPLAIN, etc.)
            if not isinstance(statement, exp.Select):
                raise GuardrailError(
                    f"Statement type not allowed: {type(statement).__name__}",
                    "NON_SELECT",
                )

            # Block PII tables
            for table in statement.find_all(exp.Table):
                if table.name.lower() in self.pii_tables:
                    raise GuardrailError(
                        f"Access to table '{table.name}' is blocked (contains PII data)",
                        "PII_TABLE",
                    )

            # Block PII columns
            for col in statement.find_all(exp.Column):
                if col.name.lower() in self.pii_columns:
                    raise GuardrailError(
                        f"Access to column '{col.name}' is blocked (PII field)",
                        "PII_COLUMN",
                    )

        # Return normalized SQL
        normalized = parsed[0].sql(dialect="postgres", pretty=True)
        logger.info(f"SQL passed guardrails: {normalized[:100]}...")
        return normalized
