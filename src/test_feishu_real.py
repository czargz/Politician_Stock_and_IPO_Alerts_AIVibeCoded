"""One-shot real delivery test for the Feishu alerter (no credentials needed
beyond the webhook already configured via .env / env). Sends a single test
message so we can confirm the link is live end-to-end."""
import os
from dotenv import load_dotenv
from feishu_alerts import FeishuAlerter

load_dotenv()

test_alerts = [
    "🔧 飞书推送链路测试",
    "来源: Politician_Stock_and_IPO_Alerts (Feishu adapter)",
    "时间: 2026-10-10 (CDT)",
    "说明: 若你在飞书群收到本条，说明 daily_check 告警已可送达。",
]

a = FeishuAlerter()
ok = a.send_alert("🚀 Feishu Link Test", test_alerts)
print("DELIVERED_OK" if ok else "DELIVERY_FAILED")
