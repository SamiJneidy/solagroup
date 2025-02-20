from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/sources")

@router.get(path="/get/id/{id}", response_model=schemas.Source, status_code=status.HTTP_200_OK, tags=["Sources"])
async def get_source_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.source.get_source_by_id(id, db)

@router.get(path="/get/zipcode/{zipcode}", response_model=schemas.Source, status_code=status.HTTP_200_OK, tags=["Sources"])
async def get_source_by_zipcode(zipcode: str, db: Session = Depends(get_db)):
    return await crud.source.get_source_by_zipcode(zipcode, db)

@router.get(path="/get", response_model=schemas.Pagination[schemas.Source], status_code=status.HTTP_200_OK, tags=["Sources"])
async def get_sources(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return await crud.source.get_sources(db, page, limit)

@router.post(path="/create", response_model=schemas.Source, status_code=status.HTTP_200_OK, tags=["Sources"])
async def create_source(data: schemas.SourceCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.source.create_source(data, db)

@router.put(path="/update/{id}", response_model=schemas.Source, status_code=status.HTTP_200_OK, tags=["Sources"])
async def update_source(id: int, data: schemas.SourceUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.source.update_source(id, data, db)

@router.delete(path="/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Sources"])
async def delete_source(id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return await crud.source.delete_source(id, db)

