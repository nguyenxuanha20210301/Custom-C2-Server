from fastapi import Query
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int

def page_params(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    return {"page": page, "size": size}

def apply_pagination(query, page: int, size: int):
    total = query.count()
    items = query.offset((page-1)*size).limit(size).all()
    return items, total
