from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional, List

class RoutineStepBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    estimated_time: int = 5
    order_index: int
    points_value: int = 5
    is_required: bool = True

class RoutineStepCreate(RoutineStepBase):
    pass

class RoutineStepResponse(RoutineStepBase):
    id: int
    routine_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RoutineBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: str = "#A7D8F0"
    start_time: Optional[time] = None
    estimated_time: Optional[int] = None

class RoutineCreate(RoutineBase):
    user_id: int
    steps: List[RoutineStepCreate] = []

class RoutineResponse(RoutineBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    steps: List[RoutineStepResponse] = []

    class Config:
        from_attributes = True

                