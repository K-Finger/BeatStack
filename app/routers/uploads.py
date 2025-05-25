import os
import re
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from ..services.converters import image_audio_to_video

router = APIRouter()

def safe_filename(name: str) -> str:
    # remove any characters except letters, numbers, dash, underscore, space
    name = re.sub(r"[^\w\-\s]", "", name)
    return name.strip().replace(" ", "_") or "output"

@router.post("/uploads", response_class=FileResponse)
async def upload_and_convert(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    tags: str = Form(""),
    image: UploadFile = File(...),
    audio: UploadFile = File(...),
):
    upload_dir = os.path.join("app", "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    img_path = os.path.join(upload_dir, image.filename)
    aud_path = os.path.join(upload_dir, audio.filename)

    with open(img_path, "wb") as f:
        f.write(await image.read())
    with open(aud_path, "wb") as f:
        f.write(await audio.read())

    print("recieved tags", tags)

    # sanitize and build output path
    base = safe_filename(title)
    out_filename = f"{base}.mp4"
    out_path = os.path.join(upload_dir, out_filename)


    try:
        out_path = image_audio_to_video(img_path, aud_path, title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    background_tasks.add_task(os.remove, img_path)
    background_tasks.add_task(os.remove, aud_path)

    return FileResponse(out_path, media_type="video/mp4")
