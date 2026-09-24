from unittest.mock import AsyncMock, patch

import pytest

from app.services.llm_engine import LLMUnavailableError
from app.services.orchestrator import validate_user_story

VALID_STORY = "Como usuario registrado quiero restablecer mi contraseña para recuperar el acceso a mi cuenta."

FAKE_INVEST_RESULT = {
    "independent": {"score": 5, "justificacion": "ok", "sugerencia": "ninguna"},
    "negotiable": {"score": 4, "justificacion": "ok", "sugerencia": "ninguna"},
    "valuable": {"score": 5, "justificacion": "ok", "sugerencia": "ninguna"},
    "estimable": {"score": 4, "justificacion": "ok", "sugerencia": "ninguna"},
    "small": {"score": 5, "justificacion": "ok", "sugerencia": "ninguna"},
    "testable": {"score": 5, "justificacion": "ok", "sugerencia": "ninguna"},
    "historia_mejorada": VALID_STORY,
}


@pytest.mark.asyncio
async def test_validate_user_story_combines_nlp_and_llm_results():
    with patch(
        "app.services.orchestrator.evaluate_invest_criteria",
        new=AsyncMock(return_value=FAKE_INVEST_RESULT),
    ):
        result = await validate_user_story(VALID_STORY, project_context="Módulo de autenticación")

    assert result["degraded"] is False
    assert result["invest_results"] == FAKE_INVEST_RESULT
    assert 0 <= result["score"] <= 100
    assert result["nlp_issues"]["errores_sintacticos"] == []


@pytest.mark.asyncio
async def test_validate_user_story_degrades_gracefully_when_llm_unavailable():
    with patch(
        "app.services.orchestrator.evaluate_invest_criteria",
        new=AsyncMock(side_effect=LLMUnavailableError("timeout")),
    ):
        result = await validate_user_story(VALID_STORY)

    assert result["degraded"] is True
    assert result["invest_results"] is None
    assert result["degraded_reason"] is not None
    assert 0 <= result["score"] <= 100


@pytest.mark.asyncio
async def test_validate_user_story_penalizes_ambiguous_words_in_score():
    ambiguous_story = "Como PO quiero una interfaz rápida y amigable para mejorar la experiencia."

    with patch(
        "app.services.orchestrator.evaluate_invest_criteria",
        new=AsyncMock(return_value=FAKE_INVEST_RESULT),
    ):
        clean_result = await validate_user_story(VALID_STORY)
        ambiguous_result = await validate_user_story(ambiguous_story)

    assert ambiguous_result["score"] <= clean_result["score"]
