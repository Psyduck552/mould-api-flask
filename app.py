from flask import Flask, request, jsonify
from gradio_client import Client
import base64
import tempfile
import os

app = Flask(__name__)
client = Client("Psyduck552/IsThisMould")

@app.route("/")
def home():
    return "✅ Mould API is live!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        if not data or "base64" not in data:
            return jsonify({"error": "Missing base64 image"}), 400

        base64_str = data["base64"].split(",")[-1]
        decoded = base64.b64decode(base64_str)

        # Save base64 image to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(decoded)
            temp_file_path = temp_file.name

        # Open file in binary mode and send to Hugging Face
        with open(temp_file_path, "rb") as f:
            result = client.predict(f, api_name="/predict")

        # Clean up
        os.remove(temp_file_path)

        # Ensure the output is clean JSON
        if isinstance(result, dict):
            safe_result = {
                str(k): float(v) if isinstance(v, (int, float)) else str(v)
                for k, v in result.items()
            }
        else:
            safe_result = {"result": str(result)}

        return jsonify(safe_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
