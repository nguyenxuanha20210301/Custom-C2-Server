from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models import CreateTaskRequest, CreateTaskResponse
from ..auth import require_role
from ..db import get_db
from ..db_models import Task, AgentTask

router = APIRouter()

@router.post("", response_model=CreateTaskResponse, status_code=201)
def create_task(req: CreateTaskRequest, db: Session = Depends(get_db), user=Depends(require_role("operator"))):
    t = Task(type=req.type, payload=req.meta or {})
    db.add(t)
    db.commit()
    db.refresh(t)
    for aid in req.agent_ids:
        db.add(AgentTask(agent_id=str(aid), task_id=t.id))
    db.commit()
    return CreateTaskResponse(task_id=t.id)
