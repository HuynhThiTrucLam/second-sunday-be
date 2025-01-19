from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DiscountRequest(BaseModel):
    start_date: datetime
    hsd: int
    quantity: int
    description: str
    typof: str
    value: int
    code: str
    type: str

class DiscountResponse(BaseModel):
    id: int
    start_date: datetime
    hsd: int
    quantity: int
    description: str
    typof: str
    code: str
    type: Optional[str]
    value: int

    class Config:
        orm_mode = True