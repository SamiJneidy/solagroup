from pydantic import BaseModel
from typing import List, Generic, TypeVar

placeholder = TypeVar("T")

class Pagination(BaseModel, Generic[placeholder]):
    data: List[placeholder]
    total_rows: int
    total_pages: int
    current_page: int
    limit: int