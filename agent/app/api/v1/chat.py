import logging

from fastapi import APIRouter, Depends, HTTPException, Request

from app.dependencies import get_agent
from app.models.request import QueryRequest
from app.models.response import QueryResponse

logger = logging.getLogger(__name__)

INTENT_SYSTEM_PROMPT = """You are an intelligent intent classifier for an enterprise SQL database assistant.

Your job is to determine if the user's message is:
1. A "data_query" — they want to retrieve, analyze, or explore data from the database. The database contains: customers, orders, order_items, products, subscriptions, and support_tickets for a Retail/SaaS business.
2. A "general" question — greetings, help requests, questions unrelated to the database, general knowledge, etc.

If the intent is "general", provide a helpful, professional response. Keep these rules:
- If the user greets you, greet them back and briefly explain you're an SQL database assistant that helps analyze customer, order, product, subscription, and support data.
- If the user asks what you can do or how you help, explain your capabilities clearly: you translate natural language questions into SQL, execute them safely against the database, auto-correct errors, and visualize results.
- If the user asks something completely outside your scope (geography, science, general knowledge, etc.), politely redirect them. Say something like "That's outside my area of expertise. I'm specialized in analyzing your business data — customers, orders, products, subscriptions, and support tickets. Try asking me something like 'What are the top customers by revenue?'"
- Be professional, concise, and friendly. No emojis.
- Never make up data or pretend to query the database for general questions."""

router = APIRouter()


@router.post("/chat", response_model=QueryResponse)
async def chat(req: QueryRequest, request: Request, agent=Depends(get_agent)):
    """Smart chat endpoint with intent classification.

    1. Classifies the user's intent (data query vs general question)
    2. General questions → LLM responds directly (no SQL pipeline)
    3. Data queries → full SQL agent pipeline
    """
    intent_llm = request.app.state.intent_llm
    question = req.question

    # Step 1: Classify intent
    try:
        classification = await intent_llm.ainvoke([
            ("system", INTENT_SYSTEM_PROMPT),
            ("human", question),
        ])
        logger.info(f"Intent classified as: {classification.intent}")
    except Exception as e:
        logger.error(f"Intent classification failed: {e}", exc_info=True)
        # Default to data query if classification fails
        classification = None

    # Step 2: Handle general questions
    if classification and classification.intent == "general":
        return QueryResponse(
            type="chat",
            final_answer=classification.response or "I'm here to help you analyze your business data. Try asking a question about customers, orders, or subscriptions.",
        )

    # Step 3: Data query — run the full SQL pipeline
    initial_state = {
        "user_query": question,
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

    chart_type = "table"
    chart_config = None
    if result.get("chart_suggestion"):
        chart_type = result["chart_suggestion"].get("type", "table")
        chart_config = result["chart_suggestion"].get("config")

    return QueryResponse(
        type="data",
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
