# Custom C2 Simulator (Academic)

**Mục tiêu:** Xây dựng một hệ thống mô phỏng "Command & Control" phục vụ mục đích học thuật, tập trung vào:
- Kiến trúc hệ thống, code sạch, deployment (Docker/K8s), CI/CD, authentication mạnh, hardening, logging/monitoring.
- **KHÔNG** cung cấp payloads, reverse shells, hoặc mã dùng để tấn công. Agent-stub có chỗ trống để bạn tự thêm logic trong lab riêng.

## Bắt đầu nhanh
1. Clone repository:
```bash
git clone git@github.com:you/custom-c2-simulator.git
cd custom-c2-simulator
```
2. Install pre-commit and run: 
```bash
pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
```
3. Xem docs/project_plan.md de biet roadmap cac giai doan

Cau truc chinh:
server/: backend skeleton
agent-sub/: client stub (safe)
infra/: manifests (docker-compose, k8s sketeton)
.github/: CI, templates
docs/: tai lieu du an 