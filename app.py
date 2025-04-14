from flask import Flask, request, jsonify
import base64
import tempfile
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Mould API is live!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        if not data or "base64" not in data:
            return jsonify({"error": "Missing base64 image"}), 400

        # Extract base64 image string
        base64_str = data["base64"].split(",")[-1]
        decoded = base64.b64decode(base64_str)

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(decoded)
            temp_file_path = temp_file.name

        # Send multipart/form-data to HF
        with open(temp_file_path, "rb") as image_file:
            response = requests.post(
                "https://psyduck552-isthismould.hf.space/predict",
                files={"image": ("image.jpg", image_file, "image/jpeg")},
                timeout=60
            )

        os.remove(temp_file_path)

        try:
            return jsonify(response.json())
        except Exception:
            return jsonify({"raw_response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
