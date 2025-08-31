# TradingView → Telegram Bot (Render + GitHub Actions)

**This repository is prepared to deploy a Flask webhook on Render and keep it alive only during Taiwan Futures (TXF) trading hours.**

## Your Render URL (set by you):
https://telegram-tradingview-bot-4q8d.onrender.com

### Webhook endpoint
`https://telegram-tradingview-bot-4q8d.onrender.com/webhook`

## Environment variables (set in Render dashboard)
- `TELEGRAM_TOKEN` = your Telegram Bot token (keep secret)
- `CHAT_ID` = your Telegram chat id (keep secret)

## GitHub Actions / Secrets
- `PING_URL` = https://telegram-tradingview-bot-4q8d.onrender.com
- (Optional, for strict pause/resume) `RENDER_API_KEY`, `RENDER_SERVICE_ID`

## Trading hours handled by workflows (Taipei time, UTC+8)
- Day: Mon–Fri 08:45–13:45
- Night: Mon–Thu 15:00–05:00 (next day)
- Friday night: 15:00–00:00 (no carry past midnight)

Workflows:
- `.github/workflows/keepalive.yml` → pings `PING_URL` every 5 minutes **only** during above trading hours to keep Render awake.
- `.github/workflows/render-control.yml` → (optional) every 5 minutes calls Render GraphQL API to `resumeService` during trading hours and `suspendService` outside trading hours.

## Local test
```
pip install -r requirements.txt
python app/app.py
curl -X POST http://localhost:5000/webhook -H "Content-Type: application/json" -d '{"symbol":"TXF","price":17560,"message":"test"}'
```
