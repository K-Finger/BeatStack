from typing import List, Optional
import os
import httpx

API_KEY = os.getenv("RAPIDTAGS_API_KEY", "")
if not API_KEY:
    raise RuntimeError("RAPIDTAGS_API_KEY environment variable is not set")

BASE_URL = "https://rapidtags.io/api"

async def generate_tags(title: str, video_url: Optional[str] = None) -> List[str]:
    """
    Generates a list of tags based on a video title and optional video URL.

    :param title: The title of the video.
    :param video_url: An optional URL to provide additional context.
    :return: A list of suggested tags.
    """
    payload = {"title": title}
    if video_url:
        payload["source"] = video_url

    headers = {"Authorization": f"Bearer {API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/generate",
            json=payload,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

    tags = data.get("tags")
    if not isinstance(tags, list):
        raise RuntimeError("Unexpected response format from RapidTags.io: 'tags' field is missing or invalid")

    return tags
