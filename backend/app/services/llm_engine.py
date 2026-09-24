import json
import os

from openai import APITimeoutError, AsyncOpenAI, RateLimitError

INVEST_CRITERIA = ("independent", "negotiable", "valuable", "estimable", "small", "testable")

LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "5"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """Eres un evaluador experto en metodologías ágiles especializado en el criterio INVEST \
para historias de usuario. Recibirás una historia de usuario y, opcionalmente, el contexto del proyecto \
(backlog relacionado, dependencias, contexto de negocio).

Evalúa los 6 criterios INVEST en español:
- independent: la funcionalidad depende de otros módulos o historias.
- negotiable: la historia da margen de negociación técnica o es demasiado cerrada.
- valuable: el valor de negocio explícito en la sección "para...".
- estimable: si la historia está lo bastante descrita para estimarse en Story Points.
- small: si tiene alcance masivo o mezcla múltiples acciones/requisitos.
- testable: la claridad semántica y facilidad de comprobación.

IMPORTANTE: si no se provee contexto del proyecto, los criterios independent, valuable, estimable y \
small no pueden evaluarse con certeza a partir del texto aislado; en ese caso asigna un score moderado \
(3) y dilo explícitamente en la justificación.

Responde ÚNICAMENTE con un JSON con esta forma exacta, sin texto adicional:
{
  "independent": {"score": <1-5>, "justificacion": "...", "sugerencia": "..."},
  "negotiable": {"score": <1-5>, "justificacion": "...", "sugerencia": "..."},
  "valuable": {"score": <1-5>, "justificacion": "...", "sugerencia": "..."},
  "estimable": {"score": <1-5>, "justificacion": "...", "sugerencia": "..."},
  "small": {"score": <1-5>, "justificacion": "...", "sugerencia": "..."},
  "testable": {"score": <1-5>, "justificacion": "...", "sugerencia": "..."},
  "historia_mejorada": "versión optimizada de la historia que cumple INVEST al 100%"
}"""


class LLMUnavailableError(Exception):
    """Se lanza cuando el LLM excede el timeout o reporta rate limit (degradación elegante)."""


def _build_user_message(story_text: str, project_context: str | None) -> str:
    context_block = project_context or "No se proporcionó contexto de proyecto."
    return f"Historia de usuario:\n{story_text}\n\nContexto del proyecto:\n{context_block}"


async def evaluate_invest_criteria(story_text: str, project_context: str | None = None) -> dict:
    """Evalúa los 6 criterios INVEST vía LLM en JSON mode. Lanza LLMUnavailableError si el servicio falla."""
    client = AsyncOpenAI(timeout=LLM_TIMEOUT_SECONDS)

    try:
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": _build_user_message(story_text, project_context)},
            ],
        )
    except (APITimeoutError, RateLimitError) as exc:
        raise LLMUnavailableError(str(exc)) from exc

    return json.loads(response.choices[0].message.content)
