from pydantic import BaseModel, conint
from typing import Generic, List, TypeVar


T = TypeVar("T")

class PageParams(BaseModel):
    page: conint(ge=1) = 1
    size: conint(ge=1, le=100) = 5


class PagedResponseSchema(BaseModel, Generic[T]):
    """Response schema for any paged API."""
    total: int
    page: int
    size: int
    results: List[T]