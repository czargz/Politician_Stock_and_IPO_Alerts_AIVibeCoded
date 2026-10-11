import os
from datetime import datetime
try:
    from dotenv import load_dotenv
    load_dotenv()  # local .env convenience; GitHub Actions supplies vars via secrets
except Exception:
    pass
from politician_trades import PoliticianTradeTracker
from ipo_alerts import IPOTracker
from email_alerts import EmailAlerter
from feishu_alerts import FeishuAlerter

def main():
    print(f"Starting daily stock and IPO check at {datetime.now()}")

    politician_tracker = PoliticianTradeTracker()
    ipo_tracker = IPOTracker()

    politician_trades = politician_tracker.get_recent_trades()
    new_ipos = ipo_tracker.get_upcoming_ipos()

    alerts = []

    if politician_trades:
        print(f"Found {len(politician_trades)} new politician trades")
        for trade in politician_trades:
            alerts.append(politician_tracker.format_trade_alert(trade))

    if new_ipos:
        print(f"Found {len(new_ipos)} new IPOs")
        for ipo in new_ipos:
            alerts.append(ipo_tracker.format_ipo_alert(ipo))

    if alerts:
        feishu_webhook = os.getenv('FEISHU_WEBHOOK')
        recipient = os.getenv('ALERT_EMAIL')
        if feishu_webhook:
            FeishuAlerter().send_alert("🚀 Daily Stock & IPO Alerts", alerts)
        elif recipient:
            alerter = EmailAlerter(recipient)
            alerter.send_alert("🚀 Daily Stock & IPO Alerts", alerts)
        else:
            print("No FEISHU_WEBHOOK/ALERT_EMAIL set. Displaying alerts:")
            for alert in alerts:
                print(f"\n{alert}\n")
    else:
        print("No new alerts today")

if __name__ == "__main__":
    main()
