from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from sqlalchemy import tuple_
from app.models import schemas, parking_data_model
from app.database import engine, SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from app.utils.token_helper import verify_token
  
router = APIRouter()
parking_data_model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()


@router.post('/update_parking_slots_bulk')
@verify_token(allowed_roles=["admin"])
def update_parking_slots_bulk(request: Request, park_slots: List[schemas.ParkingSlotsData], db: Session = Depends(get_db)):
    if not park_slots:
        raise HTTPException(status_code=400, detail="No slots data provided for update.")

    incoming_updates = {}
    for item in park_slots:
        for slot_name in item.slot:
            incoming_updates[(slot_name, item.plot)] = item.occupied

    slot_plot_pairs = list(incoming_updates.keys())

    existing_slot_records = db.query(parking_data_model.Parking_Data).filter(
        tuple_(parking_data_model.Parking_Data.slot, parking_data_model.Parking_Data.plot).in_(slot_plot_pairs)
    ).all()

    updated_slots = []
    not_found_slots = []

    for record in existing_slot_records:
        key = (record.slot, record.plot)
        if key in incoming_updates:
            record.occupied = incoming_updates[key]
            record.entry_time = datetime.now()
            updated_slots.append({"slot": record.slot, "plot": record.plot})

    found_slot_plot_pairs = {(record.slot, record.plot) for record in existing_slot_records}
    not_found_pairs = set(slot_plot_pairs) - found_slot_plot_pairs

    not_found_slots = [{"slot": slot, "plot": plot} for slot, plot in not_found_pairs]

    if not updated_slots:
        raise HTTPException(
            status_code=404,
            detail=f"No matching slots/plots found for update: {not_found_slots}"
        )

    db.commit()

    return {
        "message": "Bulk update completed.",
        "updated_slots": updated_slots,
        "not_found_slots": not_found_slots
    }