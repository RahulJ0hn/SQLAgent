import logging

from langgraph.graph import END

logger = logging.getLogger(__name__)


def should_retry_or_finish(state: dict) -> str:
    """Conditional edge after error_checker node.

    Routes to:
    - END: if the query was valid, or if max retries exceeded (final_answer set)
    - "executor": if the error_checker produced a corrected SQL for retry

    This creates the self-healing loop:
        executor -> error_checker --(retry)--> executor -> error_checker --> ...
                                  --(done)---> END
    """
    if state.get("is_valid", False):
        logger.info("Query valid — routing to END")
        return END

    if state.get("final_answer"):
        logger.info("Final answer set (max retries or success) — routing to END")
        return END

    logger.info("Routing back to executor for self-heal retry")
    return "executor"
