from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class CallCreate(BaseModel):
    receiver_id: int
    type: str 


class CallUpdate(BaseModel):
    status: str   
    ended_at: datetime | None = None


class CallResponse(BaseModel):
    id: int
    caller: UserShort
    receiver: UserShort
    type: str
    status: str
    started_at: datetime | None
    ended_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True