from pydantic import BaseModel
from datetime import datetime


class BotCreate(BaseModel):
    name: str
    username: str
    description: str | None = None


class BotResponse(BaseModel):
    id: int
    user_id: int
    name: str
    username: str
    token: str
    description: str | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BotShort(BaseModel):
    id: int
    name: str
    username: str
    is_active: bool

    class Config:
        from_attributes = True