from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date
from sqlalchemy.sql import func
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True)
    avatar_url = Column(String)
    points = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    birth_date = Column(Date)
    favorite_color = Column(String, default="#A7D8F0")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())