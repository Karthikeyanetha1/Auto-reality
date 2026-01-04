import os
import json
import numpy as np
import soundfile as sf
from scipy.fft import rfft
from scipy.linalg import norm

# ---------------- CONFIG ----------------
BASE_DIR = "../../dataset/fan"
CLASSES = ["bearing_issue", "imbalance", "normal"]
SAMPLE_RATE = 16000
FEATURE_SIZE = 128
MODEL_OUT = "fan_audio_model.npz"
LABELS_OUT = "labels.json"

# ---------------- FEATURE EXTRACTION ----------------
def extract_features(wav_path):
    try:
        audio, sr = sf.read(wav_path)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)

        if sr != SAMPLE_RATE:
            return None

        # Trim / pad
        if len(audio) < SAMPLE_RATE:
            audio = np.pad(audio, (0, SAMPLE_RATE - len(audio)))
        else:
            audio = audio[:SAMPLE_RATE]

        # FFT features
        spectrum = np.abs(rfft(audio))[:FEATURE_SIZE]
        spectrum = spectrum / (norm(spectrum) + 1e-8)
        return spectrum

    except Exception as e:
        print(f"SKIP: {wav_path} ({e})")
        return None

# ---------------- LOAD DATASET ----------------
X = []
y = []

for label_id, cls in enumerate(CLASSES):
    audio_dir = os.path.join(BASE_DIR, cls, "audio")
    print(f"\n📂 Processing {cls} ...")

    for file in os.listdir(audio_dir):
        if not file.endswith(".wav"):
            continue

        path = os.path.join(audio_dir, file)
        feat = extract_features(path)
        if feat is not None:
            X.append(feat)
            y.append(label_id)

X = np.array(X)
y = np.array(y)

if len(X) == 0:
    raise RuntimeError("❌ No valid audio files loaded")

print("\n✅ Dataset Loaded")
print("Samples:", X.shape[0])
print("Feature size:", X.shape[1])

# ---------------- SIMPLE CLASSIFIER ----------------
# Nearest-centroid classifier (very reliable)
centroids = {}
for cls_id in range(len(CLASSES)):
    centroids[cls_id] = X[y == cls_id].mean(axis=0)

# ---------------- SAVE MODEL ----------------
np.savez(
    MODEL_OUT,
    centroids=centroids,
    classes=np.array(CLASSES)
)

with open(LABELS_OUT, "w") as f:
    json.dump({i: c for i, c in enumerate(CLASSES)}, f, indent=2)

print("\n💾 Model saved:")
print(" -", MODEL_OUT)
print(" -", LABELS_OUT)
print("\n🎉 TRAINING COMPLETE")
