from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class FolderChat(Base):
    __tablename__ = "folder_chats"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    added_at = Column(DateTime, server_default=func.now())