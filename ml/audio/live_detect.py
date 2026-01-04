import os
import sys
import subprocess
from audio_engine import predict_audio

TMP_WAV = "__live_input.wav"

def record_mobile(seconds=3):
    print(f"🎙 Recording {seconds} seconds (mobile mic)...")

    # Record using Termux API (creates .m4a in storage)
    subprocess.run([
        "termux-microphone-record",
        "-l", str(seconds),
        "-f", "live.m4a"
    ], check=True)

    # Convert to required WAV format
    subprocess.run([
        "ffmpeg", "-y",
        "-i", "live.m4a",
        "-ac", "1",
        "-ar", "16000",
        TMP_WAV
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(TMP_WAV):
        raise RuntimeError("❌ Audio conversion failed")

def main():
    record_mobile(3)

    result = predict_audio(TMP_WAV)

    print("\n🔊 LIVE AUDIO RESULT")
    print("🧠 Prediction :", result["label"])
    print("📊 Confidence :", result["confidence"])
    print("📏 Distance   :", result["distance"])

    os.remove(TMP_WAV)
    os.remove("live.m4a")

if __name__ == "__main__":
    main()
