from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/maritime-transport")


@router.get(
    path="/get/id/{id}",
    response_model=schemas.MaritimeTransport,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully returned the maritime transport",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Maritime transport not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Maritime transport Not Found": {
                            "value": {"detail": "Maritime transport not found"}
                        }
                    }
                }
            },
        },
    },
    tags=["Maritime Transport"],
)
async def get_maritime_transport_by_id(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return await crud.maritime_transport.get_maritime_transport_by_id(id, db)


@router.get(
    path="/get",
    response_model=schemas.Pagination[schemas.MaritimeTransport],
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully returned the maritime transports",
        },
    },
    tags=["Maritime Transport"],
)
async def get_maritime_transports(
    page: int = 1,
    limit: int = 10,
    warehouse_id: int = None,
    shipping_line_id: int = None,
    destination_id: int = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await crud.maritime_transport.get_maritime_transports(
        db, warehouse_id, shipping_line_id, destination_id, page, limit
    )


@router.post(
    path="/create",
    response_model=schemas.MaritimeTransport,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully created the maritime transport",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Foreign key constraint violation",
            "content": {
                "application/json": {
                    "examples": {
                        "Data sent does not exist in the related table": {
                            "value": {"detail": "Foreign key constraint violation, the data sent does not exist in the related table"}
                        },
                        "Other violation reason": {
                            "value": {"detail": "Foreign key constraint violation"}
                        }
                    }
                }
            }
        },
        status.HTTP_409_CONFLICT: {
            "description": "Maritime transport already in use",
            "content": {
                "application/json": {
                    "examples": {
                        "Maritime transport already in use": {
                            "value": {"detail": "Maritime transport already in use"}
                        }
                    }
                }
            }
        },
    },
    tags=["Maritime Transport"],
)
async def create_maritime_transport(
    data: schemas.MaritimeTransportCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await crud.maritime_transport.create_maritime_transport(data, db)


@router.put(
    path="/update/{id}",
    response_model=schemas.MaritimeTransport,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully updated the maritime transport",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Foreign key constraint violation",
            "content": {
                "application/json": {
                    "examples": {
                        "Data sent does not exist in the related table": {
                            "value": {"detail": "Foreign key constraint violation, the data sent does not exist in the related table"}
                        },
                        "Other violation reason": {
                            "value": {"detail": "Foreign key constraint violation"}
                        }
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Maritime transport not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Maritime transport Not Found": {
                            "value": {"detail": "Maritime transport not found"}
                        }
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Maritime transport already in use",
            "content": {
                "application/json": {
                    "examples": {
                        "Maritime transport already in use": {
                            "value": {"detail": "Maritime transport already in use"}
                        }
                    }
                }
            }
        },
    },
    tags=["Maritime Transport"],
)
async def update_maritime_transport(
    id: int,
    data: schemas.MaritimeTransportUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await crud.maritime_transport.update_maritime_transport(id, data, db)


@router.delete(
    path="/delete/{id}",
    responses = {
        status.HTTP_204_NO_CONTENT: {
            "description": "Successfully deleted the maritime transport",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Maritime transport not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Maritime transport Not Found": {
                            "value": {"detail": "Maritime transport not found"}
                        }
                    }
                }
            },
        },
    },
    tags=["Maritime Transport"],
)
async def delete_maritime_transport(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return await crud.maritime_transport.delete_maritime_transport(id, db)
