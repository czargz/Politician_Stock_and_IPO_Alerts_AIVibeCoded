"""Dry-run verification for the Feishu adapter (no network, no credentials)."""
import sys, os, hmac, hashlib, base64, time, json
sys.path.insert(0, os.path.dirname(__file__))
from feishu_alerts import FeishuAlerter

sample = [
    "Pelosi (CA11)\nBUY 📈 NVDA  ($15,001 - $50,000)\nTraded: 06/10/2026 | Disclosed: 07/02/2026\nSource: House PTR\n---",
    "Sen. John Doe\nSELL 📉 TSLA  ($1,001 - $15,000)\nTraded: 06/12/2026 | Disclosed: 07/01/2026\nSource: Senate PTR\n---",
]

print("== 1) Dry-run (no FEISHU_WEBHOOK) ==")
FeishuAlerter().send_alert("TEST Daily Stock & IPO Alerts", sample)

print("\n== 2) Signed-bot payload construction (dummy webhook, NOT sent) ==")
a = FeishuAlerter(webhook="https://open.feishu.cn/open-apis/bot/v2/hook/dummy", secret="testsecret")
payload = {"msg_type": "text", "content": {"text": "x"}}
payload.update(a._signature())
print("signature keys:", list(payload.keys()), "timestamp len:", len(payload.get("timestamp", "")))

print("\nOK: adapter imports, dry-run prints, signature helper works.")
