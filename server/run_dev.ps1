# server\run_dev.ps1
$ROOT = Resolve-Path "$PSScriptRoot\.."
$VENV = Join-Path $ROOT ".venv\Scripts\Activate.ps1"

# Activate venv (ở repo root)
& $VENV

# Nạp .env (tùy chọn – bạn có thể dùng dotenv trong code, ở đây set thủ công cái cần thiết khi chạy dev)
$env:PYTHONPATH = (Join-Path $PSScriptRoot "src")

# Chạy uvicorn bằng interpreter trong venv
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir (Join-Path $PSScriptRoot "src")
