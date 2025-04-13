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

        # Write to temp file
        temp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        temp.write(decoded)
        temp.close()

        # Wrap in dict as required
        result = client.predict(
            {"path": temp.name},  # ✅ Correct format for Gradio
            api_name="/predict"
        )

        # Clean up the file
        os.remove(temp.name)

        return jsonify(result if isinstance(result, dict) else {"result": str(result)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
