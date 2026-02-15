from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # AWS Bedrock
    aws_access_key: str
    aws_secret_key: str
    aws_region: str = "us-east-1"
    model_id: str = "us.anthropic.claude-sonnet-4-20250514-v1:0"

    # PostgreSQL
    pg_host: str = "postgres"
    pg_port: int = 5432
    pg_user: str = "sqlagent"
    pg_password: str = "sqlagent_dev"
    pg_database: str = "retaildb"

    # ChromaDB
    chroma_host: str = "chromadb"
    chroma_port: int = 8000
    chroma_collection: str = "schema_metadata"

    # Agent behavior
    max_self_heal_attempts: int = 3
    pii_blocked_tables: list[str] = ["customer_pii", "payment_methods"]
    pii_blocked_columns: list[str] = ["ssn", "credit_card", "password_hash"]

    # Server
    agent_port: int = 8080

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
