
from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TG_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage" if TELEGRAM_TOKEN else None

@app.get("/")
def health():
    return "OK: trading bot online"

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True, silent=True) or {}
    symbol = data.get("symbol", "N/A")
    price = data.get("price", "N/A")
    msg = data.get("message", "TradingView alert")
    text = f"📢 Alert\nSymbol: {symbol}\nPrice: {price}\nMessage: {msg}"
    if TG_API and CHAT_ID:
        try:
            requests.post(TG_API, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        except Exception as e:
            return jsonify({"status":"error","detail":str(e)}), 500
    return jsonify({"status":"ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
