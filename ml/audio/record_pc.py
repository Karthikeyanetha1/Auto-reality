import sounddevice as sd
import soundfile as sf

SR = 16000
DURATION = 5
OUT_WAV = "__live_input.wav"

print("🎙 Recording from laptop mic...")
audio = sd.rec(int(DURATION * SR), samplerate=SR, channels=1)
sd.wait()
sf.write(OUT_WAV, audio, SR)
print("✅ Saved:", OUT_WAV)
