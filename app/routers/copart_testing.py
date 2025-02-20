from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, utils
from ..core.database import get_db

router = APIRouter(prefix="/copart-testing")

@router.get(path="/get", status_code=status.HTTP_200_OK, tags=["Copart"])
async def get_postal_code():
    return await utils.get_postal_code("41593405")