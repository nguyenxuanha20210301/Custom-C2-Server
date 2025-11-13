from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..db import get_db
from ..db_models import Agent, Task, FileMeta

templates = Jinja2Templates(directory="src/app/web/templates")
router = APIRouter()

@router.get("")
def index(request: Request, db: Session = Depends(get_db)):
    stats = {
        "agents": db.query(Agent).count(),
        "tasks": db.query(Task).count(),
        "files": db.query(FileMeta).count(),
    }
    return templates.TemplateResponse("index.html", {"request": request, "title":"Dashboard", "stats": stats})

@router.get("/agents")
def agents(request: Request, db: Session = Depends(get_db)):
    agents = db.query(Agent).order_by(Agent.created_at.desc()).limit(100).all()
    return templates.TemplateResponse("agents.html", {"request": request, "agents": agents})

@router.get("/tasks")
def tasks(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).order_by(Task.created_at.desc()).limit(100).all()
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})

@router.get("/files")
def files(request: Request, db: Session = Depends(get_db)):
    files = db.query(FileMeta).order_by(FileMeta.created_at.desc()).limit(100).all()
    return templates.TemplateResponse("files.html", {"request": request, "files": files})
