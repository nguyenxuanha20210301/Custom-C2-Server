from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey, JSON
from uuid import uuid4
from datetime import datetime, timezone
from .db import Base

def now():
    return datetime.now(timezone.utc)

UUIDCol = String(36)  # portable

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(UUIDCol, primary_key=True, default=lambda: str(uuid4()))
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(16), default="admin")  # admin|operator|auditor
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Agent(Base):
    __tablename__ = "agents"
    id: Mapped[str] = mapped_column(UUIDCol, primary_key=True, default=lambda: str(uuid4()))
    hostname: Mapped[str] = mapped_column(String(128))
    platform: Mapped[str] = mapped_column(String(16))
    tags: Mapped[str] = mapped_column(String(512), default="")  # csv
    public_key: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Heartbeat(Base):
    __tablename__ = "heartbeats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agent_id: Mapped[str] = mapped_column(UUIDCol, ForeignKey("agents.id", ondelete="CASCADE"))
    uptime: Mapped[int] = mapped_column(Integer)
    load: Mapped[float] = mapped_column(Integer, default=0)
    ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = mapped_column(UUIDCol, primary_key=True, default=lambda: str(uuid4()))
    type: Mapped[str] = mapped_column(String(32))  # benign only
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class AgentTask(Base):
    __tablename__ = "agent_tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agent_id: Mapped[str] = mapped_column(UUIDCol, ForeignKey("agents.id", ondelete="CASCADE"))
    task_id: Mapped[str] = mapped_column(UUIDCol, ForeignKey("tasks.id", ondelete="CASCADE"))
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class FileMeta(Base):
    __tablename__ = "files"
    id: Mapped[str] = mapped_column(UUIDCol, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(128))
    size: Mapped[int] = mapped_column(Integer)
    storage_key: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor: Mapped[str] = mapped_column(String(64))
    action: Mapped[str] = mapped_column(String(64))
    details: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
