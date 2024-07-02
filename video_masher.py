from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image
import numpy as np
import sys

def resize_frame(frame, target_width, target_height):
    # Convert frame to PIL image
    pil_image = Image.fromarray(frame)

    # Calculate the aspect ratio of the original frame
    original_width, original_height = pil_image.size
    original_aspect_ratio = original_width / original_height

    # Calculate the target aspect ratio
    target_aspect_ratio = target_width / target_height

    # Determine how to resize the image to maintain the aspect ratio
    if original_aspect_ratio > target_aspect_ratio:
        # Resize based on height
        new_height = target_height
        new_width = int(new_height * original_aspect_ratio)
    else:
        # Resize based on width
        new_width = target_width
        new_height = int(new_width / original_aspect_ratio)

    # Resize the image
    pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)

    # Crop the image to the target dimensions
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    pil_image = pil_image.crop((left, top, right, bottom))

    # Convert back to numpy array
    return np.array(pil_image)

def resize_clip(clip, target_width, target_height):
    # Apply resize_frame to each frame of the clip
    return clip.fl_image(lambda frame: resize_frame(frame, target_width, target_height))

def mash_videos(video_files, target_width=1080, target_height=1920):
    clips = []
    for video in video_files:
        clip = VideoFileClip(video)
        # Resize each clip to the target dimensions
        clip = resize_clip(clip, target_width, target_height)
        clips.append(clip)
    
    # Concatenate all the resized clips
    final_clip = concatenate_videoclips(clips, method="compose")
    # Write the final video file
    final_clip.write_videofile("output_video.mp4", codec="libx264", fps=24)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_files = sys.argv[1:]
        mash_videos(video_files)
    else:
        print("Please provide video file paths as arguments.")
