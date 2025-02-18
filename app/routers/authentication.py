from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud import authentication
from ..crud.authentication import get_current_user, OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth")

@router.post(path="/login", response_model=schemas.LoginResponse, status_code=status.HTTP_200_OK, tags=["Authentication"])
async def login(login_credentials: schemas.LoginCredentials, db: Session = Depends(get_db)):
    return await authentication.login(login_credentials, db)

@router.post(path="/signup", response_model=schemas.UserGet, status_code=status.HTTP_200_OK, tags=["Authentication"])
async def signup(data: schemas.UserCreate, db: Session = Depends(get_db)):
    return await authentication.signup(data, db)

@router.post(path="/authorize", status_code=status.HTTP_200_OK, tags=["Authentication"])
async def authorize(login_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await authentication.swaggerUI_login(login_credentials, db)