from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(
    prefix="/sources",
    tags=["Sources"],    
)


@router.get(
    path="/get/id/{id}",
    response_model=schemas.Source,
    responses = {
        status.HTTP_200_OK: {
            "description": "Successfully returned the source",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Source not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Source not found": {
                            "value": {"detail": "Source not found"}
                        }
                    }
                }
            },
        },
    },
)
async def get_source_by_id(id: int, db: Session = Depends(get_db)):
    """Returns source by id."""
    return await crud.source.get_source_by_id(id, db)


@router.get(
    path="/get/zipcode/{zipcode}",
    response_model=schemas.Source,
        responses = {
        status.HTTP_200_OK: {
            "description": "Successfully returned the source",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Source not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Source not found": {
                            "value": {"detail": "Source not found"}
                        }
                    }
                }
            },
        },
    },
)
async def get_source_by_zipcode(zipcode: str, db: Session = Depends(get_db)):
    """Returns source by zipcode."""
    return await crud.source.get_source_by_zipcode(zipcode, db)


@router.get(
    path="/get",
    response_model=schemas.Pagination[schemas.Source],
    responses = {
        status.HTTP_200_OK: {
            "description": "Successfully returned the sources",
        },
    },
)
async def get_sources(
    page: int = None,
    limit: int = None,
    source_state: str = None,
    source_city: str = None,
    source_address: str = None,
    source_zipcode: str = None,
    db: Session = Depends(get_db),
):
    """Returns sources with multiple search filters. In case you didn't provide page and limit for pagination, all data will be returned."""
    return await crud.source.get_sources(
        db, source_state, source_city, source_address, source_zipcode, page, limit
    )


@router.post(
    path="/create",
    response_model=schemas.Source,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully created the source",
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
async def create_source(
    data: schemas.SourceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Adds a new source to the database."""
    return await crud.source.create_source(data, db)


@router.put(
    path="/update/{id}",
    response_model=schemas.Source,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully updated the source",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Source not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Source not found": {
                            "value": {"detail": "Source not found"}
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
async def update_source(
    id: int,
    data: schemas.SourceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Updates source by id."""
    return await crud.source.update_source(id, data, db)


@router.delete(
    path="/delete/{id}", 
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successfully deleted the source",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Source not found",
            "content": {
                "application/json": {
                    "examples": {
                        "Source not found": {
                            "value": {"detail": "Source not found"}
                        }
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "Source cannot be deleted because it is referenced by another table as a foreign key",
            "content": {
                "application/json": {
                    "examples": {
                        "Source cannot be deleted": {
                            "value": {"detail": "Deletion failed, this record is referenced by another table and cannot be removed"}
                        }
                    }
                }
            },
        },
    },
    tags=["Sources"]
)
async def delete_source(
    id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)
):
    """Deletes source by id."""
    return await crud.source.delete_source(id, db)
