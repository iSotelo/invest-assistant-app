import os

import requests

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


def validate_story(story_text: str, project_context: str | None = None, timeout: float = 15.0) -> dict:
    """Invoca POST /api/v1/validate en el backend y retorna el JSON de resultado."""
    response = requests.post(
        f"{BACKEND_API_URL}/api/v1/validate",
        json={"story_text": story_text, "project_context": project_context},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()
