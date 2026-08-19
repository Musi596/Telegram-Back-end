from pydantic import BaseModel
from datetime import datetime
from users.schemas import UserShort


class StoryCreate(BaseModel):
    url: str
    type: str  


class StoryResponse(BaseModel):
    id: int
    user: UserShort
    url: str
    type: str
    expires_at: datetime
    views_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True