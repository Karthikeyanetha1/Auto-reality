# engine/ai_router.py

from engine.image_engine import analyze_image
from engine.video_engine import analyze_video
from engine.audio_engine import analyze_audio
from engine.overlay_engine import generate_actions

def run_diagnosis(file_path, file_type):
    if file_type == "image":
        analysis = analyze_image(file_path)

    elif file_type == "video":
        analysis = analyze_video(file_path)

    elif file_type == "audio":
        analysis = analyze_audio(file_path)

    else:
        return {
            "error": "Unsupported file type"
        }

    actions = generate_actions(analysis)

    return {
        "analysis": analysis,
        "actions": actions
    }
