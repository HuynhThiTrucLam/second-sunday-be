from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str


class CategoryResponse(CategoryBase):
    id: int


class CategoryRequest(CategoryBase):
    pass
