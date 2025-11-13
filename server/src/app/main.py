# from fastapi import FastAPI
# from .routes import auth, agents, tasks, files, health
# from .db import Base, engine, SessionLocal
# from .auth import ensure_admin_exists
# from .config import settings
# from .metrics import MetricsMiddleware, metrics_endpoint
# from .web import routes as web_routes


# def create_app() -> FastAPI:
#     app = FastAPI(
#         title="Custom C2 Simulator API (Academic, Safe)",
#         version="0.5.0",
#         description="No remote code execution. Benign tasks only.",
#     )

#     app.add_middleware(MetricsMiddleware)
#     app.add_api_route("/metrics", metrics_endpoint, methods=["GET"], include_in_schema=False)

#     Base.metadata.create_all(bind=engine)

#     # Sau khi có bảng rồi mới ensure admin
#     with SessionLocal() as db:
#         ensure_admin_exists(db)

#     prefix = settings.api_prefix
#     app.include_router(health.router, prefix=prefix, tags=["health"])
#     app.include_router(auth.router, prefix=f"{prefix}/auth", tags=["auth"])
#     app.include_router(agents.router, prefix=f"{prefix}/agents", tags=["agents"])
#     app.include_router(tasks.router, prefix=f"{prefix}/tasks", tags=["tasks"])
#     app.include_router(files.router, prefix=f"{prefix}/files", tags=["files"])

#     # Web dashboard
#     app.include_router(web_routes.router, prefix="/web", tags=["web"])
#     return app


# app = create_app()

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Thay cho @app.on_event("startup") (đã deprecated).

    Chạy khi app start:
      - Tạo schema nếu dùng SQLite (môi trường test/dev)
      - Bootstrap admin user
    """

    # chỉ dùng Base.metadata.create_all cho SQLite / test
    if settings.database_url.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)

    # Bootstrapping admin user
    db = SessionLocal()
    try:
        ensure_admin_exists(db)
    finally:
        db.close()

    # nhường control cho app chạy
    yield

    # nếu sau này cần logic shutdown thì thêm dưới này
    # ví dụ: đóng connection pool, flush metrics, ...
    # hiện tại chưa cần làm gì nên để trống
    return


def create_app() -> FastAPI:
    # cấu hình logging trước khi tạo app
    configure_logging()

    app = FastAPI(
        title="Custom C2 Simulator",
        version="0.1.0",
        lifespan=lifespan,  # 👈 dùng lifespan thay cho @app.on_event
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
