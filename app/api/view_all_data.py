from fastapi import APIRouter, Request
from app.models import schemas, parking_data_model, user_model
from app.database import engine, SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.utils.token_helper import verify_token
  
router = APIRouter()
parking_data_model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        
@router.get('/view_all_slots')
@verify_token(allowed_roles=["admin","user"])
def view_parking_data(request: Request, db: Session = Depends(get_db)):
    data =  db.query(parking_data_model.Parking_Data).all()
    return data

