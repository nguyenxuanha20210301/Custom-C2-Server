from fastapi import FastAPI
from .routes import auth, agents, tasks, files, health
from .db import Base, engine, SessionLocal
from .auth import ensure_admin_exists
from .config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title="Custom C2 Simulator API (Academic, Safe)",
        version="0.1.0",
        description="No remote code execution. Benign tasks only.",
    )

    # Khởi tạo DB (dev)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        ensure_admin_exists(db)

    # Routers
    app.include_router(health.router, prefix=settings.api_prefix, tags=["health"])
    app.include_router(auth.router, prefix=f"{settings.api_prefix}/auth", tags=["auth"])
    app.include_router(agents.router, prefix=f"{settings.api_prefix}/agents", tags=["agents"])
    app.include_router(tasks.router, prefix=f"{settings.api_prefix}/tasks", tags=["tasks"])
    app.include_router(files.router, prefix=f"{settings.api_prefix}/files", tags=["files"])
    return app

app = create_app()
