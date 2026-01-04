from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    # Replace with real output from monitor_detect
    confidence = round(random.uniform(0.45, 0.95), 3)
    label = "normal"

    if confidence >= 0.75:
        severity = "NORMAL"
    elif confidence >= 0.6:
        severity = "WARNING"
    else:
        severity = "CRITICAL"

    return jsonify({
        "label": label,
        "confidence": confidence,
        "severity": severity
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
