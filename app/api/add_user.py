import uuid
from fastapi import APIRouter, Request, HTTPException
from app.models import schemas, user_model
from app.database import engine, SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.utils.token_helper import verify_token
  
router = APIRouter()
user_model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()


@router.post('/add_user')
def add_user_data(request: schemas.UserData, db: Session = Depends(get_db)):
    # Check if user already exists
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = db.query(user_model.User_Data).filter(user_model.User_Data.username == request.username).first()
    if request.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Role must be admin or user")

    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = pwd_context.hash(request.password)
    user_id = str(uuid.uuid4())

    # Create new user
    user_data = user_model.User_Data(
        username=request.username,
        password=hashed_password,
        user_id = user_id,
        role=request.role
    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    # Return safe fields only
    return {
        "username": user_data.username,
        "role": user_data.role,
        "user_id": user_id,
        "message": "User added successfully"
    }