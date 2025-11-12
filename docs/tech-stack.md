# Tech Stack Decision Record

Mục đích: ghi lại lựa chọn công nghệ và trade-offs.

## Backend
- **FastAPI (Python)** — Lý do:
  - Fast development, async support, auto-generated OpenAPI.
  - Rich ecosystem (pydantic, alembic).
- **Trade-offs**: Python có GIL (less ideal cho CPU-bound). Nếu muốn tối đa hiệu năng chọn Go.

## Database
- **PostgreSQL**
  - ACID, rộng rãi, hỗ trợ JSONB (nếu cần lưu metadata).
- **Trade-offs**: nhẹ cho dev, dễ migrate.

## Object Storage
- **MinIO (dev)**; **S3 (prod)**
  - S3-compatible, dễ mock local.

## Queue / Background
- **Redis + RQ / Celery** (pick one)
  - Dùng khi cần tasks processing (e.g., sanitize uploaded file).
- **Trade-offs**: Celery mạnh mẽ nhưng phức tạp hơn; RQ nhẹ, dễ dùng.

## Auth
- **JWT (access/refresh) + optional mTLS for agents**
  - JWT cho operator sessions; mTLS cho agent-server channel nếu cần strong mutual auth.
- **Trade-offs**: JWT simple; mTLS phức tạp nhưng an toàn hơn cho machine identity.

## UI
- **React + Vite** hoặc **Vue**
  - Minimal dashboard. Can be containerized.

## Observability
- **Prometheus + Grafana** for metrics.
- **Loki / ELK** for logs (Loki lighter).

## CI/CD
- **GitHub Actions**
  - Build/test/lint/image-scan/deploy steps.
- **Image scanning**: Trivy

## Container & Orchestration
- **Docker (local)**, **Kubernetes (k3s/minikube)** for staging.
- **Hardening**: use distroless images or minimal base; non-root user.

## Why these choices (short)
- Balance dev speed + production practices.
- Tools chosen have good docs and are easy to run locally for student projects.

## Notes / Placeholders
- If you prefer Go for backend, swap FastAPI -> Go + Gin/Fiber.
- If you will deploy to cloud, replace MinIO with S3 and Postgres with RDS.