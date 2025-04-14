from flask import Flask, request, jsonify
import base64
import tempfile
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask proxy to Hugging Face is live!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        if not data or "base64" not in data:
            return jsonify({"error": "Missing base64 image"}), 400

        base64_str = data["base64"].split(",")[-1]
        decoded = base64.b64decode(base64_str)

        # Save the image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(decoded)
            temp_file_path = temp_file.name

        # Open the file as binary and send to Hugging Face
        with open(temp_file_path, "rb") as f:
            files = {"image": f}
            response = requests.post(
                "https://psyduck552-isthismould.hf.space/predict",
                files=files
            )

        os.remove(temp_file_path)

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
