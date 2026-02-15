class AgentError(Exception):
    """Base exception for the agent service."""

    pass


class GuardrailError(AgentError):
    """Raised when SQL fails guardrail validation."""

    def __init__(self, message: str, violation_type: str):
        self.violation_type = violation_type
        super().__init__(message)


class DatabaseError(AgentError):
    """Raised when a database operation fails."""

    pass


class SchemaReflectionError(AgentError):
    """Raised when schema reflection fails."""

    pass
