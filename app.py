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

        # Save image as temp file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp:
            temp.write(decoded)
            temp.flush()
            temp_path = temp.name

        # Reopen the file and pass it directly
        with open(temp_path, "rb") as f:
            result = client.predict(f, api_name="/predict")

        os.remove(temp_path)

        # Ensure the result is JSON-safe
        if isinstance(result, dict):
            safe_result = {
                k: (float(v) if isinstance(v, (int, float)) else v)
                for k, v in result.items()
            }
        else:
            safe_result = {"result": str(result)}

        return jsonify(safe_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
