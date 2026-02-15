from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ChartType(str, Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    TABLE = "table"
    SCALAR = "scalar"


class ReasoningStep(BaseModel):
    """A single step in the agent's reasoning chain."""

    step: str = Field(description="Name of the reasoning step (e.g., Discovery, Planner)")
    thought: str = Field(description="Human-readable explanation of what happened")
    action: Optional[str] = Field(default=None, description="Action taken, if any")


class SQLPlan(BaseModel):
    """Structured output the LLM returns from the Planner node."""

    sql: str = Field(description="The PostgreSQL SELECT query to execute")
    reasoning: list[ReasoningStep] = Field(description="Chain of reasoning steps")
    chart_type: ChartType = Field(description="Suggested visualization type for the result")
    chart_config: Optional[dict] = Field(
        default=None, description="Optional chart configuration (labels, axes, etc.)"
    )


class ErrorAnalysis(BaseModel):
    """Structured output the LLM returns when analyzing a SQL error."""

    error_cause: str = Field(description="Root cause of the SQL error")
    corrected_sql: str = Field(description="The corrected PostgreSQL SELECT query")
    fix_reasoning: str = Field(description="Explanation of what was fixed and why")


class IntentClassification(BaseModel):
    """Structured output for intent classification."""

    intent: str = Field(description="Either 'data_query' if the user is asking about database data, or 'general' if it's a conversational/general question")
    response: Optional[str] = Field(default=None, description="If intent is 'general', provide a helpful response. If intent is 'data_query', leave this null.")


class QueryResponse(BaseModel):
    """Final API response sent to the orchestrator/client."""

    type: str = "data"  # "data" or "chat"
    sql: str = ""
    result: list[dict] = []
    row_count: int = 0
    columns: list[str] = []
    reasoning: list[ReasoningStep] = []
    chart_type: ChartType = ChartType.TABLE
    chart_config: Optional[dict] = None
    attempts: int = 0
    final_answer: str = ""
