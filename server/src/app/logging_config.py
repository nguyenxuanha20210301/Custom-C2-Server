# server/src/app/logging_config.py
import json
import logging
import sys
import time
import uuid
from logging.handlers import RotatingFileHandler
from typing import Any, Dict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from .settings import settings


class JsonOrTextFormatter(logging.Formatter):
    """Formatter có thể xuất log dạng text hoặc JSON."""

    def __init__(self, use_json: bool) -> None:
        super().__init__(
            fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
        self.use_json = use_json

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        if not self.use_json:
            return super().format(record)

        payload: Dict[str, Any] = {
            "ts": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        # Các field extra thường dùng trong middleware
        for key in (
            "request_id",
            "method",
            "path",
            "status_code",
            "duration_ms",
            "agent_id",
            "user",
        ):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        return json.dumps(payload, ensure_ascii=False)


def configure_logging() -> None:
    """Cấu hình logging global cho app.

    - Level lấy từ settings.log_level (LOG_LEVEL trong .env)
    - Log ra stdout
    - Nếu LOG_FILE được set thì thêm RotatingFileHandler
    """
    level_name = settings.log_level.upper()
    level = getattr(logging, level_name, logging.INFO)

    formatter = JsonOrTextFormatter(use_json=settings.log_json)

    handlers = []

    # stdout handler (container đọc log từ đây)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    handlers.append(stream_handler)

    # optional file handler (dev)
    if settings.log_file:
        file_handler = RotatingFileHandler(
            settings.log_file,
            maxBytes=settings.log_max_bytes,
            backupCount=settings.log_backup_count,
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    logging.basicConfig(
        level=level,
        handlers=handlers,
        force=True,  # override cấu hình cũ của logging nếu có
    )

    logging.getLogger("uvicorn").setLevel(level)
    logging.getLogger("uvicorn.error").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(level)


class RequestLogMiddleware(BaseHTTPMiddleware):
    """Middleware log mỗi request với request_id & timing."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start = time.perf_counter()

        response = await call_next(request)

        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        logger = logging.getLogger("app.request")
        logger.info(
            "request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )

        response.headers["X-Request-ID"] = request_id
        return response
