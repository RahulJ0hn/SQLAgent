import logging

from app.models.response import SQLPlan, ReasoningStep

logger = logging.getLogger(__name__)


async def planner_node(state: dict, *, planner_llm) -> dict:
    """Node 2: LLM-based SQL generation with structured output.

    Uses the relevant schema context from the Discovery node to generate
    a PostgreSQL SELECT query. Returns structured output (SQLPlan) that
    includes the SQL, reasoning chain, and chart suggestion.
    """
    context = "\n\n".join(
        t["document"] for t in state["relevant_tables"] if "document" in t
    )

    if not context:
        return {
            "generated_sql": "",
            "error_message": "No relevant schema context found. Try reflecting the schema first.",
            "is_valid": False,
            "reasoning": [
                ReasoningStep(
                    step="Planner",
                    thought="No schema context available from Discovery node",
                    action="Cannot generate SQL without schema information",
                )
            ],
        }

    messages = [
        (
            "system",
            (
                "You are an expert PostgreSQL analyst. Generate a SELECT query to "
                "answer the user's question.\n\n"
                "RULES:\n"
                "- Use ONLY the tables and columns listed in the schema context below.\n"
                "- NEVER guess or invent column/table names.\n"
                "- Always use proper JOIN conditions.\n"
                "- Use aggregations and GROUP BY when the question implies summaries.\n"
                "- Limit results to 100 rows unless the user asks for more.\n"
                "- Use descriptive column aliases.\n\n"
                f"Available Schema:\n{context}"
            ),
        ),
        ("human", state["user_query"]),
    ]

    plan: SQLPlan = await planner_llm.ainvoke(messages)

    logger.info(f"Planner generated SQL: {plan.sql[:100]}...")

    return {
        "generated_sql": plan.sql,
        "reasoning": plan.reasoning,
        "chart_suggestion": {
            "type": plan.chart_type.value,
            "config": plan.chart_config,
        },
    }
