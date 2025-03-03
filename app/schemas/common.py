from pydantic import BaseModel
from typing import List, Generic, TypeVar, Optional

placeholder = TypeVar("T")

class Pagination(BaseModel, Generic[placeholder]):
    data: List[placeholder]
    total_rows: Optional[int]
    total_pages: Optional[int]
    current_page: Optional[int]
    limit: Optional[int]