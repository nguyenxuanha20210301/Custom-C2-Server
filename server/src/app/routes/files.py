from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from ..db import get_db
from ..db_models import FileMeta
from ..config import settings
import os

router = APIRouter()

@router.get("/{file_id}")
def get_file(file_id: str, db: Session = Depends(get_db)):
    meta = db.get(FileMeta, file_id)
    if not meta:
        raise HTTPException(status_code=404, detail="File not found")

    if settings.storage_driver == "local":
        if not os.path.exists(meta.storage_key):
            raise HTTPException(status_code=404, detail="File not found on disk")
        return FileResponse(meta.storage_key, media_type=meta.content_type, filename=meta.name)
    else:
        # Phase sau có thể trả signed URL; hiện trả metadata
        return JSONResponse({"file_id": meta.id, "name": meta.name, "content_type": meta.content_type, "size": meta.size})
