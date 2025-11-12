import os
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer(auto_error=False)

# PLACEHOLDERS bạn cần set qua env/secret manager
JWT_SECRET = os.getenv("JWT_SECRET", None)  # <<THAY_THEO_BAN: bắt buộc khi bật auth>>
AUTH_DISABLED = os.getenv("AUTH_DISABLED", "true").lower() == "true"  # cho dev

def require_auth(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Auth stub cho operators.
    - Dev: có thể bật AUTH_DISABLED=true để bỏ qua (không khuyến nghị prod).
    - Prod: xác thực JWT chuẩn (verify signature, expiry, roles).
    """
    if AUTH_DISABLED:
        return {"sub": "dev-operator", "roles": ["admin"]}

    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = credentials.credentials
    if not JWT_SECRET:
        raise HTTPException(status_code=500, detail="Server misconfigured: JWT_SECRET missing")

    # TODO: verify JWT properly (signature, exp, roles)
    # Đây là stub an toàn: không parse/exec gì nguy hiểm.
    if not token or len(token) < 10:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"sub": "operator", "roles": ["admin"]}
