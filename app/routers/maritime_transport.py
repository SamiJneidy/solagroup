from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/maritime-transport")

@router.get(path="/get/id/{id}", response_model=schemas.MaritimeTransport, status_code=status.HTTP_200_OK, tags=["Maritime Transport"])
async def get_maritime_transport_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.maritime_transport.get_maritime_transport_by_id(id, db)

@router.get(path="/get", response_model=schemas.Pagination[schemas.MaritimeTransport], status_code=status.HTTP_200_OK, tags=["Maritime Transport"])
async def get_maritime_transports(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return await crud.maritime_transport.get_maritime_transports(db, page, limit)

@router.post(path="/create", response_model=schemas.MaritimeTransport, status_code=status.HTTP_200_OK, tags=["Maritime Transport"])
async def create_maritime_transport(data: schemas.MaritimeTransportCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.maritime_transport.create_maritime_transport(data, db)

@router.put(path="/update/{id}", response_model=schemas.MaritimeTransport, status_code=status.HTTP_200_OK, tags=["Maritime Transport"])
async def update_maritime_transport(id: int, data: schemas.MaritimeTransportUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.maritime_transport.update_maritime_transport(id, data, db)

@router.delete(path="/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Maritime Transport"])
async def delete_maritime_transport(id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.maritime_transport.delete_maritime_transport(id, db)

