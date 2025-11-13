from sqlalchemy.orm import Session
from .db_models import AuditLog


def log(db: Session, actor: str, action: str, details: dict):
    db.add(AuditLog(actor=actor, action=action, details=details))
    db.commit()
