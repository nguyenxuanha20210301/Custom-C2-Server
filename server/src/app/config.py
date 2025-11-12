import os
from pydantic import BaseModel

class Settings(BaseModel):
    # Phase 0
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "info")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")

    # Auth / JWT (Phase 2/3)
    jwt_secret: str = os.getenv("JWT_SECRET", "")
    auth_disabled: bool = os.getenv("AUTH_DISABLED", "false").lower() == "true"
    access_expires_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    refresh_expires_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    jwt_issuer: str = os.getenv("JWT_ISSUER", "custom-c2-server")

    # DB (Phase 3)
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    db_pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
    db_retry_attempts: int = int(os.getenv("DB_RETRY_ATTEMPTS", "5"))
    db_retry_delay: int = int(os.getenv("DB_RETRY_DELAY", "2"))
    migration_tool: str = os.getenv("MIGRATION_TOOL", "alembic")

    # Storage (Phase 3)
    storage_driver: str = os.getenv("STORAGE_DRIVER", "local")  # minio|local
    local_storage_dir: str = os.getenv("LOCAL_STORAGE_DIR", "./data")
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "")
    minio_secure: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    minio_bucket: str = os.getenv("MINIO_BUCKET", "c2-artifacts")

    # Bootstrap admin (Phase 3)
    default_admin_user: str = os.getenv("DEFAULT_ADMIN_USER", "admin")
    default_admin_pass: str = os.getenv("DEFAULT_ADMIN_PASS", "ChangeMe_123!")

    # Agent defaults
    agent_default_poll_sec: int = int(os.getenv("AGENT_DEFAULT_POLL_SEC", "60"))
    hb_retention_days: int = int(os.getenv("HEARTBEAT_RETENTION_DAYS", "30"))

settings = Settings()
