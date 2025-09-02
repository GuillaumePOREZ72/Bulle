from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Time, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Routine(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False) # Routine du matin, "Routine de la journée", "Routine de la soirée"
    description = Column(Text)
    icon = Column(String) # URL de l'image de l'icône
    color = Column(String, default="#A7D8F0")
    start_time = Column(Time) #Heure de début 
    estimated_duration = Column(Integer) # Durée estimée en minutes
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relations
    steps = relationship("RoutineStep", back_populates="routine", order_by="RoutineStep.order_index")
    completions = relationship("RoutineCompletion", back_populates="routine")


class RoutineStep(Base):
    __tablename__ = "routine_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("routines.id"), nullable=False)
    title = Column(String, nullable=False)  # "Se brosser les dents"
    description = Column(Text)  # Instructions détaillées et claires
    image_url = Column(String)  # Photo explicative
    estimated_time = Column(Integer, default=5)  # Temps en minutes (max 10 min par étape)
    order_index = Column(Integer, nullable=False)  # Ordre dans la routine
    points_value = Column(Integer, default=5)
    is_required = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    routine = relationship("Routine", back_populates="steps")