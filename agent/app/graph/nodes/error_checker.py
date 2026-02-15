import logging

from app.models.response import ErrorAnalysis, ReasoningStep

logger = logging.getLogger(__name__)


async def error_checker_node(
    state: dict, *, error_llm, max_attempts: int = 3
) -> dict:
    """Node 4: Self-healing error checker.

    This is the core innovation of the agentic pipeline. It:
    1. If query succeeded (is_valid=True): generates a final human-readable answer.
    2. If query failed and retries remain: uses the LLM to analyze the error,
       understand the root cause, and produce a corrected SQL query.
    3. If max retries exceeded: returns a failure message.

    The corrected SQL routes back to the Executor node via conditional edge,
    creating the self-healing loop:

        executor -> error_checker -> executor (retry) -> error_checker -> ...
    """
    # --- SUCCESS PATH ---
    if state.get("is_valid", False):
        final_answer = _summarize_result(state)
        logger.info("Query validated successfully, generating final answer")
        return {
            "final_answer": final_answer,
            "reasoning": [
                ReasoningStep(
                    step="Validation",
                    thought="Query executed successfully. No errors to fix.",
                    action="Generating human-readable summary of results",
                )
            ],
        }

    # --- SELF-HEALING PATH ---
    current_attempt = state.get("attempt_count", 0) + 1

    # Max retries exceeded
    if current_attempt > max_attempts:
        logger.warning(f"Max self-heal attempts ({max_attempts}) exceeded")
        return {
            "attempt_count": current_attempt,
            "final_answer": (
                f"Unable to generate a valid query after {max_attempts} attempts. "
                f"Last error: {state.get('error_message', 'Unknown error')}"
            ),
            "reasoning": [
                ReasoningStep(
                    step=f"Self-Heal (attempt {current_attempt})",
                    thought=f"Maximum retry attempts ({max_attempts}) exceeded",
                    action="Returning failure response to user",
                )
            ],
        }

    # Ask LLM to fix the query
    context = "\n\n".join(
        t["document"] for t in state.get("relevant_tables", []) if "document" in t
    )

    messages = [
        (
            "system",
            (
                "You are a PostgreSQL debugging expert. A SQL query failed with an error. "
                "Analyze the error, identify the root cause, and produce a corrected "
                "PostgreSQL SELECT query.\n\n"
                "RULES:\n"
                "- Use ONLY tables and columns from the schema context.\n"
                "- The corrected query must be a valid SELECT statement.\n"
                "- Fix the specific error — don't rewrite the entire approach unless necessary.\n"
                "- If the error is about a missing column/table, find the correct name "
                "from the schema context.\n\n"
                f"Available Schema:\n{context}"
            ),
        ),
        (
            "human",
            (
                f"Original question: {state['user_query']}\n\n"
                f"Failed SQL:\n{state.get('generated_sql', 'N/A')}\n\n"
                f"Error message:\n{state.get('error_message', 'Unknown error')}\n\n"
                f"This is self-heal attempt {current_attempt} of {max_attempts}. "
                f"Please analyze the error and provide a corrected query."
            ),
        ),
    ]

    logger.info(f"Self-healing attempt {current_attempt}/{max_attempts}")

    analysis: ErrorAnalysis = await error_llm.ainvoke(messages)

    logger.info(f"Self-heal produced corrected SQL: {analysis.corrected_sql[:100]}...")

    return {
        "generated_sql": analysis.corrected_sql,
        "attempt_count": current_attempt,
        "error_message": None,
        "is_valid": False,  # Will be re-validated by executor on next loop
        "reasoning": [
            ReasoningStep(
                step=f"Self-Heal (attempt {current_attempt}/{max_attempts})",
                thought=f"Error cause: {analysis.error_cause}. Fix: {analysis.fix_reasoning}",
                action=f"Corrected SQL: {analysis.corrected_sql[:120]}...",
            )
        ],
    }


def _summarize_result(state: dict) -> str:
    """Generate a human-readable summary of the query results."""
    row_count = state.get("row_count", 0)
    columns = state.get("column_names", [])

    if row_count == 0:
        return "The query returned no results."

    if row_count == 1:
        row = state["query_result"][0]
        parts = [f"{k}: {v}" for k, v in row.items()]
        return "Result: " + ", ".join(parts)

    # For multi-row results, give a concise summary
    sample = state["query_result"][:3]
    summary = f"Query returned {row_count} rows across columns: {', '.join(columns)}."

    if row_count <= 5:
        rows_text = []
        for row in state["query_result"]:
            rows_text.append(", ".join(f"{k}: {v}" for k, v in row.items()))
        summary += "\n" + "\n".join(rows_text)
    else:
        summary += f" Showing first 3 of {row_count} rows."

    return summary
