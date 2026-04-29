from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import base64
import os

app = Flask(__name__)
CORS(app)

# Put your OpenAI API key here
client = OpenAI(api_key="sk-xxxx")


def encode_image(image_file):
    """Convert uploaded image into base64 string."""
    return base64.b64encode(image_file.read()).decode("utf-8")


@app.route("/", methods=["GET"])
def home():
    return "Conceptly AI backend running 🚀"


@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    image_file = request.files.get("image")

    if not question and not image_file:
        return jsonify({"error": "Please provide a question or image"}), 400

    content = []

    # Add text question
    if question:
        content.append({
            "type": "text",
            "text": question
        })

    # Add image if exists
    if image_file:
        base64_image = encode_image(image_file)

        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert AI tutor. "
                        "Identify the topic first, explain step-by-step, "
                        "show formulas used, provide shortcuts if possible, "
                        "and clearly highlight the final answer."
                    )
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=600
        )

        answer = response.choices[0].message.content

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)