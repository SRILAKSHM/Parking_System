import uuid
from fastapi import APIRouter, Request, HTTPException
from app.models import schemas, parking_data_model, booking_slot_model
from app.database import engine, SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.utils.token_helper import verify_token
  
router = APIRouter()
parking_data_model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        
@router.post('/cancel_slot')
@verify_token(allowed_roles=["user"])
def cancel_parking_data(request: Request, park_slots: schemas.BookSlot, db: Session = Depends(get_db)):
    failed_slots = []
    cancelled_slots = []

    # 1. Iterate through each slot in the list of slots
    for slot_name in park_slots.slot:
        # Check if the plot exists
        plot = db.query(parking_data_model.Parking_Data).filter(
            parking_data_model.Parking_Data.plot == park_slots.plot
        ).first()

        if not plot:
            failed_slots.append(f"Plot '{park_slots.plot}' does not exist")
            continue

        # 2. Check if the slot exists inside that plot
        existing_slot = db.query(parking_data_model.Parking_Data).filter(
            parking_data_model.Parking_Data.slot == slot_name,
            parking_data_model.Parking_Data.plot == park_slots.plot
        ).first()

        if not existing_slot:
            failed_slots.append(f"Slot '{slot_name}' does not exist in plot '{park_slots.plot}'")
            continue

        # 3. Check if the slot is currently occupied
        if not existing_slot.occupied:
            failed_slots.append(f"Slot '{slot_name}' in plot '{park_slots.plot}' is not booked (already vacant)")
            continue

        # 4. Mark the slot as free and update the booking details
        existing_slot.occupied = False
        existing_slot.booked_by = None
        db.commit()
        db.refresh(existing_slot)

        # 5. Update or remove the entry in the Booking_Data table
        booking_record = db.query(booking_slot_model.Booking_Data).filter(
            booking_slot_model.Booking_Data.slot == slot_name,
            booking_slot_model.Booking_Data.plot == park_slots.plot
        ).first()

        if booking_record:
            booking_record.occupied = False
            booking_record.user_id = None
            booking_record.entry_time = datetime.now()
            db.commit()
            db.refresh(booking_record)

        cancelled_slots.append(f"Slot '{slot_name}' in plot '{park_slots.plot}' has been cancelled")

    # If any slots were not found or are already vacant, raise an exception
    if failed_slots:
        raise HTTPException(status_code=400, detail={
            "message": "Cancellation failed for some slots",
            "failed_slots": failed_slots
        })

    # Return the successful cancellations if no errors
    return {
        "message": "Bulk cancellation operation completed successfully",
        "cancelled_slots": cancelled_slots
    }
