# engine/audio_engine.py

import os

def analyze_audio(file_path):
    filename = os.path.basename(file_path).lower()

    if "motor" in filename or "engine" in filename:
        return {
            "device": "motor/fan",
            "issue": "bearing_noise",
            "confidence": 0.71,
            "source": "audio"
        }

    if "hum" in filename or "buzz" in filename:
        return {
            "device": "electrical_appliance",
            "issue": "electrical_hum",
            "confidence": 0.65,
            "source": "audio"
        }

    return {
        "device": "unknown_appliance",
        "issue": "unidentified_sound",
        "confidence": 0.40,
        "source": "audio"
    }
