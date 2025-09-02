from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
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
    notes = Column(Text)

    # Relations
    routine = relationship("Routine", back_populates="completions")

class StepCompletion(Base):
    __tablename__ = "step_completions"

    id = Column(Integer, primary_key=True, index=True)
    routine_completion_id = Column(Integer, ForeignKey("routine_completions.id"), nullable=True)
    step_id = Column(Integer, ForeignKey("routine_steps.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    time_taken = Column(Integer)

    