from fastapi import APIRouter, Query
from typing import List, Optional
from app.models.car import Car
from app.services.car_service import car_service

router = APIRouter(prefix="/api/cars", tags=["cars"])


@router.get("/", response_model=List[Car])
async def get_cars(
    make: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    year_min: Optional[int] = Query(None),
    year_max: Optional[int] = Query(None),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    mileage_max: Optional[int] = Query(None),
    location: Optional[str] = Query(None),
):
    """Get all cars with optional filters"""
    if any([make, model, year_min, year_max, price_min, price_max, mileage_max, location]):
        return car_service.search_cars(
            make=make,
            model=model,
            year_min=year_min,
            year_max=year_max,
            price_min=price_min,
            price_max=price_max,
            mileage_max=mileage_max,
            location=location,
        )
    return car_service.get_all_cars()


@router.get("/{car_id}", response_model=Car)
async def get_car(car_id: int):
    """Get a specific car by ID"""
    car = car_service.get_car(car_id)
    if not car:
        return {"error": "Car not found"}
    return car
