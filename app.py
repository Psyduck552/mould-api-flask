from flask import Flask, request, jsonify
from gradio_client import Client
import base64
import tempfile
import os
import json

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

        # Send to Hugging Face
        result = client.predict({"path": temp_file_path}, api_name="/predict")

        # Clean up temp file
        os.remove(temp_file_path)

        # Ensure result is serialisable
        try:
            return jsonify(json.loads(json.dumps(result)))
        except Exception:
            return jsonify({"result": str(result)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
