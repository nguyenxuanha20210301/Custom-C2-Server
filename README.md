# SCSF – Safe C2 Simulation Framework

**SCSF (Safe C2 Simulation Framework)** là một dự án mô phỏng hệ thống  
**Command & Control (C2)**, tập trung vào:

- Thiết kế API C2 cơ bản
- Đăng ký agent, nhận nhiệm vụ, gửi kết quả
- Upload file, task queue, heartbeat
- RBAC (admin/operator/auditor)
- Logging, metrics, CI/CD
- Lưu trữ biểu mẫu (file storage: local/minio)
- Đảm bảo an toàn, tuân thủ đạo đức  
- *Không chứa shellcode, reverse shell, RCE hay bất kỳ mã khai thác nguy hiểm nào.*

---

## 🎯 1. Mục tiêu chính của SCSF

- Tạo framework giúp nghiên cứu C2 trong môi trường *an toàn và mô phỏng*.
- Cung cấp nền tảng để demo:
  - agent đăng ký → nhận task → hoàn thành task
  - agent upload file về server
  - server phân phối task, quản lý trạng thái
  - audit, RBAC, logging đầy đủ
- Không chứa mã độc, chỉ mô phỏng workflow của C2.

---

## 🧱 2. Kiến trúc tổng quan

```
client agent(s)  <───HTTP───>  SCSF API Server
                                   │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
     PostgreSQL                Local/Minio                Prometheus Metrics
```

Thành phần chính:

- **FastAPI backend**
- **SQLAlchemy ORM**
- **Alembic migration**
- **JWT Authentication + RBAC**
- **CI/CD GitHub Actions**
- **Local or Minio file storage**
- **Prometheus metrics**

---

## ✅ 3. Cách chạy nhanh (Quick Start) 

> **✔ Hoạt động thật**
> **✔ Đúng cấu trúc project**
> **✔ Không gây lỗi chạy**
> **✔ Dùng SQLite cho development**
> **✔ Có Docker Compose cho môi trường gần production**

````markdown
## 3. Cách chạy nhanh (Quick Start)

### 3.1. Development mode (SQLite + uvicorn)

Trong môi trường phát triển, server dùng SQLite nên **không cần Docker**, chỉ cần Python.

```powershell
cd C:\Users\Admin\Desktop\Custom-C2-Server
. .\.venv\Scripts\Activate.ps1

# Sử dụng SQLite
$env:DATABASE_URL = "sqlite:///demo.db"
$env:AUTH_DISABLED = "true"

cd server
uvicorn src.app.main:app --reload
````

Server sẽ chạy tại:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 3.2. Chạy database migration (bắt buộc nếu dùng Postgres hoặc Docker)

**Khi chạy development với SQLite thì Alembic sẽ tự tạo schema** nên bạn **không cần** chạy migration.
Migration **chỉ chạy** trong môi trường *production-like* (Docker).

Dùng lệnh:

```bash
cd server
alembic upgrade head
```

> ⚠ Lưu ý: migration này chạy dựa trên `DATABASE_URL`.
> Nếu bạn dùng SQLite, migration KHÔNG lỗi nhưng đơn giản không cần thiết.

---

### 3.3. Chạy unit test (Phase 6–7)

Dùng SQLite test DB tự động:

```powershell
cd C:\Users\Admin\Desktop\Custom-C2-Server
. .\.venv\Scripts\Activate.ps1

pytest -q
```

Kỳ vọng:

```
3 passed in X.XXs
```

---

### 3.4. Production-like mode (Docker Compose)

Chạy toàn bộ stack:

* PostgreSQL
* MinIO
* Custom C2 Server (uvicorn)
* Tự apply Alembic migrations

```bash
cd C:\Users\Admin\Desktop\Custom-C2-Server\infra
docker compose up --build
```

Kiểm tra health:

[http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

Shutdown:

```bash
docker compose down
```

---

## 🔐 4. Security model

- RBAC 3 nhóm quyền: **admin, operator, auditor**
- JWT access/refresh token
- Password được hash bằng **passlib/argon2**
- CORS mở trong dev, khóa trong prod
- Storage file kiểm tra content-type
- Không cho phép chạy code, exec command, reverse shell, RCE
- Audit log tất cả sự kiện quan trọng

---

## 📡 5. API chính

- `POST /api/v1/agents/register`
- `GET  /api/v1/agents/{id}/tasks`
- `POST /api/v1/tasks`
- `GET  /api/v1/tasks`
- `POST /api/v1/auth/login`
- `PUT  /api/v1/agents/{id}/upload`
- `GET  /metrics`

Tài liệu chi tiết → `docs/api_endpoints.md`

---

## 🧭 6. Giải thích tính mô phỏng

| Khái niệm gốc     | Mô phỏng trong SCSF                      |
|-------------------|------------------------------------------|
| reverse shell     | “task” agent → báo cáo kết quả text/json |
| command execution | agent gửi kết quả như log/state          |
| persistence       | agent gửi heartbeat + lưu state DB       |
| staging           | upload file qua API upload               |
| payload delivery  | task có payload dạng JSON                |

---

## 📘 7. Tài liệu đi kèm

Xem thư mục `docs/`:
- architecture.md  
- api_endpoints.md  
- SECURITY.md  
- ETHICS.md  
  
---

## 📄 9. Giấy phép

MIT License.

