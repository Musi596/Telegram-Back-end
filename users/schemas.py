from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    phone: str
    password: str
    username: str | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    full_name: str | None = None
    bio: str | None = None
    photo: str | None = None


class UserResponse(BaseModel):
    id: int
    phone: str
    username: str | None
    full_name: str | None
    bio: str | None
    photo: str | None
    is_verified: bool
    is_bot: bool
    last_seen: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


class UserShort(BaseModel):
    id: int
    username: str | None
    full_name: str | None
    photo: str | None
    is_verified: bool
    is_bot: bool

    class Config:
        from_attributes = True