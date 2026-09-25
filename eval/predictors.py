"""Convierte las salidas del MVP (scores 1-5, reglas spaCy) en predicciones
binarias por criterio INVEST, comparables contra el ground_truth anotado por
expertos.

Umbral de binarizacion acordado con el equipo (2026-09-25): score >= 4 en la
escala 1-5 del LLM se considera "cumple" (1); score < 4 se considera
"incumple" (0).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.services.linguistic_rules import analyze_story_structure  # noqa: E402
from app.services.llm_engine import INVEST_CRITERIA, evaluate_invest_criteria  # noqa: E402

SCORE_THRESHOLD = 4


async def hybrid_prediction(story_text: str, project_context: str | None) -> dict[str, int]:
    """Ejecuta el sistema hibrido completo (spaCy + LLM real) sobre una historia."""
    invest_result = await evaluate_invest_criteria(story_text, project_context)
    return {
        criterion: 1 if invest_result[criterion]["score"] >= SCORE_THRESHOLD else 0
        for criterion in INVEST_CRITERIA
    }


def baseline_prediction(story_text: str) -> dict[str, int]:
    """Baseline solo-reglas (sin LLM): todos los criterios 'cumplen' unicamente
    si la estructura es correcta y no hay ambiguedades detectadas por spaCy.
    Si cualquiera de esas dos condiciones falla, todos los criterios se marcan
    como 'incumple'. Es una regla deliberadamente ingenua para contrastar con
    el sistema hibrido (acordado con el equipo, 2026-09-25)."""
    nlp_result = analyze_story_structure(story_text)
    is_valid = nlp_result["estructura_correcta"] and not nlp_result["ambiguedades_detectadas"]
    value = 1 if is_valid else 0
    return {criterion: value for criterion in INVEST_CRITERIA}
