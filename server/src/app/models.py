# server/src/app/models.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# ========= Health =========


class HealthResponse(BaseModel):
    status: str = "ok"


# ========= Auth / Users =========


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    role: str


# ========= Agents & Heartbeats =========


class AgentRegisterRequest(BaseModel):
    hostname: str
    platform: str
    tags: List[str] | None = None
    public_key: Optional[str] = None


class AgentRegisterResponse(BaseModel):
    agent_id: str
    poll_interval: int
    config: Dict[str, Any]


class HeartbeatRequest(BaseModel):
    """
    Payload heartbeat từ agent gửi về server.

    Trong test chỉ gửi:
      { "uptime": 10, "load": 0.1 }

    Nên:
      - ip phải là optional, có default None
    """
    uptime: int = Field(..., description="Uptime (giây) mô phỏng của agent")
    load: float = Field(..., description="Load trung bình mô phỏng (0.0-1.0)")
    ip: Optional[str] = Field(
        default=None,
        description="Địa chỉ IP mô phỏng; có thể bỏ trống trong test",
    )


class TaskItem(BaseModel):
    task_id: str
    type: str
    payload: Dict[str, Any] | None = None
    created_at: str


class FileUploadResponse(BaseModel):
    file_id: str
    url: str


class AgentTaskAck(BaseModel):
    """
    Body cho /agents/{id}/ack/{task_id}.
    Hiện tại không cần field nào, nhưng để sẵn cho future.
    """
    note: Optional[str] = None


# ========= Simulated C2 Specs & Result (Phase 9–10) =========


class SimExecSpec(BaseModel):
    """
    Mô tả một "command" mô phỏng.

    Ví dụ:
      {
        "name": "ps",
        "args": ["-aux"]
      }

    Agent simulator chỉ dùng để tra vào catalog và trả stdout giả.
    """

    name: str = Field(..., description="Tên command mô phỏng, vd: whoami, ps, netstat")
    args: List[str] = Field(default_factory=list)


class SimPersistSpec(BaseModel):
    """
    Mô tả một cơ chế persistence mô phỏng.
    """

    mechanism: str = Field(..., description="Kiểu persistence mô phỏng, vd: startup_folder")
    label: str = Field(..., description="Tên logic của implant/agent")


class SimDeliverySpec(BaseModel):
    """
    Mô tả nhiệm vụ 'payload delivery' mô phỏng.
    """

    artifact_name: str = Field(..., description="Tên payload logic, vd: benign-tool.zip")
    size_kb: int = Field(..., ge=0, description="Kích thước mô phỏng (KB)")
    stage: str = Field(
        "staging",
        description="Giai đoạn: staging / delivery / execution (chỉ mang tính logical)",
    )


class TaskSimResult(BaseModel):
    """
    Kết quả mô phỏng từ agent. Không chứa output thật từ hệ thống.

    Tùy loại task, một số field sẽ được sử dụng.
    """

    kind: str = Field(..., description="exec / persist / delivery / noop")
    success: bool = Field(True)

    # Cho sim.exec
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None

    # Cho sim.persist
    persistence_mechanism: Optional[str] = None
    installed: Optional[bool] = None

    # Cho sim.delivery
    artifact_name: Optional[str] = None
    stage: Optional[str] = None


# ========= Tasks & Pagination =========


class CreateTaskRequest(BaseModel):
    """
    Request tạo task từ operator.

    type:
      - collect-metrics      -> Phase 4/5
      - sim.exec             -> Phase 9: mô phỏng command / reverse shell
      - sim.persist          -> Phase 9: mô phỏng persistence
      - sim.delivery         -> Phase 10: mô phỏng payload delivery
    """

    agent_ids: List[str]
    type: str = Field(..., description="Loại nhiệm vụ")
    meta: Dict[str, Any] | None = Field(
        default=None,
        description="Metadata cho từng loại task (tùy type).",
    )


class CreateTaskResponse(BaseModel):
    task_id: str


class TaskSummary(BaseModel):
    id: str
    type: str
    status: str
    created_at: str


class AgentTaskUpdate(BaseModel):
    status: str
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None


class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int