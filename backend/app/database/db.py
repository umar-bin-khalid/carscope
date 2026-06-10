from typing import List, Optional, Dict, Any
from app.models.car import Car, CarCreate


class InMemoryDB:
    """Simple in-memory database for cars"""
    
    def __init__(self):
        self.cars: Dict[int, Car] = {}
        self.next_id = 1
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample car data"""
        sample_cars = [
            # Toyota
            {
                "make": "Toyota",
                "model": "Camry",
                "year": 2022,
                "price": 28000,
                "mileage": 15000,
                "location": "San Francisco, CA",
                "description": "Well-maintained sedan with great fuel economy",
            },
            {
                "make": "Toyota",
                "model": "RAV4",
                "year": 2021,
                "price": 32000,
                "mileage": 28000,
                "location": "Seattle, WA",
                "description": "Popular SUV, AWD, excellent condition",
            },
            {
                "make": "Toyota",
                "model": "Corolla",
                "year": 2020,
                "price": 19500,
                "mileage": 41000,
                "location": "Phoenix, AZ",
                "description": "Fuel-efficient compact, one owner",
            },
            # Honda
            {
                "make": "Honda",
                "model": "Civic",
                "year": 2021,
                "price": 24000,
                "mileage": 22000,
                "location": "Los Angeles, CA",
                "description": "Reliable compact car, excellent condition",
            },
            {
                "make": "Honda",
                "model": "Accord",
                "year": 2022,
                "price": 31000,
                "mileage": 12000,
                "location": "Chicago, IL",
                "description": "Mid-size sedan with Honda Sensing suite",
            },
            {
                "make": "Honda",
                "model": "CR-V",
                "year": 2020,
                "price": 27500,
                "mileage": 35000,
                "location": "Dallas, TX",
                "description": "Compact SUV, great cargo space",
            },
            # BMW
            {
                "make": "BMW",
                "model": "3 Series",
                "year": 2019,
                "price": 38000,
                "mileage": 62000,
                "location": "New York, NY",
                "description": "Luxury sedan with premium features",
            },
            {
                "make": "BMW",
                "model": "5 Series",
                "year": 2021,
                "price": 52000,
                "mileage": 19000,
                "location": "Miami, FL",
                "description": "Executive sedan, loaded with options",
            },
            {
                "make": "BMW",
                "model": "X5",
                "year": 2020,
                "price": 61000,
                "mileage": 33000,
                "location": "Boston, MA",
                "description": "Luxury SUV, xDrive40i, panoramic roof",
            },
            {
                "make": "BMW",
                "model": "X3",
                "year": 2022,
                "price": 47000,
                "mileage": 10000,
                "location": "Atlanta, GA",
                "description": "Compact luxury SUV, nearly new",
            },
            # Ford
            {
                "make": "Ford",
                "model": "F-150",
                "year": 2020,
                "price": 35000,
                "mileage": 45000,
                "location": "Denver, CO",
                "description": "Pickup truck, perfect for work or adventure",
            },
            {
                "make": "Ford",
                "model": "Mustang",
                "year": 2021,
                "price": 42000,
                "mileage": 18000,
                "location": "Houston, TX",
                "description": "GT fastback, 5.0L V8, manual transmission",
            },
            {
                "make": "Ford",
                "model": "Explorer",
                "year": 2022,
                "price": 39000,
                "mileage": 22000,
                "location": "Minneapolis, MN",
                "description": "3-row SUV, great for families",
            },
            # Tesla
            {
                "make": "Tesla",
                "model": "Model 3",
                "year": 2023,
                "price": 45000,
                "mileage": 5000,
                "location": "San Jose, CA",
                "description": "Electric vehicle with autopilot features",
            },
            {
                "make": "Tesla",
                "model": "Model Y",
                "year": 2022,
                "price": 54000,
                "mileage": 14000,
                "location": "Austin, TX",
                "description": "Long Range AWD, 330 mile range",
            },
            # Chevrolet
            {
                "make": "Chevrolet",
                "model": "Silverado",
                "year": 2021,
                "price": 40000,
                "mileage": 38000,
                "location": "Detroit, MI",
                "description": "Full-size truck, LT trim, tow package",
            },
            {
                "make": "Chevrolet",
                "model": "Equinox",
                "year": 2020,
                "price": 22000,
                "mileage": 47000,
                "location": "Columbus, OH",
                "description": "Compact SUV, great value for money",
            },
            # Mercedes-Benz
            {
                "make": "Mercedes-Benz",
                "model": "C-Class",
                "year": 2021,
                "price": 48000,
                "mileage": 21000,
                "location": "San Diego, CA",
                "description": "C300 4MATIC, AMG Line package",
            },
            {
                "make": "Mercedes-Benz",
                "model": "GLC",
                "year": 2022,
                "price": 57000,
                "mileage": 9000,
                "location": "Washington, DC",
                "description": "Luxury compact SUV, Burmester audio",
            },
            # Audi
            {
                "make": "Audi",
                "model": "A4",
                "year": 2020,
                "price": 36000,
                "mileage": 29000,
                "location": "Portland, OR",
                "description": "Premium sedan, quattro AWD, S-line trim",
            },
            {
                "make": "Audi",
                "model": "Q5",
                "year": 2021,
                "price": 44000,
                "mileage": 25000,
                "location": "Nashville, TN",
                "description": "Luxury compact SUV, virtual cockpit",
            },
        ]
        
        for car_data in sample_cars:
            self.add_car(CarCreate(**car_data))
    
    def add_car(self, car: CarCreate) -> Car:
        """Add a new car to the database"""
        car_obj = Car(id=self.next_id, source="local", **car.dict())
        self.cars[self.next_id] = car_obj
        self.next_id += 1
        return car_obj
    
    def get_car(self, car_id: int) -> Optional[Car]:
        """Get a car by ID"""
        return self.cars.get(car_id)
    
    def get_all_cars(self) -> List[Car]:
        """Get all cars"""
        return list(self.cars.values())
    
    def search_cars(
        self,
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
        results = list(self.cars.values())
        
        if make:
            results = [c for c in results if c.make.lower() == make.lower()]
        if model:
            results = [c for c in results if c.model.lower() == model.lower()]
        if year_min:
            results = [c for c in results if c.year >= year_min]
        if year_max:
            results = [c for c in results if c.year <= year_max]
        if price_min:
            results = [c for c in results if c.price >= price_min]
        if price_max:
            results = [c for c in results if c.price <= price_max]
        if mileage_max:
            results = [c for c in results if c.mileage <= mileage_max]
        if location:
            results = [c for c in results if location.lower() in c.location.lower()]
        
        return results


# Global database instance
db = InMemoryDB()
