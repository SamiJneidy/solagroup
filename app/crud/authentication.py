import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from .user import get_user_by_username
from ..core.config import settings
from ..core import exceptions
from .. import schemas, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/authorize")
pwd_context = CryptContext(schemes=["bcrypt"])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def validate_access_token(token: str) -> None:
    try:
        payload: dict = jwt.decode(jwt=token, key=settings.secret_key, algorithms=[settings.algorithm])
        username = payload["username"]
        if not username:
            raise exceptions.InvalidToken()
    except jwt.InvalidTokenError:
        raise exceptions.InvalidToken()

async def create_access_token(payload: schemas.TokenPayload) -> str:
    payload.iat = datetime.now(tz=timezone.utc)
    payload.exp = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(payload.model_dump(), settings.secret_key, settings.algorithm)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = schemas.TokenPayload(**jwt.decode(token, settings.secret_key, [settings.algorithm]))
        return payload.username
    except jwt.InvalidTokenError:
        raise exceptions.InvalidToken()

async def signup(data: schemas.UserCreate, db: Session) -> schemas.UserGet:
    try:
        data.password = hash_password(data.password)
        inserted_user: models.User = db.execute(insert(models.User).values(**data.model_dump()).returning(models.User)).scalars().first()
        db.commit()
        return schemas.UserGet.model_validate(inserted_user)
    except IntegrityError:
        db.rollback()
        raise exceptions.ResourceAlreadyInUse(resource="Username")

async def login(login_credentials: schemas.LoginCredentials, db: Session) -> schemas.LoginResponse:
    user: schemas.User = await get_user_by_username(login_credentials.username, db=db)
    if not verify_password(login_credentials.password, user.password):
        raise exceptions.InvalidCredentials()
    payload = schemas.TokenPayload(username=user.username)
    access_token = await create_access_token(payload)
    return schemas.LoginResponse(username=user.username, token=access_token)

async def swaggerUI_login(login_credentials: OAuth2PasswordRequestForm, db: Session):
    user: schemas.User = await get_user_by_username(login_credentials.username, db=db)
    if not verify_password(login_credentials.password, user.password):
        raise exceptions.InvalidCredentials()
    payload = schemas.TokenPayload(username=user.username)
    access_token = await create_access_token(payload)
    return {"access_token": access_token, "token_type": "bearer"}
