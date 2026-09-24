from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

FAKE_RESULT = {
    "score": 85,
    "invest_results": {"independent": {"score": 5, "justificacion": "ok", "sugerencia": "ninguna"}},
    "nlp_issues": {"errores_sintacticos": [], "ambiguedades_detectadas": []},
    "degraded": False,
    "degraded_reason": None,
}


def test_validate_endpoint_returns_orchestrator_result():
    with patch(
        "app.routers.validate.validate_user_story",
        new=AsyncMock(return_value=FAKE_RESULT),
    ):
        response = client.post(
            "/api/v1/validate",
            json={
                "story_text": "Como PO quiero registrar una historia para iniciar su análisis.",
                "project_context": None,
            },
        )

    assert response.status_code == 200
    assert response.json() == FAKE_RESULT


def test_validate_endpoint_rejects_empty_story_text():
    response = client.post("/api/v1/validate", json={"story_text": ""})

    assert response.status_code == 422
