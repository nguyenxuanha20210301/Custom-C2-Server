from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import LoginRequest, TokenResponse
from ..db import get_db
from ..db_models import User
from ..auth import verify_password, create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(sub=user.username, role=user.role)
    return TokenResponse(access_token=token, refresh_token=None, expires_in=3600)

@router.post("/refresh", response_model=TokenResponse)
def refresh(_: dict):
    # (Tối giản demo – Phase sau có thể triển khai refresh thật)
    return TokenResponse(access_token="dev-token-placeholder", refresh_token=None, expires_in=3600)
