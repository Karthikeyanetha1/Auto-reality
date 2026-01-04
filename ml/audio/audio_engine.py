import os
import json
import subprocess
import numpy as np
import soundfile as sf
from pathlib import Path

MODEL_PATH = "fan_audio_model.npz"
LABELS_PATH = "labels.json"
TMP_WAV = "__tmp_engine.wav"
FFT_BINS = 128
TARGET_SR = 16000


# ---------------- AUDIO FIX ----------------
def _fix_audio(input_path):
    if Path(TMP_WAV).exists():
        Path(TMP_WAV).unlink()

    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", str(TARGET_SR),
        "-sample_fmt", "s16",
        TMP_WAV
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode != 0 or not Path(TMP_WAV).exists():
        raise RuntimeError("FFmpeg failed to convert audio")

    return TMP_WAV


# ---------------- FEATURE EXTRACTION ----------------
def _extract_features(wav_path):
    y, sr = sf.read(wav_path)

    if y.ndim > 1:
        y = y.mean(axis=1)

    if len(y) < TARGET_SR:
        y = np.pad(y, (0, TARGET_SR - len(y)))
    else:
        y = y[:TARGET_SR]

    spectrum = np.abs(np.fft.rfft(y))[:FFT_BINS]
    spectrum = spectrum / (np.linalg.norm(spectrum) + 1e-9)

    return spectrum


# ---------------- LOAD MODEL (ONCE) ----------------
_model = None
_labels = None


def _load_model():
    global _model, _labels

    if _model is not None:
        return

    data = np.load(MODEL_PATH, allow_pickle=True)
    _model = data["centroids"].item()

    with open(LABELS_PATH, "r") as f:
        _labels = json.load(f)


# ---------------- PUBLIC API ----------------
def predict_audio(audio_path):
    """
    Main prediction function.
    Returns dict:
    {
        label: str,
        confidence: float,
        distance: float
    }
    """

    if not Path(audio_path).exists():
        raise FileNotFoundError(f"Audio not found: {audio_path}")

    _load_model()

    fixed = _fix_audio(audio_path)
    feat = _extract_features(fixed)

    distances = {}
    for class_id, centroid in _model.items():
        distances[int(class_id)] = np.linalg.norm(centroid - feat)

    best_id = min(distances, key=distances.get)
    best_dist = distances[best_id]

    label = _labels[str(best_id)]

    # confidence: inverse-distance scaled
    confidence = 1 / (1 + best_dist)

    # cleanup
    Path(TMP_WAV).unlink(missing_ok=True)

    return {
        "label": label,
        "confidence": round(float(confidence), 3),
        "distance": round(float(best_dist), 3)
    }
