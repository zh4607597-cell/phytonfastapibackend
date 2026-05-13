from pydantic import BaseModel
from typing import Optional


class CityBase(BaseModel):
    city: str
    city_code: str


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    city: Optional[str] = None
    city_code: Optional[str] = None


class CityResponse(CityBase):
    id: int

    class Config:
        from_attributes = True
