import logging

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_agent
from app.models.request import QueryRequest
from app.models.response import QueryResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def run_query(req: QueryRequest, agent=Depends(get_agent)):
    """Execute a natural language query through the agentic SQL pipeline.

    The agent graph runs through 4 nodes:
    1. Discovery: RAG lookup for relevant schema
    2. Planner: LLM generates SQL + reasoning
    3. Executor: Guardrail check + SQL execution
    4. Error Checker: Validates or self-heals (up to 3 retries)
    """
    initial_state = {
        "user_query": req.question,
        "relevant_tables": [],
        "generated_sql": "",
        "reasoning": [],
        "query_result": None,
        "row_count": 0,
        "column_names": [],
        "error_message": None,
        "attempt_count": 0,
        "is_valid": False,
        "guardrail_passed": False,
        "guardrail_message": None,
        "chart_suggestion": None,
        "final_answer": None,
    }

    try:
        result = await agent.ainvoke(initial_state)
    except Exception as e:
        logger.error(f"Agent pipeline failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Agent pipeline error: {e}")

    # Extract chart type safely
    chart_type = "table"
    chart_config = None
    if result.get("chart_suggestion"):
        chart_type = result["chart_suggestion"].get("type", "table")
        chart_config = result["chart_suggestion"].get("config")

    return QueryResponse(
        sql=result.get("generated_sql", ""),
        result=result.get("query_result") or [],
        row_count=result.get("row_count", 0),
        columns=result.get("column_names", []),
        reasoning=result.get("reasoning", []),
        chart_type=chart_type,
        chart_config=chart_config,
        attempts=result.get("attempt_count", 1),
        final_answer=result.get("final_answer", ""),
    )
