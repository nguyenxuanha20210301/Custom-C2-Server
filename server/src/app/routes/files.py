from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from .agents import FILES  # in-memory prototype

router = APIRouter()

@router.get("/{file_id}")
def get_file(file_id: str):
    file_meta = FILES.get(file_id)
    if not file_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    # Prototype: không có signed URL thật; trả 200/redirect giả lập
    # Phase 3: generate signed URL từ MinIO/S3
    return {"file": file_meta, "message": "In dev, content is stored in-memory only"}
