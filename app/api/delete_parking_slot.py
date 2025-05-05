from fastapi import APIRouter, Request, HTTPException
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
        
@router.post('/delete_parking_slot')
@verify_token(allowed_roles=["admin"])
def delete_parking_slot(request: Request, park_slots: schemas.ParkingSlotsData, db: Session = Depends(get_db)):
    deleted_slots = []
    failed_slots = []

    # 1. Iterate through each slot in the list of slots
    for slot_name in park_slots.slot:
        # 2. Check if the plot exists
        plot_exists = db.query(parking_data_model.Parking_Data).filter(
            parking_data_model.Parking_Data.plot == park_slots.plot
        ).first()

        if not plot_exists:
            failed_slots.append(f"Plot '{park_slots.plot}' not found")
            continue

        # 3. Check if the slot exists inside that plot
        existing_slot = db.query(parking_data_model.Parking_Data).filter(
            parking_data_model.Parking_Data.plot == park_slots.plot,
            parking_data_model.Parking_Data.slot == slot_name
        ).first()

        if not existing_slot:
            failed_slots.append(f"Slot '{slot_name}' not found in plot '{park_slots.plot}'")
            continue

        # 4. Check if the slot is already vacant
        if not existing_slot.occupied:
            failed_slots.append(f"Slot '{slot_name}' in plot '{park_slots.plot}' is already vacant")
            continue

        # 5. Delete the slot if it's occupied
        db.delete(existing_slot)
        db.commit()

        deleted_slots.append(f"Slot '{slot_name}' in plot '{park_slots.plot}' deleted successfully")

    # Prepare response with failed and deleted slots
    return {
        "message": "Slot deletion operation completed",
        "failed_slots": failed_slots,
        "deleted_slots": deleted_slots
    }
