from fastapi import FastAPI
from .routes import auth, agents, tasks, files, health
from .db import Base, engine, SessionLocal
from .auth import ensure_admin_exists
from .config import settings
from .metrics import MetricsMiddleware, metrics_endpoint
from .web import routes as web_routes

def create_app() -> FastAPI:
    app = FastAPI(
        title="Custom C2 Simulator API (Academic, Safe)",
        version="0.4.0",
        description="No remote code execution. Benign tasks only.",
    )

    app.add_middleware(MetricsMiddleware)
    app.add_api_route("/metrics", metrics_endpoint, methods=["GET"], include_in_schema=False)

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        ensure_admin_exists(db)

    prefix = settings.api_prefix
    app.include_router(health.router, prefix=prefix, tags=["health"])
    app.include_router(auth.router, prefix=f"{prefix}/auth", tags=["auth"])
    app.include_router(agents.router, prefix=f"{prefix}/agents", tags=["agents"])
    app.include_router(tasks.router, prefix=f"{prefix}/tasks", tags=["tasks"])
    app.include_router(files.router, prefix=f"{prefix}/files", tags=["files"])

    # Web dashboard
    app.include_router(web_routes.router, prefix="/web", tags=["web"])
    return app

app = create_app()
