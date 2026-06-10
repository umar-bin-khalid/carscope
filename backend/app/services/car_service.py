from typing import List, Optional
from app.database.db import db
from app.models.car import Car


class CarService:
    """Service layer for car operations"""
    
    @staticmethod
    def get_all_cars() -> List[Car]:
        """Get all available cars"""
        return db.get_all_cars()
    
    @staticmethod
    def get_car(car_id: int) -> Optional[Car]:
        """Get a specific car by ID"""
        return db.get_car(car_id)
    
    @staticmethod
    def search_cars(
        make: Optional[str] = None,
        model: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        mileage_max: Optional[int] = None,
        location: Optional[str] = None,
    ) -> List[Car]:
        """Search cars with filters"""
        return db.search_cars(
            make=make,
            model=model,
            year_min=year_min,
            year_max=year_max,
            price_min=price_min,
            price_max=price_max,
            mileage_max=mileage_max,
            location=location,
        )


car_service = CarService()
