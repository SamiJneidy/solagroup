from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/inland-transport")

@router.get(path="/get/id/{id}", response_model=schemas.InlandTransport, status_code=status.HTTP_200_OK, tags=["Inland Transport"])
async def get_inland_transport_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.inland_transport.get_inland_transport_by_id(id, db)

@router.get(path="/get", response_model=schemas.Pagination[schemas.InlandTransport], status_code=status.HTTP_200_OK, tags=["Inland Transport"])
async def get_inland_transports(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return await crud.inland_transport.get_inland_transports(db, page, limit)

@router.post(path="/create", response_model=schemas.InlandTransport, status_code=status.HTTP_200_OK, tags=["Inland Transport"])
async def create_inland_transport(data: schemas.InlandTransportCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.inland_transport.create_inland_transport(data, db)

@router.put(path="/update/{id}", response_model=schemas.InlandTransport, status_code=status.HTTP_200_OK, tags=["Inland Transport"])
async def update_inland_transport(id: int, data: schemas.InlandTransportUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.inland_transport.update_inland_transport(id, data, db)

@router.delete(path="/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Inland Transport"])
async def delete_inland_transport(id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.inland_transport.delete_inland_transport(id, db)

