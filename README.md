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

## 🚀 3. Cách chạy nhanh

### 3.1. Development (SQLite + uvicorn)

```bash
cd server
uvicorn app.main:app --reload
```

### 3.2. Run database migration

```bash
alembic upgrade head
```

### 3.3. Run test

```bash
pytest -q
```

### 3.4. Docker Compose (prod-like)

```bash
docker compose up --build
```

---

## 📁 4. Cấu trúc thư mục

```
server/
 ├── src/
 │    ├── app/
 │    │    ├── routes/
 │    │    ├── db_models.py
 │    │    ├── models.py
 │    │    ├── settings.py
 │    │    ├── logging_config.py
 │    │    ├── auth.py
 │    │    └── main.py
 │    └── ...
 ├── tests/
 ├── alembic/
 ├── requirements.txt
docs/
 ├── architecture.md
 ├── api_endpoints.md
 ├── ETHICS.md
 ├── SECURITY.md
 └── tech-stack.md
README.md
```

---

## 🔐 5. Security model (tóm tắt)

- RBAC 3 nhóm quyền: **admin, operator, auditor**
- JWT access/refresh token
- Password được hash bằng **passlib/argon2**
- CORS mở trong dev, khóa trong prod
- Storage file kiểm tra content-type
- Không cho phép chạy code, exec command, reverse shell, RCE
- Audit log tất cả sự kiện quan trọng

---

## 📡 6. API chính

- `POST /api/v1/agents/register`
- `GET  /api/v1/agents/{id}/tasks`
- `POST /api/v1/tasks`
- `GET  /api/v1/tasks`
- `POST /api/v1/auth/login`
- `PUT  /api/v1/agents/{id}/upload`
- `GET  /metrics`

Tài liệu chi tiết → `docs/api_endpoints.md`

---

## 🧭 7. Giải thích tính mô phỏng

| Khái niệm gốc     | Mô phỏng trong SCSF                      |
|-------------------|------------------------------------------|
| reverse shell     | “task” agent → báo cáo kết quả text/json |
| command execution | agent gửi kết quả như log/state          |
| persistence       | agent gửi heartbeat + lưu state DB       |
| staging           | upload file qua API upload               |
| payload delivery  | task có payload dạng JSON                |

---

## 📘 8. Tài liệu đi kèm

Xem thư mục `docs/`:
- architecture.md  
- api_endpoints.md  
- SECURITY.md  
- ETHICS.md  
  
---

## 📄 10. Giấy phép

MIT License.

