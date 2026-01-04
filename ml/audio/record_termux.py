import subprocess
import os
import signal
import time

OUT = "__live_input.wav"

def ignore_ctrl_c(signum, frame):
    print("⛔ CTRL+C disabled during recording")

signal.signal(signal.SIGINT, ignore_ctrl_c)

def record(seconds=5):
    if os.path.exists(OUT):
        os.remove(OUT)

    print(f"🎙 Recording {seconds} seconds (mobile mic)...")
    print("⏳ Please wait... DO NOT press CTRL+C")

    subprocess.run([
        "termux-microphone-record",
        "-f", OUT,
        "-l", str(seconds)
    ])

    time.sleep(1)

    if os.path.exists(OUT):
        print("✅ Recording saved:", OUT)
    else:
        print("❌ Recording failed — mic permission or device issue")

if __name__ == "__main__":
    record()
