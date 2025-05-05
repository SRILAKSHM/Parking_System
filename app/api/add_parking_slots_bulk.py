from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from typing import List
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


@router.post('/add_parking_slots_bulk')
@verify_token(allowed_roles=["admin"])
def add_parking_slots_bulk(request: Request, park_slots: List[schemas.ParkingSlotsData], db: Session = Depends(get_db)):
    incoming_data = park_slots  

    if not incoming_data:
        raise HTTPException(status_code=400, detail="No plot/slot data provided.")

    created_plots = set()
    created_slots = []
    existing_slots = []

    for plot_data in incoming_data:
        plot_name = plot_data.plot
        slot_list = plot_data.slot

        if not slot_list:
            continue

        
        plot_exists = db.query(parking_data_model.Parking_Data).filter(
            parking_data_model.Parking_Data.plot == plot_name
        ).first()

        if not plot_exists:
            created_plots.add(plot_name)

        existing_slot_records = db.query(parking_data_model.Parking_Data.slot).filter(
            parking_data_model.Parking_Data.plot == plot_name
        ).all()

        existing_slot_names = {record.slot for record in existing_slot_records}

        new_slots = set(slot_list) - existing_slot_names

        for slot_name in new_slots:
            new_slot = parking_data_model.Parking_Data(
                plot=plot_name,
                slot=slot_name,
                booked_by=plot_data.booked_by,
                occupied=plot_data.occupied,
                entry_time=plot_data.entry_time or datetime.now()
            )
            db.add(new_slot)
            created_slots.append({"plot": plot_name, "slot": slot_name})

        if not new_slots and existing_slot_names:
            existing_slots.extend([{"plot": plot_name, "slot": slot} for slot in existing_slot_names])

    db.commit()

    response = {}
    if created_plots:
        response["created_plots"] = list(created_plots)
    if created_slots:
        response["created_slots"] = created_slots
    if existing_slots:
        response["existing_slots"] = existing_slots

    return response
