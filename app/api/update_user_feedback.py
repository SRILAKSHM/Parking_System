import uuid
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
from app.models import schemas, user_model, feedback_model
from app.database import engine, SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.utils.token_helper import verify_token
  
router = APIRouter()
user_model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()


@router.post('/edit_feedback')
@verify_token(allowed_roles=["user"])
def add_user_data(request:  Request, user:schemas.FeedbackData, db: Session = Depends(get_db)):
    user_id = db.query(feedback_model.Feedback_Request).filter(feedback_model.Feedback_Request.user_id == request.state.user_id).first()
    if not user_id:
        raise HTTPException(status_code=400, detail="Feedback not given")

    user_id.feedback = user.feedback
    user_id.entry_time = datetime.now()

    db.add(user_id)
    db.commit()
    db.refresh(user_id)
    return {"message": "Feedback updated successfully"}