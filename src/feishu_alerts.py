import os
import time
import hashlib
import base64
import hmac
import requests
from typing import List


class FeishuAlerter:
    """Send daily stock & IPO alerts to a Feishu/Lark custom bot webhook.

    Environment variables:
      FEISHU_WEBHOOK  required - the bot URL
                     https://open.feishu.cn/open-apis/bot/v2/hook/<token>
      FEISHU_SECRET   optional - signing secret for the bot (recommended)

    If FEISHU_WEBHOOK is not set, send_alert() degrades to a dry-run that
    simply prints the alerts, so the pipeline can be verified without any
    credentials. This mirrors the original email fallback behaviour.
    """

    def __init__(self, webhook: str = None, secret: str = None):
        self.webhook = webhook or os.getenv('FEISHU_WEBHOOK')
        self.secret = secret or os.getenv('FEISHU_SECRET')
        self.timeout = int(os.getenv('FEISHU_TIMEOUT', '10'))

    def _signature(self) -> dict:
        """Compute Feishu signed-bot timestamp+sign when a secret is configured."""
        if not self.secret:
            return {}
        timestamp = str(int(time.time()))
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            self.secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256,
        ).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return {'timestamp': timestamp, 'sign': sign}

    def send_alert(self, subject: str, alerts: List[str]) -> bool:
        """Send a list of formatted alert strings to Feishu as one text message.

        Returns True when delivered (or when dry-run printed), False on error.
        """
        if not self.webhook:
            print("[Feishu] FEISHU_WEBHOOK not set - DRY RUN, printing alerts:")
            for a in alerts:
                print(f"\n{a}\n")
            return True

        content = subject + "\n" + "=" * 32 + "\n\n" + "\n\n".join(alerts)

        # Feishu text messages are capped at 20KB; truncate safely with a marker.
        if len(content.encode('utf-8')) > 18000:
            content = content[:18000] + "\n...(truncated)"

        payload = {
            "msg_type": "text",
            "content": {"text": content},
        }
        payload.update(self._signature())

        try:
            resp = requests.post(self.webhook, json=payload, timeout=self.timeout)
            data = resp.json() if resp.content else {}
            if data.get('code') == 0:
                print(f"[Feishu] Alert sent ({len(alerts)} items)")
                return True
            print(f"[Feishu] Send failed: {data}")
            return False
        except Exception as e:
            print(f"[Feishu] Error sending: {e}")
            return False
