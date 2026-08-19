from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class ContactCreate(BaseModel):
    contact_id: int
    name: str | None = None


class ContactResponse(BaseModel):
    id: int
    user: UserShort
    name: str | None
    created_at: datetime

    class Config:
        from_attributes = True
        