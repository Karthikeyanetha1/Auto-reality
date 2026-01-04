from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, template_folder="templates", static_folder="static")

REMOTE_AI_URL = "http://127.0.0.1:8000/analyze"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ar")
def ar():
    return render_template("ar.html")

@app.route("/detect", methods=["POST"])
def detect():
    if request.is_json:
        r = requests.post(REMOTE_AI_URL, json=request.json)
        return jsonify(r.json())
    return jsonify({"error": "Invalid request"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
