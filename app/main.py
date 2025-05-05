from fastapi import FastAPI  
from app.api import (add_parking_slot, health, add_user, login, view_all_data, update_parking_slot, delete_parking_slot, book_slot, view_user_bookings
,cancel_booking, create_user_feedback, update_user_feedback, view_all_feedback, add_parking_slots_bulk)
from app.api import health
app = FastAPI()  

app.include_router(health.router , prefix="/api/Parking_System")  
app.include_router(login.router , prefix="/api/Parking_System")
app.include_router(add_parking_slot.router , prefix="/api/Parking_System") 
app.include_router(add_user.router , prefix="/api/Parking_System")   
app.include_router(view_all_data.router , prefix="/api/Parking_System")
app.include_router(update_parking_slot.router , prefix="/api/Parking_System")
app.include_router(delete_parking_slot.router , prefix="/api/Parking_System")
app.include_router(book_slot.router , prefix="/api/Parking_System")
app.include_router(view_user_bookings.router , prefix="/api/Parking_System")
app.include_router(cancel_booking.router , prefix="/api/Parking_System")
app.include_router(create_user_feedback.router , prefix="/api/Parking_System")
app.include_router(update_user_feedback.router , prefix="/api/Parking_System")
app.include_router(view_all_feedback.router , prefix="/api/Parking_System")
app.include_router(add_parking_slots_bulk.router, prefix="/api/Parking_System")