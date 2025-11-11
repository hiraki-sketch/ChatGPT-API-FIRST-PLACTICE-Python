import os, sys
from dotenv import load_dotenv
from openai import OpenAI

# .env から API キーを読み込む
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("[ERROR] OPENAI_API_KEY が設定されていません。.env に追加してください。")
    sys.exit(1)

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = (
    "あなたは親切で丁寧なAIアシスタントです。"
    "質問には日本語で、初心者にも分かりやすく答えてください。"
)

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def chat_once(user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
    )
    reply = res.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply

def main():
    print("🧠 ChatGPT Q&A アプリへようこそ！（終了は :q または exit）")
    while True:
        q = input("\nあなた> ").strip()
        if q in {":q", "exit"}:
            print("終了します。")
            break
        if not q:
            continue
        print("\n--- 回答 ---\n" + chat_once(q))

if __name__ == "__main__":
    main()
