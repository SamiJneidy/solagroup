from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/warehouses")


@router.get(path="/get/id/{id}", response_model=schemas.Warehouse, status_code=status.HTTP_200_OK, tags=["Warehouses"])
async def get_warehouse_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.warehouse.get_warehouse_by_id(id, db)

@router.get(path="/get/zipcode/{zipcode}", response_model=schemas.Warehouse, status_code=status.HTTP_200_OK, tags=["Warehouses"])
async def get_warehouse_by_zipcode(zipcode: str, db: Session = Depends(get_db)):
    return await crud.warehouse.get_warehouse_by_zipcode(zipcode, db)

@router.get(path="/get", response_model=schemas.Pagination[schemas.Warehouse], status_code=status.HTTP_200_OK, tags=["Warehouses"])
async def get_warehouses(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return await crud.warehouse.get_warehouses(db, page, limit)

@router.post(path="/create", response_model=schemas.Warehouse, status_code=status.HTTP_200_OK, tags=["Warehouses"])
async def create_warehouse(data: schemas.WarehouseCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.warehouse.create_warehouse(data, db)

@router.put(path="/update/{id}", response_model=schemas.Warehouse, status_code=status.HTTP_200_OK, tags=["Warehouses"])
async def update_warehouse(id: int, data: schemas.WarehouseUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.warehouse.update_warehouse(id, data, db)

@router.delete(path="/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Warehouses"])
async def delete_warehouse(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.warehouse.delete_warehouse(id, db)

