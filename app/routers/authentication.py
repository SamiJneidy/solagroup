from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud import authentication
from ..crud.authentication import get_current_user, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    path="/login", 
    response_model=schemas.LoginResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Logged in successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Username not found or Invalid credentials",
            "content": {
                "application/json": {
                    "examples": {
                        "Username not found": {
                            "value": {"detail": "Username not found"}
                        },
                        "Invalid credentials": {
                            "value": {"detail": "Invalid credentials"}
                        }
                    }
                }
            }
        }
    },
)
async def login(login_credentials: schemas.LoginCredentials, db: Session = Depends(get_db)):
    """Used by admins to login to the dashboard"""
    return await authentication.login(login_credentials, db)

@router.post(
    path="/signup", 
    response_model=schemas.UserGet, 
    responses={
        status.HTTP_200_OK: {
            "description": "Signed up successfully",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Username already in use",
            "content": {
                "application/json": {
                    "examples": {
                        "Username already in use": {
                            "value": {"detail": "Username already in use"}
                        }
                    }
                }
            }
        }
    },
)
async def signup(data: schemas.UserCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Used for adding a new admin to the dashboard"""
    return await authentication.signup(data, db)

@router.post(
    path="/authorize", 
    responses={
        status.HTTP_200_OK: {
            "description": "Logged in successfully",
        },
    },
)
async def authorize(login_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """For SwaggerUI authentication"""
    return await authentication.swaggerUI_login(login_credentials, db)