from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
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
        
@router.post('/update_parking_slot')
@verify_token(allowed_roles=["admin"])
def update_parking_slot(request: Request, park_slot: schemas.ParkingSlotsData, db: Session = Depends(get_db)):
    updated_slots = []
    not_found_slots = []

    for slot_name in park_slot.slot:
        existing_slot = db.query(parking_data_model.Parking_Data).filter(
            parking_data_model.Parking_Data.slot == slot_name,
            parking_data_model.Parking_Data.plot == park_slot.plot
        ).first()

        if not existing_slot:
            not_found_slots.append(slot_name)
        else:
            existing_slot.occupied = park_slot.occupied
            existing_slot.entry_time = datetime.now()
            updated_slots.append(slot_name)

    if not updated_slots:
        # No slots were updated at all
        raise HTTPException(
            status_code=404,
            detail=f"No matching plot '{park_slot.plot}' or slots {park_slot.slot} found."
        )

    db.commit()

    # Prepare success response
    response = {
        "message": "Slots updated successfully.",
        "updated_slots": updated_slots
    }
    if not_found_slots:
        response["not_found_slots"] = not_found_slots

    return response
