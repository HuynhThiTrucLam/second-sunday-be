from pydantic import BaseModel

class SizeRequest(BaseModel):
    value: str

class SizeResponse(BaseModel):
    id: int
    value: str

    class Config:
        orm_mode = True