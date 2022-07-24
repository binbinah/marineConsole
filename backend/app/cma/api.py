from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter, Header, Response
from backend.config import MarineConfig
from backend.app.cma.service import MonitorService
from backend.app.cma import schemas, crud, models
from backend.database import engine, get_db

router = APIRouter()
models.Base.metadata.create_all(bind=engine)


@router.post("/monitor/create", response_model=schemas.MonitorInfo)
async def create_monitor_info(
    monitor_info: schemas.MonitorInfoCreate,
    db: crud.create_monitor_info_item = Depends(get_db),
    api_key: str = Header(...),
):
    marine_config = MarineConfig()
    if api_key != marine_config.config["API_KEY"]:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    monitor_service = MonitorService()
    if monitor_service.send_monitor_info_email(monitor_info):
        return crud.create_monitor_info_item(db, monitor_info)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----------------------------account--------------------------------


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(
        crud.fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    current_user: schemas.User = Depends(crud.get_current_active_user),
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: schemas.User = Depends(crud.get_current_active_user),
):
    return [{"item_id": "Foo", "owner": current_user.username}]
