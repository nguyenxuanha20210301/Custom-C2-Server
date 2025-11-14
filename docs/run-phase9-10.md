## 1. Nếu bạn chỉ cần demo cho thầy (không bắt buộc Docker)

Thực ra để **demo Phase 9–10** bạn *không cần* Docker, chỉ cần:

### Bước 1 – Chạy server local bằng SQLite

Trong repo root:

```powershell
# 1) Bật venv
. .\.venv\Scripts\Activate.ps1

# 2) Dùng SQLite cho đơn giản (như pytest)
$env:DATABASE_URL = "sqlite:///demo.db"
$env:AUTH_DISABLED = "true"

# 3) Chạy server
cd server
uvicorn src.app.main:app --reload
```

– Server chạy ở: `http://127.0.0.1:8000`
– Health check: `http://127.0.0.1:8000/api/v1/health`

### Bước 2 – Chạy agent_sim

Mở **cửa sổ terminal khác**, bật venv:

```powershell
cd C:\Users\Admin\Desktop\Custom-C2-Server
. .\.venv\Scripts\Activate.ps1

#root repo
cd tools
ni __init__.py -ItemType File
cd ..

python tools\agent_sim.py --base-url http://127.0.0.1:8000/api/v1
```

Bạn sẽ thấy:

```text
[+] Registered agent_id=...
[+] Starting poll loop for agent ...
[.] No tasks, sleeping...
```

### Bước 3 – Tạo task Phase 9–10

Dùng PowerShell (vẫn ở repo root):

```powershell
# 1) Lấy AGENT_ID từ output agent_sim.py (copy lại)

$AGENT = "<AGENT_ID_COPY_TU_AGENT_SIM>"

# 2) Tạo task sim.exec (command execution / reverse shell mô phỏng)
$bodyExec = @{
  agent_ids = @($AGENT)
  type      = "sim.exec"
  meta      = @{
    spec = @{
      name = "ps"
    }
  }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8000/api/v1/tasks" `
  -ContentType "application/json" `
  -Body $bodyExec

# 3) Tạo task sim.persist (persistence mô phỏng)
$bodyPersist = @{
  agent_ids = @($AGENT)
  type      = "sim.persist"
  meta      = @{
    spec = @{
      mechanism = "systemd_service"
      label     = "demo-agent"
    }
  }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8000/api/v1/tasks" `
  -ContentType "application/json" `
  -Body $bodyPersist

# 4) Tạo task sim.delivery (payload delivery mô phỏng)
$bodyDelivery = @{
  agent_ids = @($AGENT)
  type      = "sim.delivery"
  meta      = @{
    spec = @{
      artifact_name = "benign-tool.zip"
      stage         = "staging"
      size_kb       = 512
    }
  }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8000/api/v1/tasks" `
  -ContentType "application/json" `
  -Body $bodyDelivery
```

👉 Quay lại cửa sổ `agent_sim.py`, bạn sẽ thấy nó nhận từng task, in ra JSON và báo:

```text
[+] Received 3 task(s)
[+] Completed task <id> (sim.exec)
[+] Completed task <id> (sim.persist)
[+] Completed task <id> (sim.delivery)
```

