from typing import List, Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class MonitorInfoBase(BaseModel):
    port_of_loading: str
    port_of_discharge: str
    container_detail: str
    monitor_time: str
    monitor_type: str
    email_status: bool
    is_active: bool


class MonitorInfoCreate(MonitorInfoBase):
    pass


class MonitorInfo(MonitorInfoBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True
