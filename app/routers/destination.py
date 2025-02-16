from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/destinations")



@router.get(path="/get/id/{id}", response_model=schemas.Destination, status_code=status.HTTP_200_OK, tags=["Destinations"])
async def get_destination_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.destination.get_destination_by_id(id, db)

@router.get(path="/get/zipcode/{zipcode}", response_model=schemas.Destination, status_code=status.HTTP_200_OK, tags=["Destinations"])
async def get_destination_by_zipcode(zipcode: str, db: Session = Depends(get_db)):
    return await crud.destination.get_destination_by_zipcode(zipcode, db)

@router.get(path="/get", response_model=list[schemas.Destination], status_code=status.HTTP_200_OK, tags=["Destinations"])
async def get_destinations(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return await crud.destination.get_destinations(db, page, limit)

@router.post(path="/create", response_model=schemas.Destination, status_code=status.HTTP_200_OK, tags=["Destinations"])
async def create_destination(data: schemas.DestinationCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.destination.create_destination(data, db)

@router.put(path="/update/{id}", response_model=schemas.Destination, status_code=status.HTTP_200_OK, tags=["Destinations"])
async def update_destination(id: int, data: schemas.DestinationUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.destination.update_destination(id, data, db)

@router.delete(path="/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Destinations"])
async def delete_destination(id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.destination.delete_destination(id, db)

