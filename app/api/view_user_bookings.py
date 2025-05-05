from fastapi import APIRouter, Request
from app.models import schemas, booking_slot_model
from app.database import engine, SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.utils.token_helper import verify_token
  
router = APIRouter()
booking_slot_model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        
@router.get('/view_user_bookings')
@verify_token(allowed_roles=["user"])
def view_parking_data(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    data = db.query(booking_slot_model.Booking_Data).filter(
        booking_slot_model.Booking_Data.user_id == user_id
    ).all()
    if data:
        return data
    return {"message": "No bookings made"}

