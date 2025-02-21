from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/shipping-lines")

@router.get(path="/get/id/{id}", response_model=schemas.ShippingLine, status_code=status.HTTP_200_OK, tags=["Shipping lines"])
async def get_shipping_line_by_id(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.shipping_line.get_shipping_line_by_id(id, db)

@router.get(path="/get", response_model=schemas.Pagination[schemas.ShippingLine], status_code=status.HTTP_200_OK, tags=["Shipping lines"])
async def get_shipping_line(page: int = 1, limit: int = 10, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.shipping_line.get_shipping_lines(db, page, limit)

@router.post(path="/create", response_model=schemas.ShippingLine, status_code=status.HTTP_200_OK, tags=["Shipping lines"])
async def create_shipping_line(data: schemas.ShippingLineCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.shipping_line.create_shipping_line(data, db)

@router.put(path="/update/{id}", response_model=schemas.ShippingLine, status_code=status.HTTP_200_OK, tags=["Shipping lines"])
async def update_shipping_line(id: int, data: schemas.ShippingLineUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.shipping_line.update_shipping_line(id, data, db)

@router.delete(path="/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Shipping lines"])
async def delete_shipping_line(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.shipping_line.delete_shipping_line(id, db)

