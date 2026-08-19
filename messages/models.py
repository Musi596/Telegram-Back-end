from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String, nullable=True)
    media_id = Column(Integer, ForeignKey("medias.id"), nullable=True)
    reply_to_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    forward_from_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    is_edited = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    edited_at = Column(DateTime, nullable=True)