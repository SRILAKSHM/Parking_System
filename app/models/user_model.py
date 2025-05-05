import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class User_Data(Base):
    __tablename__ = 'user_data'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String) 
    role = Column(String)
    login_time = Column(DateTime, default=datetime.now())