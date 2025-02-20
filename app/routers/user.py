from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db

router = APIRouter(prefix="/users")

@router.get(path="/get", response_model=schemas.Pagination[schemas.UserGet], status_code=status.HTTP_200_OK, tags=["Users"])
async def get_users(db: Session = Depends(get_db)):
    return await crud.get_users(db)