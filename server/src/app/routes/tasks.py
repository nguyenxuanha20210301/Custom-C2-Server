from uuid import uuid4
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from ..models import CreateTaskRequest, CreateTaskResponse, TaskItem
from ..deps import require_auth

router = APIRouter()

# reuse in-memory TASKS from agents module
from .agents import TASKS  # noqa

@router.post("", response_model=CreateTaskResponse, status_code=201)
def create_task(req: CreateTaskRequest, user=Depends(require_auth)):
    # Only benign types by schema; assign per-agent
    now = datetime.now(timezone.utc).isoformat()
    tid = uuid4()
    for aid in req.agent_ids:
        TASKS.setdefault(str(aid), []).append(
            TaskItem(task_id=tid, type=req.type, payload=req.meta or {}, created_at=now)
        )
    return CreateTaskResponse(task_id=tid)
