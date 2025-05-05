from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ParkingSlotsData(BaseModel):
    plot: str
    booked_by: Optional[str] = None
    occupied: Optional[bool] = False
    entry_time: Optional[datetime] = None
    slot: List[str]

    class Config:
        orm_mode = True
    
class UserData(BaseModel):
    username: str
    user_id: Optional[str] = None
    password: str 
    role: str
    login_time : Optional[datetime] = None
    
class LoginRequest(BaseModel):
    username: str
    password: str
    user_id: Optional[str] = None

class BookSlot(BaseModel):
    user_id: Optional[str] = None
    occupied: Optional[bool] = True
    entry_time: Optional[datetime] = None
    slot: List[str]
    plot: str
    class Config:
        orm_mode = True
        
class FeedbackData(BaseModel):
    user_id: Optional[str] = None
    feedback: str
    entry_time: Optional[datetime] = None