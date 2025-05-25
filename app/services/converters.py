import os
from moviepy.editor import ImageClip, AudioFileClip

UPLOAD_DIR = os.path.join("app", "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def image_audio_to_video(image_path, audio_path, title):
    """
    Combines image_path + audio_path into an MP4 saved under UPLOAD_DIR,
    using the image's base name for the output filename.
    Returns the full path to the generated video.
    """
    out_path = os.path.join(UPLOAD_DIR, f"{title}.mp4")

    audio = AudioFileClip(audio_path)
    clip = ImageClip(image_path).set_duration(audio.duration)
    clip = clip.set_audio(audio)
    clip.write_videofile(out_path, codec="libx264", fps=24)

    clip.close()
    audio.close()

    return out_path
