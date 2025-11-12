import os
from uuid import uuid4
from typing import Tuple
from .config import settings
from minio import Minio

def _minio_client():
    return Minio(
        settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )

def ensure_bucket():
    client = _minio_client()
    if not client.bucket_exists(settings.minio_bucket):
        client.make_bucket(settings.minio_bucket)

def store_bytes(content: bytes, filename: str, content_type: str) -> Tuple[str, str]:
    file_id = str(uuid4())
    if settings.storage_driver == "minio":
        ensure_bucket()
        key = f"{file_id}/{filename}"
        client = _minio_client()
        client.put_object(
            bucket_name=settings.minio_bucket,
            object_name=key,
            data=content,
            length=len(content),
            content_type=content_type,
        )
        return file_id, key
    else:
        os.makedirs(settings.local_storage_dir, exist_ok=True)
        key = os.path.join(settings.local_storage_dir, f"{file_id}_{filename}")
        with open(key, "wb") as f:
            f.write(content)
        return file_id, key
