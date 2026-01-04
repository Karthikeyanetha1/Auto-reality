import sys
import json
import numpy as np
import subprocess
import os
import soundfile as sf

TMP_WAV = "__tmp_predict.wav"

def convert_to_wav(input_audio):
    if os.path.exists(TMP_WAV):
        os.remove(TMP_WAV)

    cmd = [
        "ffmpeg", "-y",
        "-i", input_audio,
        "-ac", "1",
        "-ar", "16000",
        "-sample_fmt", "s16",
        TMP_WAV
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.returncode == 0 and os.path.exists(TMP_WAV)


def extract_features(wav_path, n_mfcc=128):
    y, sr = sf.read(wav_path)

    if y.ndim > 1:
        y = y.mean(axis=1)

    # simple FFT-based feature (librosa-free)
    spectrum = np.abs(np.fft.rfft(y))
    spectrum = spectrum[:n_mfcc]

    if len(spectrum) < n_mfcc:
        spectrum = np.pad(spectrum, (0, n_mfcc - len(spectrum)))

    return spectrum


def main():
    if len(sys.argv) != 2:
        print("Usage: python predict_fan_audio.py <audio.wav>")
        sys.exit(1)

    audio_path = sys.argv[1]

    if not convert_to_wav(audio_path):
        print("❌ FFmpeg failed to convert audio:", audio_path)
        sys.exit(1)

    feat = extract_features(TMP_WAV)

    data = np.load("fan_audio_model.npz", allow_pickle=True)
    centroids = data["centroids"].item()

    with open("labels.json") as f:
        id_to_label = json.load(f)   # already id → label ✅

    # distance calculation
    distances = {
        int(k): np.linalg.norm(v - feat)
        for k, v in centroids.items()
    }

    pred_id = min(distances, key=distances.get)

    print("🔍 Prediction:", id_to_label[str(pred_id)])
    print("📏 Distance:", round(distances[pred_id], 4))

    if os.path.exists(TMP_WAV):
        os.remove(TMP_WAV)


if __name__ == "__main__":
    main()
