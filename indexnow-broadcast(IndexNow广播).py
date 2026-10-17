#!/usr/bin/env python3
"""One-shot IndexNow submission; no timer, retries or persistent queue."""
import json
import subprocess
from datetime import datetime, timezone

KEY = "e9a7c3b2f1048a90d8e27c1b5049a3ef"
HOSTS = ("proxy.mybskm.top", "gpu.mybskm.top", "pay.mybskm.top")


def main():
    # Verify all public keys before sending any notifications.
    for host in HOSTS:
        response = subprocess.run(
            ["curl", "-fsS", "--max-time", "20", f"https://{host}/{KEY}.txt"],
            capture_output=True, text=True, check=True,
        )
        if response.stdout.strip() != KEY:
            raise ValueError(f"Public key mismatch: {host}")
    failed = False
    for host in HOSTS:
        payload = {"host": host, "key": KEY,
                   "keyLocation": f"https://{host}/{KEY}.txt",
                   "urlList": [f"https://{host}/"]}
        response = subprocess.run(
            ["curl", "-sS", "--max-time", "30", "-X", "POST",
             "-H", "Content-Type: application/json; charset=utf-8",
             "--data-binary", "@-", "-w", "\n%{http_code}",
             "https://api.indexnow.org/indexnow"],
            input=json.dumps(payload), capture_output=True, text=True,
        )
        body, _, status = response.stdout.rpartition("\n")
        ok = response.returncode == 0 and status in ("200", "202")
        failed |= not ok
        print(json.dumps({"time": datetime.now(timezone.utc).isoformat(),
                          "host": host, "http_status": status, "accepted": ok,
                          "response": body, "error": response.stderr}, ensure_ascii=False))
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
