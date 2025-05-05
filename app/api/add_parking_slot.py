from fastapi import APIRouter, Request
from datetime import datetime
from fastapi import Request, HTTPException
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
        
@router.post('/add_parking_slot')
@verify_token(allowed_roles=["admin"])
def add_parking_data(request: Request, park_slot: schemas.ParkingSlotsData, db: Session = Depends(get_db)):
    created_plot = None
    created_slots = []
    existing_slots = []

    # Check if plot exists (based on the plot name)
    plot_exists = db.query(parking_data_model.Parking_Data).filter(
        parking_data_model.Parking_Data.plot == park_slot.plot
    ).first()

    # If plot doesn't exist, create it
    if not plot_exists:
        created_plot = park_slot.plot

    # Fetch existing slots in the given plot
    existing_slot_records = db.query(parking_data_model.Parking_Data.slot).filter(
        parking_data_model.Parking_Data.plot == park_slot.plot
    ).all()

    # Store existing slots in the plot
    existing_slots = [record.slot for record in existing_slot_records]

    # Add slots to the existing or new plot
    for slot_name in park_slot.slot:
        # Check if this slot already exists in the given plot
        existing_slot = db.query(parking_data_model.Parking_Data).filter(
            parking_data_model.Parking_Data.plot == park_slot.plot,
            parking_data_model.Parking_Data.slot == slot_name
        ).first()

        # If slot doesn't exist, create a new slot
        if not existing_slot:
            new_slot = parking_data_model.Parking_Data(
                plot=park_slot.plot,
                slot=slot_name,
                booked_by=park_slot.booked_by,
                occupied=park_slot.occupied,
                entry_time=park_slot.entry_time or datetime.now()  # Use current time if entry_time is not provided
            )
            db.add(new_slot)
            created_slots.append(slot_name)

    db.commit()

    # Prepare the response
    response = {}
    if created_plot:
        response["created_plot"] = created_plot
    if created_slots:
        response["created_slots"] = created_slots
    if not created_slots and existing_slots:
        response["existing_slots"] = existing_slots

    return response
