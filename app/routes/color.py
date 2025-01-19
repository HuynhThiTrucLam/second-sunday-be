from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.color import ColorRequest, ColorResponse
from app.cruds.color import create_color, get_color, get_colors, update_color, delete_color
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/colors/", response_model=ColorResponse)
def create_new_color(color: ColorRequest, db: Session = Depends(get_db)):
    return create_color(db, color)

@router.get("/colors/{color_id}", response_model=ColorResponse)
def read_color(color_id: int, db: Session = Depends(get_db)):
    db_color = get_color(db, color_id)
    if db_color is None:
        raise HTTPException(status_code=404, detail="Color not found")
    return db_color

@router.get("/colors/", response_model=list[ColorResponse])
def read_colors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_colors(db, skip, limit)

@router.put("/colors/{color_id}", response_model=bool)
def update_existing_color(color_id: int, color: ColorRequest, db: Session = Depends(get_db)):
    db_color = update_color(db, color_id, color)
    if db_color is None:
        raise HTTPException(status_code=404, detail="Color not found")
    return True

@router.delete("/colors/{color_id}", response_model=bool)
def delete_existing_color(color_id: int, db: Session = Depends(get_db)):
    db_color = delete_color(db, color_id)
    if db_color is None:
        raise HTTPException(status_code=404, detail="Color not found")
    return True