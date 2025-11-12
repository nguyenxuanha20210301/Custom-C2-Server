"""
Agent Stub (SAFE)
- Chỉ: register -> heartbeat loop -> optional benign upload demo
- KHÔNG có remote code execution, KHÔNG payloads.

THAM SỐ (env hoặc sửa trực tiếp):
- SERVER_URL: URL API server, vd: https://localhost:8000
- AGENT_PLATFORM: linux/windows/macos/other
- POLL_SEC: khoảng cách heartbeat (sẽ override bởi server nếu trả poll_interval)
- CERT_FILE/KEY_FILE: (optional) nếu bạn dùng mTLS trong lab
"""

import os
import time
import json
import uuid
import requests

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")
AGENT_PLATFORM = os.getenv("AGENT_PLATFORM", "linux")
POLL_SEC = int(os.getenv("POLL_SEC", "10"))

# mTLS (optional)
CERT_FILE = os.getenv("CERT_FILE", "")  # path tới client cert (nếu dùng)
KEY_FILE = os.getenv("KEY_FILE", "")    # path tới client key (nếu dùng)
VERIFY = os.getenv("VERIFY_TLS", "false").lower() == "true"  # dùng cert CA nếu bật

def mtls_kwargs():
    # Nếu dùng mTLS: return {'cert': (CERT_FILE, KEY_FILE), 'verify': '/path/to/ca.pem'}
    if CERT_FILE and KEY_FILE:
        return {"cert": (CERT_FILE, KEY_FILE), "verify": VERIFY}
    return {"verify": VERIFY}

def register():
    payload = {
        "hostname": os.uname().nodename if hasattr(os, "uname") else "agent-host",
        "platform": AGENT_PLATFORM,
        "tags": ["lab-safe"],
    }
    r = requests.post(f"{SERVER_URL}/api/v1/agents/register", json=payload, **mtls_kwargs())
    r.raise_for_status()
    data = r.json()
    return data["agent_id"], int(data.get("poll_interval", POLL_SEC))

def heartbeat(agent_id: str):
    payload = {"uptime": int(time.time()), "load": 0.0}
    r = requests.post(f"{SERVER_URL}/api/v1/agents/{agent_id}/heartbeat", json=payload, **mtls_kwargs())
    r.raise_for_status()

def benign_upload(agent_id: str, content: str = "hello-from-agent-stub"):
    files = {"file": ("report.txt", content.encode("utf-8"), "text/plain")}
    r = requests.put(f"{SERVER_URL}/api/v1/agents/{agent_id}/upload", files=files, **mtls_kwargs())
    if r.status_code == 200:
        print("Uploaded:", r.json())
    else:
        print("Upload failed:", r.status_code, r.text)

def main():
    print("[*] Registering...")
    agent_id, poll = register()
    print("[*] Registered:", agent_id, "poll:", poll)

    # Demo upload benign file 1 lần
    try:
        benign_upload(agent_id)
    except Exception as e:
        print("Upload error (ignored in demo):", e)

    # Heartbeat loop
    while True:
        try:
            heartbeat(agent_id)
            print("[*] Heartbeat OK")
        except Exception as e:
            print("Heartbeat error:", e)
        time.sleep(poll)

# === PLACEHOLDER ===
# AGENT_TASK_HANDLER_PLACEHOLDER:
# Tại đây (hoặc file khác do bạn tạo) bạn có thể thêm logic agent trong lab OFFLINE của riêng bạn.
# KHÔNG thực thi lệnh từ server trong repo này. KHÔNG commit payloads/mã nguy hiểm.
# ===================

if __name__ == "__main__":
    main()
