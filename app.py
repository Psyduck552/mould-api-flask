from flask import Flask, request, jsonify
import base64
import tempfile
import os
import requests

app = Flask(__name__)

# Roboflow API config
ROBOFLOW_API_URL = "https://detect.roboflow.com/mold-data-kjqz3/1"
ROBOFLOW_API_KEY = "s9LOYEL2DpeZHq1V4tn5"

@app.route("/")
def home():
    return "✅ Mould API (Roboflow) is live!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        if not data or "base64" not in data:
            return jsonify({"error": "Missing base64 image"}), 400

        # Decode the base64 string
        base64_str = data["base64"].split(",")[-1]
        decoded = base64.b64decode(base64_str)

        # Save to temporary image file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(decoded)
            temp_file_path = temp_file.name

        # Send to Roboflow
        with open(temp_file_path, "rb") as image_file:
            response = requests.post(
                f"{ROBOFLOW_API_URL}?api_key={ROBOFLOW_API_KEY}",
                files={"file": ("image.jpg", image_file, "image/jpeg")},
                timeout=60
            )

        # Remove temp file
        os.remove(temp_file_path)

        # Return prediction
        try:
            return jsonify(response.json())
        except Exception:
            return jsonify({"raw_response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
