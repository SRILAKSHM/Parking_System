import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Feedback_Request(Base):
    __tablename__ = 'user_feedback'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default=lambda: str(uuid.uuid4()))
    feedback = Column(String(100), nullable=False)  
    entry_time = Column(DateTime, default=datetime.now())

    
   
    