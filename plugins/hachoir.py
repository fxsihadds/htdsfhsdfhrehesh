from PIL import Image
from random import randint
from moviepy.editor import VideoFileClip


def get_video_duration(video_file_path):
    try:
        with VideoFileClip(video_file_path) as video_clip:
            duration = int(video_clip.duration)
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return None


def thumbnail_video(video_file_path):
    duration = get_video_duration(video_file_path)
    rnm = str(randint(0, duration))

    try:
        with VideoFileClip(video_file_path) as video_clip:
            thumbnail_frame = video_clip.get_frame(rnm)
            thumbnail_image = Image.fromarray(thumbnail_frame)
            thumbnail_image.save('thumbnail.png')
    except Exception as e:
        print(f"Error: {e}")

    return
