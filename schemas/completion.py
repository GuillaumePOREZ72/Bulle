from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RoutineCompletionResponse(BaseModel):
    id: int
    user_id: int
    routine_id: int
    completed_at: datetime
    points_earned: int
    all_steps_completed: bool
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

class StepCompletionCreate(BaseModel):
    step_id: int
    time_taken: Optional[int] = None

class StepCompletionResponse(BaseModel):
    id: int
    step_id: int
    completed_at: datetime
    time_taken: Optional[int] = None
    
    class Config:
        from_attributes = True