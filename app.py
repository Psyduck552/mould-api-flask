from flask import Flask, request, jsonify
from gradio_client import Client
import base64
import tempfile

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

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(decoded)
            temp.flush()

            result = client.predict(
                {"path": temp.name},  # ✅ Pass as dictionary
                api_name="/predict"
            )

        if isinstance(result, dict):
            return jsonify(result)
        else:
            return jsonify({"result": str(result)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
