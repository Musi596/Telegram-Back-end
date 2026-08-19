from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    phone_visibility = Column(String, default="contacts")
    photo_visibility = Column(String, default="everyone")
    who_can_message = Column(String, default="everyone")
    notifications = Column(Boolean, default=True)
    updated_at = Column(DateTime, server_default=func.now())