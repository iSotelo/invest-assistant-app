from pydantic import BaseModel, Field


class UserStoryInput(BaseModel):
    """Payload de entrada para registrar una historia de usuario a analizar."""

    story_text: str = Field(..., min_length=1, description="Historia completa en formato Como/Quiero/Para")
    project_context: str | None = Field(
        default=None,
        description="Contexto del proyecto (backlog, dependencias, negocio) requerido para evaluar Independent, Valuable, Estimable y Small",
    )
