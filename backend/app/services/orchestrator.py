from app.services.linguistic_rules import analyze_story_structure
from app.services.llm_engine import INVEST_CRITERIA, LLMUnavailableError, evaluate_invest_criteria


def _calculate_score(nlp_result: dict, invest_result: dict | None) -> int:
    """Combina la validación sintáctica local con los scores INVEST del LLM en un score 0-100."""
    structural_score = 100 if nlp_result["estructura_correcta"] else 40
    structural_score -= len(nlp_result["ambiguedades_detectadas"]) * 5

    if invest_result is None:
        return max(0, structural_score)

    invest_scores = [invest_result[criterion]["score"] for criterion in INVEST_CRITERIA]
    invest_score = (sum(invest_scores) / (len(invest_scores) * 5)) * 100

    return max(0, round((structural_score * 0.4) + (invest_score * 0.6)))


async def validate_user_story(story_text: str, project_context: str | None = None) -> dict:
    """Orquesta el análisis híbrido (spaCy + LLM) y consolida la respuesta de /api/v1/validate."""
    nlp_result = analyze_story_structure(story_text)

    degraded = False
    invest_result = None
    try:
        invest_result = await evaluate_invest_criteria(story_text, project_context)
    except LLMUnavailableError:
        degraded = True

    return {
        "score": _calculate_score(nlp_result, invest_result),
        "invest_results": invest_result,
        "nlp_issues": {
            "errores_sintacticos": nlp_result["errores_sintacticos"],
            "ambiguedades_detectadas": nlp_result["ambiguedades_detectadas"],
        },
        "degraded": degraded,
        "degraded_reason": (
            "El servicio de IA no respondió a tiempo; se muestra únicamente el análisis sintáctico local."
            if degraded
            else None
        ),
    }
