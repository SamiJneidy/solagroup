from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..crud.authentication import get_current_user
from ..core.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    path="/get",
    response_model=schemas.Pagination[schemas.UserGet],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    db: Session = Depends(get_db), page: int = None, limit: int = None, current_user = Depends(get_current_user)
):
    """Returns the users that have access to the dashboard."""
    return await crud.get_users(db, page, limit)
