from unittest.mock import MagicMock, patch

from api_client import validate_story

FAKE_RESPONSE_JSON = {
    "score": 85,
    "invest_results": {"independent": {"score": 5, "justificacion": "ok", "sugerencia": "ninguna"}},
    "nlp_issues": {"errores_sintacticos": [], "ambiguedades_detectadas": []},
    "degraded": False,
    "degraded_reason": None,
}


def test_validate_story_sends_expected_payload_and_returns_json():
    mock_response = MagicMock()
    mock_response.json.return_value = FAKE_RESPONSE_JSON
    mock_response.raise_for_status.return_value = None

    with patch("api_client.requests.post", return_value=mock_response) as mock_post:
        result = validate_story("Como PO quiero X para Y", project_context="contexto de prueba")

    mock_post.assert_called_once()
    _, kwargs = mock_post.call_args
    assert kwargs["json"] == {"story_text": "Como PO quiero X para Y", "project_context": "contexto de prueba"}
    assert result == FAKE_RESPONSE_JSON
