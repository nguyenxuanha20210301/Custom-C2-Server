#!/usr/bin/env bash
set -e

echo "[entrypoint] running DB migrations..."
alembic upgrade head

echo "[entrypoint] starting uvicorn..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir /app/src
