from backend.app.cma import models, schemas
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Union
from backend.app.cma import schemas
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from backend.config import MarineConfig
from backend.database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/cma/v1/token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    config = MarineConfig()
    encoded_jwt = jwt.encode(
        to_encode, config.config["SECRET_KEY"], algorithm=config.config["ALGORITHM"]
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        config = MarineConfig()
        payload = jwt.decode(token, config.config["SECRET_KEY"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# -------------------------------------------------------------


def get_monitor_info_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MonitorInfo).offset(skip).limit(limit).all()


def get_monitor_info_by_item(
    db: Session, monitor_time: str, monitor_type: str, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.MonitorInfo)
        .filter(models.MonitorInfo.monitor_time == monitor_time)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_monitor_info_item(db: Session, item: schemas.MonitorInfoCreate):
    db_item = models.MonitorInfo(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


class MarineMonitorCRUD:
    def __init__(self):
        self.session = SessionLocal()

    def __del__(self):
        self.session.close()

    def get_monitor_info_by_item(self, monitor_time: str, monitor_type: str):
        return get_monitor_info_by_item(self.session, monitor_time, monitor_type)
