# server/src/app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import ensure_admin_exists
from .db import SessionLocal, engine
from .db_models import Base
from .logging_config import RequestLogMiddleware, configure_logging
from .metrics import MetricsMiddleware, router as metrics_router
from .routes import agents, auth, files, health, tasks
from .settings import settings

# =========================
# SQLite: đảm bảo schema tồn tại cho pytest / dev
# =========================
if settings.database_url.startswith("sqlite"):
    # idempotent: gọi nhiều lần cũng không sao
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Thay cho @app.on_event("startup").

    Khi app start:
      - (SQLite) schema đã được tạo ở trên.
      - Bootstrap admin user.
    """

    # Bootstrapping admin user
    db = SessionLocal()
    try:
        ensure_admin_exists(db)
    finally:
        db.close()

    # nhường control cho app chạy
    yield

    # shutdown hook (hiện chưa cần)
    return


def create_app() -> FastAPI:
    # cấu hình logging trước khi tạo app
    configure_logging()

    app = FastAPI(
        title="LabC2 Simulator",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS cho dev / lab
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware: metrics + request logging
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(RequestLogMiddleware)

    # API routers
    prefix = settings.api_prefix.rstrip("/")
    app.include_router(health.router, prefix=prefix)
    app.include_router(auth.router, prefix=prefix)
    app.include_router(agents.router, prefix=prefix)
    app.include_router(tasks.router, prefix=prefix)
    app.include_router(files.router, prefix=prefix)

    # /metrics nằm ngoài api_prefix
    app.include_router(metrics_router)

    return app


app = create_app()
