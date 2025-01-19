from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.feedbacks import FeedbackRequest, FeedbackResponse
from app.cruds.feedbacks import create_feedback, get_feedback, get_feedbacks, update_feedback, delete_feedback
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/feedbacks/", response_model=FeedbackResponse)
def create_new_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    return create_feedback(db, feedback)

@router.get("/feedbacks/{feedback_id}", response_model=FeedbackResponse)
def read_feedback(feedback_id: int, db: Session = Depends(get_db)):
    return get_feedback(db, feedback_id)

@router.get("/feedbacks/", response_model=list[FeedbackResponse])
def read_feedbacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_feedbacks(db, skip, limit)

@router.put("/feedbacks/{feedback_id}", response_model=bool)
def update_existing_feedback(feedback_id: int, feedback: FeedbackRequest, db: Session = Depends(get_db)):
    return update_feedback(db, feedback_id, feedback)

@router.delete("/feedbacks/{feedback_id}", response_model=bool)
def delete_existing_feedback(feedback_id: int, db: Session = Depends(get_db)):
    return delete_feedback(db, feedback_id)