from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..models import AgentRegisterRequest, AgentRegisterResponse, HeartbeatRequest, TaskItem, FileUploadResponse
from ..db import get_db
from ..db_models import Agent, Heartbeat, FileMeta, AgentTask, Task
from ..storage import store_bytes
from typing import List

router = APIRouter()

@router.post("/register", response_model=AgentRegisterResponse)
def register_agent(req: AgentRegisterRequest, db: Session = Depends(get_db)):
    agent = Agent(
        hostname=req.hostname,
        platform=req.platform,
        tags=",".join(req.tags or []),
        public_key=req.public_key,
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return AgentRegisterResponse(agent_id=agent.id, poll_interval=60, config={})

@router.post("/{agent_id}/heartbeat")
def heartbeat(agent_id: str, hb: HeartbeatRequest, db: Session = Depends(get_db)):
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.add(Heartbeat(agent_id=agent_id, uptime=hb.uptime, load=hb.load, ip=hb.ip))
    db.commit()
    return {"ok": True}

@router.get("/{agent_id}/tasks", response_model=List[TaskItem])
def get_tasks(agent_id: str, limit: int = 10, db: Session = Depends(get_db)):
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    q = (
        db.query(AgentTask, Task)
        .join(Task, Task.id == AgentTask.task_id)
        .filter(AgentTask.agent_id == agent_id)
        .order_by(Task.created_at.desc())
        .limit(min(max(limit, 1), 100))
    )
    items: List[TaskItem] = []
    for at, t in q:
        items.append(TaskItem(task_id=t.id, type=t.type, payload=t.payload, created_at=t.created_at.isoformat()))
    return items

@router.put("/{agent_id}/upload", response_model=FileUploadResponse)
async def upload(agent_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    allowed = {"text/plain", "application/json", "application/pdf"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported content type: {file.content_type}")

    content = await file.read()
    file_id, storage_key = store_bytes(content, file.filename, file.content_type)

    meta = FileMeta(id=file_id, name=file.filename, content_type=file.content_type, size=len(content), storage_key=storage_key)
    db.add(meta)
    db.commit()

    return FileUploadResponse(file_id=file_id, url=f"/api/v1/files/{file_id}")
