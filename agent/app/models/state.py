from typing import TypedDict, Annotated, Optional
import operator

from app.models.response import ReasoningStep


class AgentState(TypedDict):
    """Central state object passed through all LangGraph nodes.

    The `reasoning` field uses `operator.add` so each node appends
    its reasoning steps without overwriting previous ones.
    """

    # Input
    user_query: str

    # Discovery node output
    relevant_tables: list[dict]

    # Planner node output
    generated_sql: str
    reasoning: Annotated[list[ReasoningStep], operator.add]

    # Executor node output
    query_result: Optional[list[dict]]
    row_count: int
    column_names: list[str]

    # Error checker state
    error_message: Optional[str]
    attempt_count: int
    is_valid: bool

    # Guardrail output
    guardrail_passed: bool
    guardrail_message: Optional[str]

    # Final output
    chart_suggestion: Optional[dict]
    final_answer: Optional[str]
