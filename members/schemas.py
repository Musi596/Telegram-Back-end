from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class MemberCreate(BaseModel):
    user_id: int


class MemberUpdate(BaseModel):
    role: str | None = None       
    can_send: bool | None = None
    can_add_members: bool | None = None
    can_pin: bool | None = None


class MemberResponse(BaseModel):
    id: int
    user: UserShort
    role: str
    can_send: bool
    can_add_members: bool
    can_pin: bool
    joined_at: datetime

    class Config:
        from_attributes = True