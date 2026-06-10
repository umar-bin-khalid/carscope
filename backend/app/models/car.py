from pydantic import BaseModel
from typing import Optional, Union


class Car(BaseModel):
    id: Union[int, str]
    make: str
    model: str
    year: int
    price: float
    mileage: int
    location: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    source: Optional[str] = "local"       # "local" or "marketcheck"
    listing_url: Optional[str] = None     # Marketcheck VDP URL
    vin: Optional[str] = None             # Vehicle Identification Number
    trim: Optional[str] = None            # e.g., "SE", "Sport"


class CarCreate(BaseModel):
    make: str
    model: str
    year: int
    price: float
    mileage: int
    location: str
    description: Optional[str] = None
    image_url: Optional[str] = None
