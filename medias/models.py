from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Media(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    file_name = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())