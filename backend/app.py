from flask import Flask, request, jsonify, render_template
import requests
import base64

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
    # image can come as base64 OR file
    if request.is_json:
        image_base64 = request.json.get("image")
        payload = {"image": image_base64}
        r = requests.post(REMOTE_AI_URL, json=payload)
    else:
        file = request.files.get("file")
        r = requests.post(
            REMOTE_AI_URL,
            files={"file": (file.filename, file.stream, file.mimetype)}
        )

    return jsonify(r.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
