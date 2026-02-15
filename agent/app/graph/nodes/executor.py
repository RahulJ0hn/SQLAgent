import logging

from app.models.response import ReasoningStep
from app.services.database import DatabaseService
from app.guardrails.sql_validator import SQLValidator
from app.utils.exceptions import GuardrailError

logger = logging.getLogger(__name__)


async def executor_node(
    state: dict, *, db: DatabaseService, validator: SQLValidator
) -> dict:
    """Node 3: SQL guardrail validation + execution.

    First passes the generated SQL through the sqlglot guardrail to ensure:
    - Only SELECT statements
    - No PII table/column access

    Then executes against Postgres in a read-only transaction (defense in depth).
    """
    sql = state["generated_sql"]

    if not sql:
        return {
            "error_message": "No SQL to execute (planner returned empty query)",
            "is_valid": False,
            "guardrail_passed": False,
            "reasoning": [
                ReasoningStep(
                    step="Executor",
                    thought="No SQL provided by planner",
                    action="Returning error for self-healing",
                )
            ],
        }

    # --- Guardrail check ---
    try:
        cleaned_sql = validator.validate(sql)
    except GuardrailError as e:
        logger.warning(f"Guardrail blocked SQL: {e.violation_type} - {e}")
        return {
            "error_message": f"Guardrail blocked: {e}",
            "guardrail_passed": False,
            "guardrail_message": str(e),
            "is_valid": False,
            "reasoning": [
                ReasoningStep(
                    step="Guardrail",
                    thought=f"SQL blocked by security guardrail: {e.violation_type}",
                    action=f"Violation: {e}",
                )
            ],
        }

    # --- Execute query ---
    try:
        rows, columns = await db.execute_query(cleaned_sql)
        logger.info(f"Query executed successfully: {len(rows)} rows returned")
        return {
            "query_result": rows,
            "row_count": len(rows),
            "column_names": columns,
            "generated_sql": cleaned_sql,
            "error_message": None,
            "is_valid": True,
            "guardrail_passed": True,
            "reasoning": [
                ReasoningStep(
                    step="Executor",
                    thought=f"Query executed successfully, returned {len(rows)} rows across {len(columns)} columns",
                    action=f"Executed: {cleaned_sql[:100]}...",
                )
            ],
        }
    except Exception as e:
        logger.error(f"SQL execution failed: {e}")
        return {
            "error_message": str(e),
            "is_valid": False,
            "guardrail_passed": True,
            "reasoning": [
                ReasoningStep(
                    step="Executor",
                    thought=f"SQL execution failed with database error: {e}",
                    action="Passing error to self-healing loop for correction",
                )
            ],
        }
