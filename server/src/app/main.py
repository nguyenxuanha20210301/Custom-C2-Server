from fastapi import FastAPI
from .routes import auth, agents, tasks, files, health

def create_app() -> FastAPI:
    app = FastAPI(
        title="Custom C2 Simulator API (Academic, Safe)",
        version="0.1.0",
        description="No remote code execution. Benign tasks only.",
    )

    app.include_router(health.router, prefix="/api/v1", tags=["health"])
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
    app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
    app.include_router(files.router, prefix="/api/v1/files", tags=["files"])

    return app

app = create_app()
