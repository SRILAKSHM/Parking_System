import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Booking_Data(Base):
    __tablename__ = 'user_booking_data'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default=lambda: str(uuid.uuid4()))
    occupied = Column(Boolean, nullable=True, default=False)
    entry_time = Column(DateTime, default=datetime.now)
    slot = Column(String, nullable=False)
    plot = Column(String, nullable=False)  
    

    
   
    