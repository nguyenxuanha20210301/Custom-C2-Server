# server/src/app/settings.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # ================= Phase 0: Core app =================
    environment: str = Field("development")
    log_level: str = Field("info")

    host: str = Field("0.0.0.0")
    port: int = Field(8000)
    api_prefix: str = Field("/api/v1")

    # ================= Logging =================
    log_json: bool = Field(False)
    log_file: str | None = Field(None)
    log_max_bytes: int = Field(5 * 1024 * 1024)  # 5MB
    log_backup_count: int = Field(3)

    # ================= Auth / JWT =================
    jwt_secret: str = Field("test-secret")  # dùng giá trị default để test không fail
    auth_disabled: bool = Field(False)
    access_token_expire_minutes: int = Field(60)
    refresh_token_expire_days: int = Field(7)
    jwt_issuer: str = Field("custom-c2-server")

    # ================= Database =================
    database_url: str = Field("sqlite:///test.db")  # default để pytest không fail
    db_pool_size: int = Field(5)
    db_retry_attempts: int = Field(5)
    db_retry_delay: int = Field(2)
    migration_tool: str = Field("alembic")

    # ================= Object storage =================
    storage_driver: str = Field("local")  # local|minio

    minio_endpoint: str = Field("minio:9000")
    minio_access_key: str = Field("minio")
    minio_secret_key: str = Field("minio123")
    minio_secure: bool = Field(False)
    minio_bucket: str = Field("c2-artifacts")

    local_storage_dir: str = Field("./data")

    # ================= RBAC / bootstrap admin =================
    default_admin_user: str = Field("admin")
    default_admin_pass: str = Field("ChangeMe_123!")

    # ================= Agent defaults =================
    agent_default_poll_sec: int = Field(60)
    heartbeat_retention_days: int = Field(30)

    # ================= Pydantic v2 config =================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",      # 👈 tránh lỗi pythonpath extra_forbidden
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
