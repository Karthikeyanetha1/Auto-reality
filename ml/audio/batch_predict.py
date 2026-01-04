import os
import csv
from audio_engine import predict_audio

AUDIO_DIR = "../../dataset/fan/bearing_issue/audio"
OUT_CSV = "batch_results.csv"


def main():
    rows = []
    files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")]

    print(f"🔍 Processing {len(files)} audio files...")

    for fname in files:
        path = os.path.join(AUDIO_DIR, fname)
        try:
            result = predict_audio(path)
            rows.append([
                fname,
                result["label"],
                result["confidence"],
                result["distance"]
            ])
            print("✔", fname, "→", result["label"])
        except Exception as e:
            print("✖", fname, "→ ERROR:", e)

    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "prediction", "confidence", "distance"])
        writer.writerows(rows)

    print(f"\n📄 Results saved to {OUT_CSV}")


if __name__ == "__main__":
    main()
