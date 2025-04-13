from flask import Flask, request, jsonify
from gradio_client import Client
import base64
import io

app = Flask(__name__)

# Connect to your Hugging Face Space
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

        # Extract the base64 string from the JSON
        base64_str = data["base64"].split(",")[-1]
        decoded_image = base64.b64decode(base64_str)

        # Convert to file-like object for Gradio
        image_file = io.BytesIO(decoded_image)

        # Send to Hugging Face Space
        result = client.predict(
            image_file,
            api_name="/predict"
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
