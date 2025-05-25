from moviepy.editor import ImageClip, AudioFileClip

def image_audio_to_video(image_path, audio_path, output_path):
    audio = AudioFileClip(audio_path)
    clip = ImageClip(image_path).set_duration(audio.duration)
    clip = clip.set_audio(audio)
    clip.write_videofile(output_path, codec='libx264', fps=24)