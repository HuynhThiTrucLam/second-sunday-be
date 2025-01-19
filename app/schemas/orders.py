from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class OrderDetailRequest(BaseModel):
    product_variant_id: int
    count: int

class OrderRequest(BaseModel):
    account_id: int
    ship_amount: int
    discount_id: Optional[int]
    status: Optional[str]
    order_details: List[OrderDetailRequest]

class OrderDetailResponse(BaseModel):
    id: int
    order_id: int
    product_variant_id: int
    count: int

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    account_id: int
    create_at: datetime
    confirm_at: Optional[datetime]
    ship_amount: int
    discount_id: Optional[int]
    status: str
    order_details: List[OrderDetailResponse]
    customer: Optional[str]

    class Config:
        orm_mode = True