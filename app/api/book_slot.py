import uuid
from fastapi import APIRouter, Request
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
        
@router.post('/book_slot')
@verify_token(allowed_roles=["user"])
def add_parking_data(request: Request, park_slots: schemas.BookSlot, db: Session = Depends(get_db)):
    created_slots = []
    failed_slots = []

    for slot_name in park_slots.slot:
        plot_exists = db.query(parking_data_model.Parking_Data).filter(
            parking_data_model.Parking_Data.plot == park_slots.plot
        ).first()

        if not plot_exists:
            failed_slots.append(f"Plot '{park_slots.plot}' does not exist")
            continue

        slot_record = db.query(parking_data_model.Parking_Data).filter(
            parking_data_model.Parking_Data.plot == park_slots.plot,
            parking_data_model.Parking_Data.slot == slot_name
        ).first()

        if not slot_record:
            failed_slots.append(f"Slot '{slot_name}' does not exist in plot '{park_slots.plot}'")
            continue

        if slot_record.occupied:
            failed_slots.append(f"Slot '{slot_name}' in plot '{park_slots.plot}' is already booked")
            continue

        slot_record.occupied = True
        slot_record.booked_by = request.state.user_id
        slot_record.entry_time = datetime.now()
        db.commit()
        db.refresh(slot_record)

        booking_record = db.query(booking_slot_model.Booking_Data).filter(
            booking_slot_model.Booking_Data.plot == park_slots.plot,
            booking_slot_model.Booking_Data.slot == slot_name
        ).first()

        if booking_record:
            booking_record.user_id = request.state.user_id
            booking_record.occupied = True
            booking_record.entry_time = datetime.now()
            db.commit()
            db.refresh(booking_record)
        else:
            new_booking = booking_slot_model.Booking_Data(
                user_id=request.state.user_id,
                slot=slot_name,
                plot=park_slots.plot,
                occupied=True,
                entry_time=datetime.now()
            )
            db.add(new_booking)
            db.commit()
            db.refresh(new_booking)

        created_slots.append(f"Slot '{slot_name}' in plot '{park_slots.plot}' booked successfully")

    if not created_slots and failed_slots:
        return {"message": "No slots were booked", "failed_slots": failed_slots}
    
    if created_slots and not failed_slots:
        return {"message": "All slots booked successfully", "created_slots": created_slots}
    
    if created_slots and failed_slots:
        return {
            "message": "Some slots were successfully booked, others failed",
            "created_slots": created_slots,
            "failed_slots": failed_slots
        }

    return {"message": "No action taken, something went wrong."}
