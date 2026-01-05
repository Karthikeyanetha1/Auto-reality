from flask import Flask, render_template, request, jsonify

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/")
def home():
    return render_template("ar.html")

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()

    # Fake AI response (UI / UX verification)
    return jsonify({
        "bbox": [0.25, 0.25, 0.5, 0.5],
        "issue": "Loose connection detected",
        "confidence": 0.91
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
