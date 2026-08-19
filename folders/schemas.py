from pydantic import BaseModel
from datetime import datetime


class FolderCreate(BaseModel):
    name: str


class FolderUpdate(BaseModel):
    name: str


class FolderResponse(BaseModel):
    id: int
    user_id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True