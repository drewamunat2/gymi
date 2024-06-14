from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image
import numpy as np
import sys

def resize_frame(frame, target_width, target_height):
    # Convert frame to PIL image
    pil_image = Image.fromarray(frame)
    # Resize image using LANCZOS filter
    pil_image = pil_image.resize((target_width, target_height), Image.LANCZOS)
    # Convert back to numpy array
    return np.array(pil_image)

def resize_clip(clip, target_width, target_height):
    # Apply resize_frame to each frame of the clip
    return clip.fl_image(lambda frame: resize_frame(frame, target_width, target_height))

def mash_videos(video_files, target_width=1920, target_height=1080):
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
