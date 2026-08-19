from pydantic import BaseModel
from datetime import datetime
from chats.schemas import ChatResponse


class FolderChatCreate(BaseModel):
    chat_id: int


class FolderChatResponse(BaseModel):
    id: int
    folder_id: int
    chat: ChatResponse
    added_at: datetime

    class Config:
        from_attributes = True
        