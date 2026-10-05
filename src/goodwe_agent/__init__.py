"""GoodWe Charge Assistant - Sprint 04."""

__all__ = ["AgentResponse", "GoodWeAgent"]


def __getattr__(name):
    """Evita carregar dependências de agentes ao usar apenas artefatos históricos."""
    if name in __all__:
        from .agent import AgentResponse, GoodWeAgent
        return {"AgentResponse": AgentResponse, "GoodWeAgent": GoodWeAgent}[name]
    raise AttributeError(name)

