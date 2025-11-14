param(
    # API base URL cua server trong Docker
    [string]$ApiBaseUrl = "http://localhost:8000/api/v1"
)

Write-Host "=== [Step 0] Move to repo root (neu chua) ===" -ForegroundColor Cyan
# Gia su ban da chay script nay tu repo root: Custom-C2-Server

Write-Host "=== [Step 1] Tao venv + cai dependencies ===" -ForegroundColor Cyan
if (!(Test-Path ".\.venv")) {
    python -m venv .venv
}
. .\.venv\Scripts\Activate.ps1

pip install -r .\server\requirements.txt

Write-Host '=== [Step 2] Chay pytest (Phase 6-7) voi SQLite test DB ===' -ForegroundColor Cyan
# Dam bao khong bi .env PostgreSQL pha DB_URL
$env:DATABASE_URL = "sqlite:///test.db"
$env:AUTH_DISABLED = "true"  # Cho test & demo nhe nhang

pytest -q

Write-Host "=== [Step 3] Bat Docker stack (db + minio + server) ===" -ForegroundColor Cyan
# Dung Docker Compose da setup tu cac phase truoc
docker compose -f .\infra\docker-compose.yml down -v
docker compose -f .\infra\docker-compose.yml up -d --build

Write-Host "Doi server khoi dong..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "=== [Step 4] Kiem tra health check /api/v1/health ===" -ForegroundColor Cyan
try {
    $healthUrl = ($ApiBaseUrl.TrimEnd('/api/v1')) + "/api/v1/health"
    Write-Host "Health URL: $healthUrl"
    $resp = Invoke-WebRequest $healthUrl -UseBasicParsing
    Write-Host "Health status code:" $resp.StatusCode
    Write-Host "Health body:" $resp.Content
}
catch {
    Write-Host "[!] Health check loi, kiem tra container infra-server-1" -ForegroundColor Red
    Write-Host "    docker logs -f infra-server-1"
    exit 1
}

Write-Host "=== [Step 5] Mo cua so PowerShell moi chay agent_sim.py ===" -ForegroundColor Cyan
# Cua so moi: kich hoat venv + chay agent_sim
$cmd = "cd `"$PWD`"; . .\.venv\Scripts\Activate.ps1; python tools/agent_sim.py --base-url $ApiBaseUrl"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $cmd

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Green
Write-Host "  BAY GIO: nhin sang cua so agent_sim.py, no se in dang:" -ForegroundColor Green
Write-Host "      [+] Registered agent_id=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX" -ForegroundColor Green
Write-Host "  Copy AGENT_ID do, roi dung cac lenh test Phase 9-10 ben duoi." -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Goi y: sau khi co AGENT_ID, mo 1 cua so PowerShell khac va chay:" -ForegroundColor Yellow

Write-Host '  # Vi du tao task sim.exec' -ForegroundColor Yellow
Write-Host '  curl -X POST http://localhost:8000/api/v1/tasks ^' -ForegroundColor Yellow
Write-Host '    -H "Content-Type: application/json" ^' -ForegroundColor Yellow
Write-Host '    -d "{`"agent_ids`":[`"AGENT_ID_BENIGN`"],`"type`":`"sim.exec`",`"meta`":{`"spec`":{`"name`":`"whoami`"}}}"' -ForegroundColor Yellow

Write-Host ""
Write-Host "Hoac xem chi tiet cac lenh Phase 9-10 trong README / FULL_PHASE_EXPLAIN_FOR_ME.md" -ForegroundColor Yellow
