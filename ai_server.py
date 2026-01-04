from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    # Simulate AI processing delay (cloud-safe)
    time.sleep(0.15)

    response = {
        "bbox": [0.28, 0.22, 0.44, 0.46],
        "issue": "Loose connection detected",
        "confidence": round(random.uniform(0.75, 0.95), 2),
        "actions": [
            "Turn OFF power",
            "Tighten mounting screws",
            "Reconnect cable",
            "Test again"
        ]
    }

    return jsonify(response)

@app.route("/", methods=["GET"])
def health():
    return "AI SERVER OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
