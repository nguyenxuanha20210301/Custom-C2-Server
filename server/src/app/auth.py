import jwt
from datetime import datetime, timedelta, timezone
from passlib.hash import pbkdf2_sha256
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .config import settings
from .db import get_db
from .db_models import User

bearer = HTTPBearer(auto_error=False)

def hash_password(pw: str) -> str:
    return pbkdf2_sha256.hash(pw)

def verify_password(pw: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(pw, hashed)

def create_access_token(sub: str, role: str, expires_minutes: int | None = None) -> str:
    if not settings.jwt_secret:
        raise RuntimeError("JWT_SECRET missing")
    exp_min = expires_minutes or settings.access_expires_minutes
    now = datetime.now(timezone.utc)
    payload = {
        "iss": settings.jwt_issuer,
        "sub": sub,
        "role": role,
        "exp": now + timedelta(minutes=exp_min),
        "iat": now,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"], options={"require": ["exp", "iat"]})
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def require_user(db: Session = Depends(get_db), cred: HTTPAuthorizationCredentials = Depends(bearer)):
    if settings.auth_disabled:
        return {"sub": "dev-operator", "role": "admin"}
    if not cred:
        raise HTTPException(status_code=401, detail="Missing token")
    data = decode_token(cred.credentials)
    return {"sub": data["sub"], "role": data.get("role", "operator")}

def require_role(role: str):
    def dep(user=Depends(require_user)):
        ranking = {"admin": 3, "operator": 2, "auditor": 1}
        if ranking.get(user.get("role", "operator"), 0) < ranking.get(role, 0):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return dep

def ensure_admin_exists(db: Session):
    u = db.query(User).filter(User.username == settings.default_admin_user).first()
    if not u:
        db.add(User(
            username=settings.default_admin_user,
            password_hash=hash_password(settings.default_admin_pass),
            role="admin"
        ))
        db.commit()
