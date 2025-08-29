from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class UserBase(BaseModel):
    first_name: str
    username: str
    favorite_color: Otptional[str] = "#A7D8F0"

class UserCreate(UserBase):
    birth_date: Optional[date] = None

class UserResponse(UserBase):
    id: int
    points: int
    current_streak: int
    avatar_url: Optional[str] = None
    birth_date: Optional[date] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True