import os
from fastapi import APIRouter  
from fastapi import HTTPException, Depends
from app.models import schemas
import jwt
import datetime
from fastapi import APIRouter
from app.models import schemas, user_model
from app.database import engine, SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
router = APIRouter()  

from dotenv import load_dotenv
import os

load_dotenv()  
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)  # Default 1 hour expiry

    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

user_model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@router.post("/login", tags=["Login"]) 
async def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = db.query(user_model.User_Data).filter(user_model.User_Data.username == request.username).first()
    if not user or not pwd_context.verify(request.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    user_id = user.user_id
    payload = {
        "username": user.username,  
        "role": user.role,
        "user_id": user_id     
    }
    
    access_token = create_access_token(
        data=payload,
        expires_delta=datetime.timedelta(hours=1)  # Token expires in 1 hour
    )
    
    return {"access_token": access_token, "token_type": "bearer"}