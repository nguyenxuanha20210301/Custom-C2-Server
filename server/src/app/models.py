from typing import List, Optional, Dict, Any, Literal
from uuid import UUID
from pydantic import BaseModel, Field

Platform = Literal["linux", "windows", "macos", "other"]
TaskType = Literal["collect-metrics", "download-config", "upload-report"]


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int = 3600


# Agents
class AgentRegisterRequest(BaseModel):
    hostname: str
    platform: Platform = "linux"
    tags: Optional[List[str]] = Field(default_factory=list)
    public_key: Optional[str] = None


class AgentRegisterResponse(BaseModel):
    agent_id: UUID
    poll_interval: int = 60
    config: Dict[str, Any] = Field(default_factory=dict)


class HeartbeatRequest(BaseModel):
    uptime: int
    load: float
    ip: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)


# Tasks
class TaskItem(BaseModel):
    task_id: UUID
    type: TaskType
    payload: Dict[str, Any] = Field(default_factory=dict)
    created_at: str


class CreateTaskRequest(BaseModel):
    agent_ids: List[UUID]
    type: TaskType
    meta: Dict[str, Any] = Field(default_factory=dict)
    expires_in: Optional[int] = 3600


class CreateTaskResponse(BaseModel):
    task_id: UUID


# Files
class FileUploadResponse(BaseModel):
    file_id: UUID
    url: str


class TaskFilter(BaseModel):
    status: Optional[str] = None
    type: Optional[TaskType] = None
    agent_id: Optional[UUID] = None


class TaskSummary(BaseModel):
    id: UUID
    type: TaskType
    status: str
    created_at: str


class AgentTaskAck(BaseModel):
    ack: bool = True


class AgentTaskUpdate(BaseModel):
    status: str  # running|done|failed|canceled
    result: Dict[str, Any] | None = None
    error: str | None = None
