from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.discount import DiscountRequest, DiscountResponse
from app.cruds.discount import create_discount, get_discount, get_discounts, update_discount, delete_discount
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/discounts/", response_model=DiscountResponse)
def create_new_discount(discount: DiscountRequest, db: Session = Depends(get_db)):
    return create_discount(db, discount)

@router.get("/discounts/{discount_id}", response_model=DiscountResponse)
def read_discount(discount_id: int, db: Session = Depends(get_db)):
    return get_discount(db, discount_id)

@router.get("/discounts/", response_model=list[DiscountResponse])
def read_discounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_discounts(db, skip, limit)

@router.put("/discounts/{discount_id}", response_model=bool)
def update_existing_discount(discount_id: int, discount: DiscountRequest, db: Session = Depends(get_db)):
    return update_discount(db, discount_id, discount)

@router.delete("/discounts/{discount_id}", response_model=bool)
def delete_existing_discount(discount_id: int, db: Session = Depends(get_db)):
    return delete_discount(db, discount_id)