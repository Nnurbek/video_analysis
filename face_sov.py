import cv2
import os

  
def extract_frames(video_path, frames_dir, prefix, interval=10):
    os.makedirs(frames_dir, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    frame_count = 0

    while success:
        if frame_count % interval == 0:
            frame_path = os.path.join(frames_dir, f"{prefix}_frame_{count:04d}.jpg")
            cv2.imwrite(frame_path, image)    
            count += 1
        success, image = vidcap.read()
        frame_count += 1
    return frames_dir

  
video_files = [
    'videos/bloger.mp4',  
    'videos/my_heart.mp4',
    'videos/norm.mp4',
    'videos/test.mp4',
    'videos/john.mp4'
]

  
for video_file in video_files:
    video_name = os.path.basename(video_file)
    frames_dir = f"frames_{video_name}"
    extract_frames(video_file, frames_dir, video_name)
