from pydantic import BaseModel

class ColorRequest(BaseModel):
    value: str

class ColorResponse(BaseModel):
    id: int
    value: str

    class Config:
        orm_mode = True