from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.orders import OrderRequest, OrderResponse
from app.cruds.orders import create_order, get_order, get_orders, update_order, delete_order
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/orders/", response_model=bool)
def create_new_order(order: OrderRequest, db: Session = Depends(get_db)):
    return create_order(db, order)

@router.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    return get_order(db, order_id)

@router.get("/orders", response_model=list[OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, type: str="ALL", db: Session = Depends(get_db)):
    return get_orders(type, db, skip, limit)

@router.put("/orders/{order_id}", response_model=bool)
def update_existing_order(order_id: int, order: OrderRequest, db: Session = Depends(get_db)):
    return update_order(db, order_id, order)

@router.delete("/orders/{order_id}", response_model=bool)
def delete_existing_order(order_id: int, db: Session = Depends(get_db)):
    return delete_order(db, order_id)