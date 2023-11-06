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

def get_file_size(video_file_path) -> bool:
    get_size = os.path.getsize(video_file_path)
    file_size_megabytes = round(get_size / (1024 * 1024))
    print(f"File size: {file_size_megabytes} MB")
    if file_size_megabytes < 1950:
        return True
    else:
        os.remove(video_file_path)
        return False
