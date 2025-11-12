from fastapi import APIRouter
from ..models import LoginRequest, TokenResponse

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    # DEV ONLY: trả token giả (không ký). Production cần JWT chuẩn.
    return TokenResponse(access_token="dev-token-placeholder", refresh_token=None, expires_in=3600)

@router.post("/refresh", response_model=TokenResponse)
def refresh(refresh_token: dict):
    # DEV ONLY
    _ = refresh_token
    return TokenResponse(access_token="dev-token-placeholder", refresh_token=None, expires_in=3600)
