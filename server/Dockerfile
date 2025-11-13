# Multi-stage build: slim image, non-root
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy src
COPY src ./src

# Create non-root user
RUN useradd -m appuser
USER appuser

# đảm bảo Python thấy /app/src
ENV PYTHONPATH=/app/src

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "/app/src"]

COPY src ./src
# thêm nếu chưa có:
# ENV PYTHONPATH=/app/src
# CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--app-dir","/app/src"]