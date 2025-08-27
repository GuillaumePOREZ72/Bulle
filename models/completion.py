from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.sql import func
from core.database import Base

class RoutineCompletion(Base):
    __tablename__ = "routine_completions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    routine_id = Column(Integer, ForeignKey("routines.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    points_earned = Column(Integer, default=0)
    all_steps_completed = Column(Boolean, default=False)

    