# live_predict.py
from audio_engine import predict_audio
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python live_predict.py <wav_file>")
        return

    wav_path = sys.argv[1]

    if not os.path.exists(wav_path):
        print("❌ File not found:", wav_path)
        return

    result = predict_audio(wav_path)

    print("\n🔊 LIVE AUDIO RESULT")
    print("🧠 Prediction :", result["label"])
    print("📊 Confidence :", round(result["confidence"], 3))
    print("📏 Distance   :", round(result["distance"], 3))

if __name__ == "__main__":
    main()
