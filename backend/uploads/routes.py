# uploads/routes.py
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from .converters import image_audio_to_video

router = APIRouter()

@router.post("/api/uploads", response_class=FileResponse)
async def upload_file(
    image: UploadFile = File(...),
    audio: UploadFile = File(...),
):
    # 1) save uploads to temp files
    suffix_img = os.path.splitext(image.filename)[1]
    suffix_aud = os.path.splitext(audio.filename)[1]

    img_tmp = tempfile.NamedTemporaryFile(suffix=suffix_img, delete=False)
    img_data = await image.read()
    img_tmp.write(img_data)
    img_tmp.close()

    aud_tmp = tempfile.NamedTemporaryFile(suffix=suffix_aud, delete=False)
    aud_data = await audio.read()
    aud_tmp.write(aud_data)
    aud_tmp.close()

    # 2) prepare output path
    out_tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    out_tmp.close()
    output_path = out_tmp.name

    # 3) convert
    try:
        image_audio_to_video(
            img_tmp.name,
            aud_tmp.name,
            output_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 4) return the file
    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename="output.mp4"
    )
