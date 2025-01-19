from pydantic import BaseModel, condecimal
from datetime import datetime

class FeedbackRequest(BaseModel):
    account_id: int
    product_id: int
    rating: condecimal(max_digits=2, decimal_places=1, ge=1.0, le=5.0) = ...
    content: str
    reply_content: str

class FeedbackResponse(BaseModel):
    id: int
    create_at: datetime
    account_id: int
    product_id: int
    rating: condecimal(max_digits=2, decimal_places=1, ge=1.0, le=5.0) = ...
    content: str
    reply_content: str

    class Config:
        orm_mode = True