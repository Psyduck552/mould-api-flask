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
        print("🔍 Received request:", data)  # 👈 log request body
        if not data or "base64" not in data:
            print("❌ Missing base64 image")  # 👈 log error
            return jsonify({"error": "Missing base64 image"}), 400

        base64_str = data["base64"].split(",")[-1]
        decoded = base64.b64decode(base64_str)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(decoded)
            temp.flush()
            print("📤 Sending image to Hugging Face...")  # 👈 log before API call

            result = client.predict(
                temp.name,
                api_name="/predict"
            )

        print("✅ Prediction result:", result)  # 👈 log prediction
        return jsonify(result)

    except Exception as e:
        print("🔥 Exception occurred:", str(e))  # 👈 log exception
        return jsonify({"error": str(e)}), 500
