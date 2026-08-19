from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class StoryView(Base):
    __tablename__ = "story_views"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    viewed_at = Column(DateTime, server_default=func.now())