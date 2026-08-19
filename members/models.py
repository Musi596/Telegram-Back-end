from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, default="member")
    can_send = Column(Boolean, default=True)
    can_add_members = Column(Boolean, default=False)
    can_pin = Column(Boolean, default=False)
    joined_at = Column(DateTime, server_default=func.now())