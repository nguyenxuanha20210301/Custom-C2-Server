# server/src/app/routes/tasks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import CreateTaskRequest, CreateTaskResponse, TaskSummary
from ..auth import require_role
from ..db import get_db
from ..db_models import Task, AgentTask
from ..pagination import Page, page_params, apply_pagination
from ..audit import log

ALLOWED_TASK_TYPES = {
    "collect-metrics",
    "sim.exec",
    "sim.persist",
    "sim.delivery",
}

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("", response_model=CreateTaskResponse, status_code=201)
def create_task(
    req: CreateTaskRequest,
    db: Session = Depends(get_db),
    user=Depends(require_role("operator")),
):
    """
    Tạo task mới.

    type:
      - collect-metrics  : task benign có sẵn từ Phase 4/5
      - sim.exec         : Phase 9 – mô phỏng command / reverse shell
      - sim.persist      : Phase 9 – mô phỏng persistence
      - sim.delivery     : Phase 10 – mô phỏng payload staging / delivery

    Lưu ý:
      - Server KHÔNG thực thi lệnh nào trên hệ điều hành.
      - Server KHÔNG tải payload thực.
      - Tất cả logic thực thi nằm trong agent simulator và chỉ sử dụng catalog giả lập.
    """
    if req.type not in ALLOWED_TASK_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported task type: {req.type}",
        )

    t = Task(type=req.type, payload=req.meta or {}, status="queued")
    db.add(t)
    db.commit()
    db.refresh(t)

    for aid in req.agent_ids:
        db.add(
            AgentTask(
                agent_id=str(aid),
                task_id=t.id,
                status="pending",
            )
        )

    db.commit()

    log(
        db,
        actor=user["sub"],
        action="task.create",
        details={
            "task_id": t.id,
            "type": t.type,
            "agents": [str(a) for a in req.agent_ids],
        },
    )

    return CreateTaskResponse(task_id=t.id)


@router.get("", response_model=Page[TaskSummary])
def list_tasks(
    db: Session = Depends(get_db),
    q_status: str | None = None,
    q_type: str | None = None,
    params: dict = Depends(page_params),
    user=Depends(require_role("auditor")),
):
    page, size = params["page"], params["size"]

    query = db.query(Task)
    if q_status:
        query = query.filter(Task.status == q_status)
    if q_type:
        query = query.filter(Task.type == q_type)

    query = query.order_by(Task.created_at.desc())
    items, total = apply_pagination(query, page, size)

    resp = [
        TaskSummary(
            id=i.id,
            type=i.type,
            status=i.status,
            created_at=i.created_at.isoformat(),
        )
        for i in items
    ]

    return {
        "items": resp,
        "total": total,
        "page": page,
        "size": size,
    }


@router.post("/{task_id}/cancel")
def cancel_task(
    task_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("operator")),
):
    t = db.get(Task, task_id)
    if not t:
        return {"ok": False, "reason": "not_found"}

    t.status = "canceled"

    (
        db.query(AgentTask)
        .filter(
            AgentTask.task_id == task_id,
            AgentTask.status.in_(["pending", "acknowledged", "running"]),
        )
        .update({AgentTask.status: "canceled"}, synchronize_session=False)
    )

    db.commit()

    log(
        db,
        actor=user["sub"],
        action="task.cancel",
        details={"task_id": task_id},
    )

    return {"ok": True}
