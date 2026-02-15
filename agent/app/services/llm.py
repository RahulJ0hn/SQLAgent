from langchain_aws import ChatBedrockConverse
import boto3

from app.config import Settings
from app.models.response import SQLPlan, ErrorAnalysis, IntentClassification


def get_llm(settings: Settings) -> ChatBedrockConverse:
    """Create a base ChatBedrockConverse instance using AWS Bedrock."""
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
    )

    return ChatBedrockConverse(
        model=settings.model_id,
        client=bedrock_client,
        temperature=0,
        max_tokens=4096,
    )


def get_planner_llm(settings: Settings):
    """Return LLM bound to SQLPlan structured output for the Planner node."""
    llm = get_llm(settings)
    return llm.with_structured_output(SQLPlan)


def get_error_llm(settings: Settings):
    """Return LLM bound to ErrorAnalysis structured output for the Error Checker node."""
    llm = get_llm(settings)
    return llm.with_structured_output(ErrorAnalysis)


def get_intent_llm(settings: Settings):
    """Return LLM bound to IntentClassification structured output."""
    llm = get_llm(settings)
    return llm.with_structured_output(IntentClassification)
