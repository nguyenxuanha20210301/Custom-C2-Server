# Yêu cầu dự án — Custom C2 Simulator (Phase 1)

## 1. Mục tiêu tổng quát
Xây dựng hệ thống mô phỏng Command & Control (C2) cho mục đích học thuật, tập trung vào:
- API server quản lý "agents" (register, heartbeat, tasks, upload/download mẫu).
- Agent-stub an toàn: chỉ heartbeat / upload mẫu; **không** thực thi lệnh.
- Triển khai production-like (Docker/K8s), authentication mạnh, logging, monitoring.
- Để chỗ trống (placeholder) cho phần agent logic mà người dùng (bạn) sẽ tự thêm offline.

## 2. Yêu cầu chức năng (Functional Requirements)
FR-01 — Agent registration
- Agent có thể POST metadata để đăng ký.
- Server tạo `agent_id` duy nhất và trả về thông tin cấu hình (ví dụ polling interval).

FR-02 — Heartbeat
- Agent định kỳ gửi heartbeat với trạng thái cơ bản (uptime, load, tags).
- Server lưu lịch sử heartbeat tối thiểu `N` bản (configurable).

FR-03 — Tasks (benign)
- Admin có thể tạo tasks dạng **non-executable** (ví dụ: "collect-metrics", "download-config", "upload-report").
- Agent có thể lấy danh sách tasks assigned (read-only contract).
  > **Lưu ý:** Tasks không được chứa lệnh thực thi; chỉ là mô tả / pointer tới file.

FR-04 — File storage
- Server cho phép upload/download files (chỉ whitelist mime types: `.txt`, `.json`, `.cfg`, `.pdf` ...).
- Files lưu trên S3-compatible storage (MinIO cho dev).

FR-05 — Authentication & Authorization
- Người dùng (admin/operator) phải login.
- RBAC: role = {admin, operator, auditor}.
- Agents authenticate (mTLS or asymmetric token). Option: JWT + mTLS.

FR-06 — Audit & Logging
- Mỗi action quan trọng (auth, register, task create, file access) ghi audit log có tamper-evidence metadata (timestamp, actor_id, action).

FR-07 — Dashboard minimal
- Web UI hoặc API endpoints để liệt kê agents, tasks, files, và các logs (phân quyền).

## 3. Yêu cầu phi chức năng (Non-functional)
NFR-01 — Bảo mật
- TLS mandatory (HTTPS).
- Không lưu secrets trong repo. Dùng Vault hoặc env vars (GitHub Secrets).
- Rate-limiting endpoints để giảm abuse.

NFR-02 — Hiệu năng
- Hỗ trợ mô phỏng tối thiểu 1000 agents nhẹ (heartbeat every 60s) trên staging infra nhỏ.
- Tối ưu DB queries cho các bảng agents/heartbeats.

NFR-03 — Sẵn sàng & Bảo trì
- Containerized; có k8s manifests skeleton.
- CI pipeline kiểm tra lint, tests, và image scanning.

NFR-04 — Testability
- Unit tests cho business logic; integration tests cho API contracts (mock DB/storage).

## 4. Acceptance criteria (kết quả chấp nhận)
- Có API endpoint register + heartbeat + get-tasks + upload/download hoạt động trên local docker-compose.
- Có agent-stub chạy được, gửi register + heartbeat và nhận response (không thực thi lệnh).
- CI pipeline chạy lint + unit tests.
- TLS được bật trên ingress (self-signed ok cho dev).
- Security checklist (docs/SECURITY.md) hoàn chỉnh.

## 5. Các tham số cấu hình (placeholders)
- `DATABASE_URL` = postgresql://<user>:<pass>@<host>:<port>/<db>
- `MINIO_ENDPOINT` = <host:port>
- `JWT_SECRET` = <<THAY_THEO_BAN; ít nhất 32 ký tự>>
- `AGENT_DEFAULT_POLL_SEC` = 60
- `HEARTBEAT_RETENTION_DAYS` = 30

> **Ghi chú:** Các giá trị trên để trong `.env` (local dev) hoặc secret manager (production). Không commit `.env`.
