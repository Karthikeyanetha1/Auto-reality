import subprocess
import os
from PIL import Image

def analyze_video(video_path):
    os.makedirs("tmp_frames", exist_ok=True)

    # Extract 1 frame per second
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", "fps=1",
        "tmp_frames/frame_%03d.jpg"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    frames = os.listdir("tmp_frames")

    if len(frames) < 3:
        return {
            "type": "video",
            "issues": ["Video too short or unstable"],
            "recommendation": "Record steady video (5–10 sec)"
        }

    return {
        "type": "video",
        "issues": ["Possible vibration or movement detected"],
        "recommendation": "Check mounting screws or imbalance"
    }
