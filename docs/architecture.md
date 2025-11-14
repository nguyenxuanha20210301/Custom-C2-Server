# Architecture – SCSF

Kiến trúc tổng thể của Safe C2 Simulation Framework.

## 1. Thành phần chính
- FastAPI backend
- PostgreSQL/SQLite
- SQLAlchemy ORM
- JWT Auth + RBAC
- Task queue
- File storage local/minio

## 2. Luồng hoạt động
Agent:
    register → heartbeat → get_tasks → upload → complete

Operator:
    login → create task → xem task → audit

## 3. Lý do mô phỏng
- Không chạy shell
- Không chạy command
- Không tạo reverse shell
- Chỉ mô phỏng payload JSON + task queue
