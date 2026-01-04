import os
import time
import csv
import subprocess
from datetime import datetime

from audio_engine import predict_audio

# ================= CONFIG =================
RECORD_SECONDS = 3
AUTO_INTERVAL_SECONDS = 10        # ⏱ Auto-monitor every N seconds
TEMP_WAV = "__live_input.wav"
LOG_FILE = "monitor_logs.csv"

ENABLE_SOUND_ALERT = True         # 🔊 ENABLED
# =========================================


def ensure_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "prediction",
                "confidence",
                "distance",
                "severity",
                "audio_file"
            ])


def wait_until_file_stable(path, timeout=10):
    last_size = -1
    start = time.time()

    while time.time() - start < timeout:
        if os.path.exists(path):
            size = os.path.getsize(path)
            if size > 0 and size == last_size:
                return True
            last_size = size
        time.sleep(0.5)

    return False


def record_mobile():
    if os.path.exists(TEMP_WAV):
        os.remove(TEMP_WAV)

    print(f"\n🎙 Recording {RECORD_SECONDS} seconds...")

    subprocess.run([
        "termux-microphone-record",
        "-f", TEMP_WAV,
        "-l", str(RECORD_SECONDS)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("⏳ Waiting for recording to finalize...")

    if not wait_until_file_stable(TEMP_WAV):
        raise RuntimeError("Recording not finalized")


def play_alert():
    if not ENABLE_SOUND_ALERT:
        return
    try:
        subprocess.run(
            ["termux-vibrate", "-d", "400"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass


def classify_severity(label, confidence):
    if label == "normal":
        return "NORMAL"

    if confidence < 0.6:
        return "IGNORE"
    if confidence < 0.75:
        return "WARNING"
    return "CRITICAL"


def log_result(result, severity):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            result["label"],
            round(result["confidence"], 3),
            round(result["distance"], 3),
            severity,
            TEMP_WAV
        ])


def handle_alert(result, severity):
    label = result["label"]
    confidence = result["confidence"]

    if severity == "IGNORE":
        print("ℹ️ Noise ignored")
        return

    if severity == "WARNING":
        print(f"⚠️ WARNING: {label} | Confidence {confidence:.3f}")
        return

    if severity == "CRITICAL":
        print("🚨🚨 CRITICAL FAULT DETECTED 🚨🚨")
        print(f"⚠️ Issue      : {label}")
        print(f"📊 Confidence : {confidence:.3f}")
        play_alert()
        return

    print("✅ Fan healthy")


def monitor():
    ensure_log_file()
    print("🟢 Auto Fan Monitoring Started")
    print(f"⏱ Interval: every {AUTO_INTERVAL_SECONDS} seconds")
    print("🛑 Press CTRL+C to stop\n")

    while True:
        try:
            record_mobile()
            result = predict_audio(TEMP_WAV)

            severity = classify_severity(
                result["label"],
                result["confidence"]
            )

            print(
                f"🔍 {result['label']} | "
                f"Confidence: {result['confidence']:.3f} | "
                f"Severity: {severity}"
            )

            log_result(result, severity)
            handle_alert(result, severity)

            time.sleep(AUTO_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(3)


if __name__ == "__main__":
    monitor()
