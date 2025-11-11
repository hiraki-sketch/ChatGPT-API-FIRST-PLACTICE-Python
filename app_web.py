import os
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, jsonify, render_template

# 環境変数（.env）読み込み
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

app = Flask(__name__)

SYSTEM = ("あなたは丁寧な日本語で回答します。"
          "専門用語はやさしく説明し、手順は番号付きで簡潔に示してください。")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_text = (data or {}).get("message", "").strip()
    if not user_text:
        return jsonify({"error": "message is empty"}), 400

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_text},
    ]
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
    )
    answer = resp.choices[0].message.content
    return jsonify({"reply": answer})

if __name__ == "__main__":
    # http://localhost:8000 で開けます
    app.run(host="127.0.0.1", port=8000, debug=True)
