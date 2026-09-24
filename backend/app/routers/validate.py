from fastapi import APIRouter

from app.models.user_story import UserStoryInput
from app.services.orchestrator import validate_user_story

router = APIRouter()


@router.post("/api/v1/validate")
async def validate_story(payload: UserStoryInput) -> dict:
    return await validate_user_story(payload.story_text, payload.project_context)
