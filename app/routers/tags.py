# from fastapi import APIRouter, HTTPException, Request
# from app.services.tag_service import generate_tags

# router = APIRouter(prefix="/api/tags")

# @router.post("/generate")
# async def generate(request: Request):
#     data = await request.json()
#     title = data.get("title")
#     video_url = data.get("video_url")
#     if not title:
#         raise HTTPException(status_code=400, detail="title required")
#     try:
#         tags = await generate_tags(title, video_url)
#         return {"tags": tags}
#     except Exception:
#         raise HTTPException(status_code=502, detail="Failed to fetch tags")
