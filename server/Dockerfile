FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY alembic.ini .
COPY alembic ./alembic
COPY entrypoint.sh ./entrypoint.sh

# RUN useradd -m appuser && chmod +x /app/entrypoint.sh
# USER appuser

# ENV PYTHONPATH=/app/src

# EXPOSE 8000
# CMD ["./entrypoint.sh"]

# Tạo user, tạo file log, cấp quyền đầy đủ cho appuser
RUN useradd -m appuser \
    && touch /app/server.log \
    && chown -R appuser:appuser /app \
    && chmod +x /app/entrypoint.sh

USER appuser

ENV PYTHONPATH=/app/src

EXPOSE 8000
CMD ["./entrypoint.sh"]