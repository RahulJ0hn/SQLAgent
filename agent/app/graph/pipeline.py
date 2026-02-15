import logging
from functools import partial

from langgraph.graph import StateGraph, START, END

from app.models.state import AgentState
from app.graph.nodes.discovery import discovery_node
from app.graph.nodes.planner import planner_node
from app.graph.nodes.executor import executor_node
from app.graph.nodes.error_checker import error_checker_node
from app.graph.edges import should_retry_or_finish
from app.services.database import DatabaseService
from app.services.chroma import ChromaService
from app.guardrails.sql_validator import SQLValidator

logger = logging.getLogger(__name__)


def build_agent_graph(
    *,
    chroma: ChromaService,
    db: DatabaseService,
    validator: SQLValidator,
    planner_llm,
    error_llm,
    max_attempts: int = 3,
):
    """Construct and compile the 4-node LangGraph agent pipeline.

    Graph topology:

        START -> discovery -> planner -> executor -> error_checker
                                            ^              |
                                            |   (retry)    |
                                            +--------------+
                                                           |
                                                           v (success or max attempts)
                                                          END

    Args:
        chroma: ChromaDB service for schema metadata lookups
        db: Database service for SQL execution
        validator: SQL guardrail validator
        planner_llm: LLM bound to SQLPlan structured output
        error_llm: LLM bound to ErrorAnalysis structured output
        max_attempts: Maximum self-healing retry attempts

    Returns:
        Compiled LangGraph agent
    """
    # Bind dependencies to node functions via partial
    _discovery = partial(discovery_node, chroma=chroma)
    _planner = partial(planner_node, planner_llm=planner_llm)
    _executor = partial(executor_node, db=db, validator=validator)
    _error_checker = partial(
        error_checker_node, error_llm=error_llm, max_attempts=max_attempts
    )

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("discovery", _discovery)
    graph.add_node("planner", _planner)
    graph.add_node("executor", _executor)
    graph.add_node("error_checker", _error_checker)

    # Linear edges: START -> discovery -> planner -> executor -> error_checker
    graph.add_edge(START, "discovery")
    graph.add_edge("discovery", "planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "error_checker")

    # Conditional edge: self-healing loop or END
    graph.add_conditional_edges(
        "error_checker",
        should_retry_or_finish,
        {"executor": "executor", END: END},
    )

    compiled = graph.compile()
    logger.info(
        f"Agent graph compiled: 4 nodes, self-healing loop (max {max_attempts} retries)"
    )
    return compiled
