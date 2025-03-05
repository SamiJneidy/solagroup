from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(
    prefix="/destinations",
    tags=["Destinations"],
)


@router.get(
    path="/get/id/{id}",
    response_model=schemas.Destination,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully returned the destination",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Destination not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Destination not found": {
                            "value": {"detail": "Destination not found"}
                        }
                    }
                }
            },
        },
    },
)
async def get_destination_by_id(id: int, db: Session = Depends(get_db)):
    """Returns destination by id."""
    return await crud.destination.get_destination_by_id(id, db)


@router.get(
    path="/get",
    response_model=schemas.Pagination[schemas.Destination],
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully returned the destinations",
        },
    },
)
async def get_destinations(
    page: int = None,
    limit: int = None,
    country: str = None,
    port: str = None,
    db: Session = Depends(get_db),
):
    """Returns destinations with multiple search filters. In case you didn't provide page and limit for pagination, all data will be returned."""
    return await crud.destination.get_destinations(db, country, port, page, limit)


@router.post(
    path="/create",
    response_model=schemas.Destination,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully created the destination",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Duplicate entry: The specified country and port combination already exists. Please use a different combination",
            "content": {
                "application/json": {
                    "examples": {
                        "Destination already in use": {
                            "value": {"detail": "Destination already in use"}
                        }
                    }
                }
            }
        },
    },
)
async def create_destination(
    data: schemas.DestinationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Adds a new destination to the database."""
    return await crud.destination.create_destination(data, db)


@router.put(
    path="/update/{id}",
    response_model=schemas.Destination,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully updated the destination",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Destination not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Destination not found": {
                            "value": {"detail": "Destination not found"}
                        }
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Duplicate entry: The specified country and port combination already exists. Please use a different combination",
            "content": {
                "application/json": {
                    "examples": {
                        "Destination already in use": {
                            "value": {"detail": "Destination already in use"}
                        }
                    }
                }
            }
        },
    },
)
async def update_destination(
    id: int,
    data: schemas.DestinationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Updates destination by id."""
    return await crud.destination.update_destination(id, data, db)


@router.delete(
    path="/delete/{id}", 
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successfully deleted the destination",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Destination not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Destination not found": {
                            "value": {"detail": "Destination not found"}
                        }
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Destination cannot be deleted because it is referenced by another table as a foreign key",
            "content": {
                "application/json": {
                    "examples": {
                        "Destination cannot be deleted": {
                            "value": {"detail": "Deletion failed, this record is referenced by another table and cannot be removed"}
                        }
                    }
                }
            },
        },
    },
    tags=["Destinations"]
)
async def delete_destination(
    id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)
):
    """Deletes a destination by id."""
    return await crud.destination.delete_destination(id, db)
