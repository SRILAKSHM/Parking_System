import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, UniqueConstraint
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Parking_Data(Base):
    __tablename__ = 'Parking_data'
    
    id = Column(Integer, primary_key=True, index=True)
    plot = Column(String, nullable=False)
    slot = Column(String, nullable=False)
    occupied = Column(Boolean, nullable=False, default=False)
    booked_by = Column(String, nullable=True)
    entry_time = Column(DateTime, default=datetime.now)
    
    __table_args__ = (UniqueConstraint('plot', 'slot', name='unique_plot_slot'),)
   
    