from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"],
)


@router.get(
    path="/get/id/{id}",
    response_model=schemas.Warehouse,
    responses = {
        status.HTTP_200_OK: {
            "description": "Successfully returned the warehouse",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Warehouse not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Warehouse not found": {
                            "value": {"detail": "Warehouse not found"}
                        }
                    }
                }
            },
        },
    },
)
async def get_warehouse_by_id(id: int, db: Session = Depends(get_db)):
    return await crud.warehouse.get_warehouse_by_id(id, db)


@router.get(
    path="/get/zipcode/{zipcode}",
    response_model=schemas.Warehouse,
    responses = {
        status.HTTP_200_OK: {
            "description": "Successfully returned the warehouse",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Warehouse not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Warehouse not found": {
                            "value": {"detail": "Warehouse not found"}
                        }
                    }
                }
            },
        },
    },
)
async def get_warehouse_by_zipcode(zipcode: str, db: Session = Depends(get_db)):
    return await crud.warehouse.get_warehouse_by_zipcode(zipcode, db)


@router.get(
    path="/get",
    response_model=schemas.Pagination[schemas.Warehouse],
    responses = {
        status.HTTP_200_OK: {
            "description": "Successfully returned the warehouses",
        },
    },
)
async def get_warehouses(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return await crud.warehouse.get_warehouses(db, page, limit)


@router.get(
    path="/get/order-by-cost",
    response_model=schemas.Pagination[schemas.Warehouse],
    responses = {
        status.HTTP_200_OK: {
            "description": "Successfully returned the warehouse",
        },
    },
)
async def get_warehouses_order_by_cost(
    page: int = 1,
    limit: int = 10,
    source_id: int = None,
    shipping_line_id: int = None,
    destination_country: str = None,
    destination_port: str = None,
    db: Session = Depends(get_db),
):
    return await crud.warehouse.get_warehouses_order_by_cost(
        db,
        source_id,
        shipping_line_id,
        destination_country,
        destination_port,
        page,
        limit,
    )


@router.post(
    path="/create",
    response_model=schemas.Warehouse,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully created the warehouse",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Zipcode already in use",
            "content": {
                "application/json": {
                    "examples": {
                        "Zipcode already in use": {
                            "value": {"detail": "Zipcode already in use"}
                        }
                    }
                }
            }
        },
    },
)
async def create_warehouse(
    data: schemas.WarehouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await crud.warehouse.create_warehouse(data, db)


@router.put(
    path="/update/{id}",
    response_model=schemas.Warehouse,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully updated the warehouse",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Warehouse not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Warehouse not found": {
                            "value": {"detail": "Warehouse not found"}
                        }
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Zipcode already in use",
            "content": {
                "application/json": {
                    "examples": {
                        "Zipcode already in use": {
                            "value": {"detail": "Zipcode already in use"}
                        }
                    }
                }
            }
        },
    },
)
async def update_warehouse(
    id: int,
    data: schemas.WarehouseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await crud.warehouse.update_warehouse(id, data, db)


@router.delete(
    path="/delete/{id}", 
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successfully deleted the warehouse",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Warehouse not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Warehouse not found": {
                            "value": {"detail": "Warehouse not found"}
                        }
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Warehouse cannot be deleted because it is referenced by another table as a foreign key",
            "content": {
                "application/json": {
                    "examples": {
                        "Warehouse cannot be deleted": {
                            "value": {"detail": "Deletion failed, this record is referenced by another table and cannot be removed"}
                        }
                    }
                }
            },
        },
    },
    tags=["Warehouses"]
)
async def delete_warehouse(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return await crud.warehouse.delete_warehouse(id, db)
