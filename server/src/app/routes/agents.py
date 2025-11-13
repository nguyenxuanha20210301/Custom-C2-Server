from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models import AgentRegisterRequest, AgentRegisterResponse
from ..models import HeartbeatRequest, TaskItem, FileUploadResponse
from ..db import get_db
from ..db_models import Agent, Heartbeat, FileMeta, AgentTask, Task
from ..storage import store_bytes
from typing import List
from datetime import datetime, timezone
from ..models import AgentTaskAck, AgentTaskUpdate

router = APIRouter()
def _now(): return datetime.now(timezone.utc)


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
        items.append(TaskItem(task_id=t.id,
                              type=t.type,
                              payload=t.payload,
                              created_at=t.created_at.isoformat()))
    return items


@router.put("/{agent_id}/upload", response_model=FileUploadResponse)
async def upload(agent_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    allowed = {"text/plain", "application/json", "application/pdf"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400,
                            detail=f"Unsupported content type: {file.content_type}")

    content = await file.read()
    file_id, storage_key = store_bytes(content, file.filename, file.content_type)

    meta = FileMeta(id=file_id, name=file.filename,
                    content_type=file.content_type,
                    size=len(content),
                    storage_key=storage_key)
    db.add(meta)
    db.commit()

    return FileUploadResponse(file_id=file_id, url=f"/api/v1/files/{file_id}")


@router.get("/{agent_id}/next", response_model=List[TaskItem])
def next_tasks(agent_id: str, limit: int = 1, db: Session = Depends(get_db)):
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    q = (db.query(AgentTask, Task)
         .join(Task, Task.id == AgentTask.task_id)
         .filter(AgentTask.agent_id == agent_id, AgentTask.status.in_(["pending", "acknowledged"]))
         .order_by(Task.created_at.asc())
         .limit(min(max(limit, 1), 10)))
    items = []
    for at, t in q:
        items.append(TaskItem(task_id=t.id,
                              type=t.type,
                              payload=t.payload,
                              created_at=t.created_at.isoformat()))
    return items


@router.post("/{agent_id}/ack/{task_id}")
def ack_task(agent_id: str, task_id: str, _: AgentTaskAck, db: Session = Depends(get_db)):
    at = db.query(AgentTask).filter(AgentTask.agent_id == agent_id,
                                    AgentTask.task_id == task_id).first()
    if not at:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if at.status == "pending":
        at.status = "acknowledged"
        at.acknowledged_at = _now()
        db.commit()
    return {"ok": True}


@router.post("/{agent_id}/complete/{task_id}")
def complete_task(agent_id: str,
                  task_id: str,
                  body: AgentTaskUpdate,
                  db: Session = Depends(get_db)):
    at = db.query(AgentTask).filter(AgentTask.agent_id == agent_id,
                                    AgentTask.task_id == task_id).first()
    if not at:
        raise HTTPException(status_code=404, detail="Assignment not found")
    at.status = body.status
    at.finished_at = _now()
    at.last_error = body.error
    # tổng hợp trạng thái về Task nếu mọi AgentTask đã kết thúc
    db.commit()
    remaining = db.query(AgentTask).filter(AgentTask.task_id == task_id,
                                           AgentTask.status.in_(["pending",
                                                                 "acknowledged",
                                                                 "running"])).count()
    if remaining == 0:
        t = db.get(Task, task_id)
        if t:
            failed_count = db.query(AgentTask).filter(AgentTask.task_id == task_id,
                                                      AgentTask.status == "failed").count()
            t.status = "failed" if failed_count > 0 else "done"
            if body.result is not None:
                t.result = body.result
            db.commit()

    return {"ok": True}
