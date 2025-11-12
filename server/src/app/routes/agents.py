from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from ..models import AgentRegisterRequest, AgentRegisterResponse, HeartbeatRequest, TaskItem, FileUploadResponse
from typing import List
from datetime import datetime, timezone

router = APIRouter()

# In-memory stores cho prototype (Phase 3 sẽ dùng DB)
AGENTS = {}
TASKS = {}
FILES = {}

@router.post("/register", response_model=AgentRegisterResponse)
def register_agent(req: AgentRegisterRequest):
    agent_id = uuid4()
    AGENTS[str(agent_id)] = {
        "hostname": req.hostname,
        "platform": req.platform,
        "tags": req.tags or [],
        "public_key": req.public_key,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    return AgentRegisterResponse(agent_id=agent_id, poll_interval=60, config={})

@router.post("/{agent_id}/heartbeat")
def heartbeat(agent_id: str, hb: HeartbeatRequest):
    if agent_id not in AGENTS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    # Prototype: chỉ ghi nhận. Phase 3: lưu DB + retention policy.
    return {"ok": True}

@router.get("/{agent_id}/tasks", response_model=List[TaskItem])
def get_tasks(agent_id: str, limit: int = 10):
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail="Agent not found")
    items = TASKS.get(agent_id, [])
    return items[: max(1, min(limit, 100))]

@router.put("/{agent_id}/upload", response_model=FileUploadResponse)
async def upload(agent_id: str, file: UploadFile = File(...)):
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail="Agent not found")
    # Whitelist rất cơ bản (Phase 3 sẽ cấu hình chi tiết)
    allowed = {"text/plain", "application/json", "application/pdf"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported content type: {file.content_type}")
    file_id = str(uuid4())
    # Prototype: đọc bytes vào memory — Phase 3 sẽ ghi S3/MinIO
    content = await file.read()
    FILES[file_id] = {"name": file.filename, "content_type": file.content_type, "size": len(content)}
    return FileUploadResponse(file_id=file_id, url=f"/api/v1/files/{file_id}")
