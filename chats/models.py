from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=False)
    username = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now())