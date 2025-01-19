from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.sizes import SizeRequest, SizeResponse
from app.cruds.sizes import create_size, get_size, get_sizes, update_size, delete_size
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sizes/", response_model=SizeResponse)
def create_new_size(size: SizeRequest, db: Session = Depends(get_db)):
    return create_size(db, size)

@router.get("/sizes/{size_id}", response_model=SizeResponse)
def read_size(size_id: int, db: Session = Depends(get_db)):
    return get_size(db, size_id)

@router.get("/sizes/", response_model=list[SizeResponse])
def read_sizes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_sizes(db, skip, limit)

@router.put("/sizes/{size_id}", response_model=bool)
def update_existing_size(size_id: int, size: SizeRequest, db: Session = Depends(get_db)):
    return update_size(db, size_id, size)

@router.delete("/sizes/{size_id}", response_model=bool)
def delete_existing_size(size_id: int, db: Session = Depends(get_db)):
    return delete_size(db, size_id)