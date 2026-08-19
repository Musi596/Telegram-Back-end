from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Pin(Base):
    __tablename__ = "pins"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    pinned_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    pinned_at = Column(DateTime, server_default=func.now())