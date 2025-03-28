from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(
    prefix="/shipping-lines",
    tags=["Shipping Lines"],
)


@router.get(
    path="/get/id/{id}",
    response_model=schemas.ShippingLine,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully returned the shipping line",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Shipping line not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Shipping line not found": {
                            "value": {"detail": "Shipping line not found"}
                        }
                    }
                }
            },
        },
    },
)
async def get_shipping_line_by_id(id: int, db: Session = Depends(get_db)):
    """Returns shipping line by id"""
    return await crud.shipping_line.get_shipping_line_by_id(id, db)


@router.get(
    path="/get",
    response_model=schemas.Pagination[schemas.ShippingLine],
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully returned the shipping lines",
        },
    },
)
async def get_shipping_lines(
    page: int = None, limit: int = None, db: Session = Depends(get_db)
):
    """Returns shipping lines with multiple search filters. In case you didn't provide page and limit for pagination, all data will be returned."""
    return await crud.shipping_line.get_shipping_lines(db, page, limit)


@router.post(
    path="/create",
    response_model=schemas.ShippingLine,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully created the shipping line",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Shipping line already in use",
            "content": {
                "application/json": {
                    "examples": {
                        "Shipping line already in use": {
                            "value": {"detail": "Shipping line already in use"}
                        }
                    }
                }
            }
        },
    },
)
async def create_shipping_line(
    data: schemas.ShippingLineCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Adds a new shipping line to the database."""
    return await crud.shipping_line.create_shipping_line(data, db)


@router.put(
    path="/update/{id}",
    response_model=schemas.ShippingLine,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully updated the shipping line",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Shipping line not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Shipping line not found": {
                            "value": {"detail": "Shipping line not found"}
                        }
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Shipping line already in use",
            "content": {
                "application/json": {
                    "examples": {
                        "Shipping line already in use": {
                            "value": {"detail": "Shipping line already in use"}
                        }
                    }
                }
            }
        },
    },
)
async def update_shipping_line(
    id: int,
    data: schemas.ShippingLineUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Updates shipping line by id."""
    return await crud.shipping_line.update_shipping_line(id, data, db)


@router.delete(
    path="/delete/{id}",  
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successfully deleted the shipping line",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Shipping line not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Shipping line not found": {
                            "value": {"detail": "Shipping line not found"}
                        }
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Shipping line cannot be deleted because it is referenced by another table as a foreign key",
            "content": {
                "application/json": {
                    "examples": {
                        "Shipping line cannot be deleted": {
                            "value": {"detail": "Deletion failed, this record is referenced by another table and cannot be removed"}
                        }
                    }
                }
            },
        },
    },
)
async def delete_shipping_line(
    id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)
):
    """Deletes shipping line by id."""
    return await crud.shipping_line.delete_shipping_line(id, db)
