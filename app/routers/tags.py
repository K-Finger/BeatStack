from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.tag_service import TagService

router = APIRouter(prefix="/api/tags", tags=["tags"])


class TagRequest(BaseModel):
    title: str
    video_url: str | None = None  # optional, if you want to send a hosted URL


class TagResponse(BaseModel):
    tags: list[str]


@router.post("/generate", response_model=TagResponse)
async def generate_tags(request: TagRequest):
    try:
        service = TagService()
        tags = await service.generate_tags(request.title, request.video_url)
        return TagResponse(tags=tags)

    except Exception as e:
        raise HTTPException(status_code=502, detail="Failed to fetch tags from RapidTags.io")
