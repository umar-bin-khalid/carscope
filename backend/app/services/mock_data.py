"""
Mock inventory — same shape as normalized Marketcheck listings.
Used as a fallback when the Marketcheck API is unavailable, slow, or rate-limited.
"""

from app.models.car import Car

MOCK_LISTINGS: list[Car] = [
    Car(id="mock-1", make="Toyota", model="Camry", trim="SE", year=2022, price=27495,
        mileage=18200, location="Los Angeles, CA",
        description="2022 Toyota Camry SE — clean title, one owner",
        vin="4T1B11HK5NU123456", source="mock", listing_url=None),
    Car(id="mock-2", make="Toyota", model="RAV4", trim="XLE", year=2023, price=34900,
        mileage=9100, location="San Diego, CA",
        description="2023 Toyota RAV4 XLE AWD — nearly new",
        vin="2T3P1RFV4PW234567", source="mock", listing_url=None),
    Car(id="mock-3", make="Toyota", model="Corolla", trim="LE", year=2021, price=19800,
        mileage=31000, location="Phoenix, AZ",
        description="2021 Toyota Corolla LE — fuel efficient daily driver",
        vin="5YFEPRAE5MP345678", source="mock", listing_url=None),
    Car(id="mock-4", make="Honda", model="Civic", trim="Sport", year=2022, price=24200,
        mileage=21500, location="San Jose, CA",
        description="2022 Honda Civic Sport — sporty compact, no accidents",
        vin="2HGFE2F58NH456789", source="mock", listing_url=None),
    Car(id="mock-5", make="Honda", model="Accord", trim="EX-L", year=2021, price=31500,
        mileage=28000, location="Sacramento, CA",
        description="2021 Honda Accord EX-L — sunroof, heated seats",
        vin="1HGCV1F35MA567890", source="mock", listing_url=None),
    Car(id="mock-6", make="Honda", model="CR-V", trim="AWD EX", year=2022, price=33000,
        mileage=15700, location="Portland, OR",
        description="2022 Honda CR-V AWD EX — great family SUV",
        vin="7FARW2H89NE678901", source="mock", listing_url=None),
    Car(id="mock-7", make="BMW", model="3 Series", trim="330i", year=2021, price=41000,
        mileage=29000, location="New York, NY",
        description="2021 BMW 330i xDrive — M Sport package, premium audio",
        vin="WBA5R7C08MFH23456", source="mock", listing_url=None),
    Car(id="mock-8", make="BMW", model="5 Series", trim="530i", year=2022, price=54900,
        mileage=17000, location="Miami, FL",
        description="2022 BMW 530i — executive sedan, panoramic roof",
        vin="WBA13BJ04NCF34567", source="mock", listing_url=None),
    Car(id="mock-9", make="BMW", model="X5", trim="xDrive40i", year=2021, price=62000,
        mileage=33000, location="Chicago, IL",
        description="2021 BMW X5 xDrive40i — 3rd row, HK sound",
        vin="5UXCR6C08M9D45678", source="mock", listing_url=None),
    Car(id="mock-10", make="BMW", model="X3", trim="xDrive30i", year=2023, price=51000,
        mileage=6200, location="Boston, MA",
        description="2023 BMW X3 xDrive30i — nearly new, full warranty",
        vin="5UX53DP05P9E56789", source="mock", listing_url=None),
    Car(id="mock-11", make="Ford", model="F-150", trim="XLT", year=2022, price=42500,
        mileage=22000, location="Dallas, TX",
        description="2022 Ford F-150 XLT — 4WD, tow package",
        vin="1FTEW1EP5NFA67890", source="mock", listing_url=None),
    Car(id="mock-12", make="Ford", model="Mustang", trim="GT", year=2021, price=44000,
        mileage=14000, location="Houston, TX",
        description="2021 Ford Mustang GT — 5.0L V8, manual, fastback",
        vin="1FA6P8CF5M5123456", source="mock", listing_url=None),
    Car(id="mock-13", make="Ford", model="Explorer", trim="XLT", year=2022, price=40000,
        mileage=19000, location="Atlanta, GA",
        description="2022 Ford Explorer XLT — 3-row SUV, 4WD",
        vin="1FMSK8DH7NGA78901", source="mock", listing_url=None),
    Car(id="mock-14", make="Tesla", model="Model 3", trim="Long Range", year=2023, price=46500,
        mileage=8000, location="San Francisco, CA",
        description="2023 Tesla Model 3 Long Range AWD — autopilot, 358mi range",
        vin="5YJ3E1EA5PF890123", source="mock", listing_url=None),
    Car(id="mock-15", make="Tesla", model="Model Y", trim="Long Range", year=2022, price=54000,
        mileage=11000, location="Austin, TX",
        description="2022 Tesla Model Y Long Range — 7-seat, FSD capable",
        vin="7SAYGDEE5NF901234", source="mock", listing_url=None),
    Car(id="mock-16", make="Chevrolet", model="Silverado", trim="LT", year=2021, price=39000,
        mileage=37000, location="Detroit, MI",
        description="2021 Chevrolet Silverado LT — 4WD, tow/haul mode",
        vin="3GCUYBEF5MG012345", source="mock", listing_url=None),
    Car(id="mock-17", make="Chevrolet", model="Equinox", trim="LT AWD", year=2022, price=29500,
        mileage=24000, location="Columbus, OH",
        description="2022 Chevrolet Equinox LT AWD — remote start, heated seats",
        vin="2GNAXUEV5N6123456", source="mock", listing_url=None),
    Car(id="mock-18", make="Mercedes-Benz", model="C-Class", trim="C300", year=2022, price=52000,
        mileage=14000, location="Washington, DC",
        description="2022 Mercedes-Benz C300 4MATIC — AMG Line, Burmester audio",
        vin="W1KWF8EB5NR234567", source="mock", listing_url=None),
    Car(id="mock-19", make="Mercedes-Benz", model="GLC", trim="GLC300", year=2021, price=55000,
        mileage=26000, location="Seattle, WA",
        description="2021 Mercedes-Benz GLC 300 4MATIC — premium package",
        vin="W1N0G8EB5MF345678", source="mock", listing_url=None),
    Car(id="mock-20", make="Audi", model="A4", trim="Premium Plus", year=2022, price=43000,
        mileage=18000, location="Denver, CO",
        description="2022 Audi A4 Premium Plus quattro — virtual cockpit",
        vin="WAUENAF43NA456789", source="mock", listing_url=None),
    Car(id="mock-21", make="Audi", model="Q5", trim="Premium", year=2021, price=45500,
        mileage=27000, location="Nashville, TN",
        description="2021 Audi Q5 Premium quattro — panoramic sunroof",
        vin="WA1ANAFY5M2567890", source="mock", listing_url=None),
    Car(id="mock-22", make="Hyundai", model="Tucson", trim="SEL", year=2022, price=28900,
        mileage=20000, location="Minneapolis, MN",
        description="2022 Hyundai Tucson SEL AWD — great value compact SUV",
        vin="5NMP3DAJ5NH678901", source="mock", listing_url=None),
    Car(id="mock-23", make="Hyundai", model="Elantra", trim="SEL", year=2023, price=22500,
        mileage=8500, location="Charlotte, NC",
        description="2023 Hyundai Elantra SEL — nearly new, fuel efficient",
        vin="KMHLS4AG7PU789012", source="mock", listing_url=None),
    Car(id="mock-24", make="Kia", model="Telluride", trim="EX", year=2022, price=44000,
        mileage=16000, location="Phoenix, AZ",
        description="2022 Kia Telluride EX — 3-row SUV, top safety pick",
        vin="5XYP5DHC0NG890123", source="mock", listing_url=None),
    Car(id="mock-25", make="Kia", model="Sportage", trim="EX", year=2023, price=31000,
        mileage=7200, location="San Antonio, TX",
        description="2023 Kia Sportage EX AWD — redesigned, loaded",
        vin="KNDPUCAF8P7901234", source="mock", listing_url=None),
]


def filter_mock(
    listings: list[Car],
    make: str | None = None,
    model: str | None = None,
    year: int | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    mileage_max: int | None = None,
) -> list[Car]:
    """Apply the same filter parameters used by the Marketcheck proxy."""
    results = listings
    if make:
        results = [c for c in results if c.make.lower() == make.lower()]
    if model:
        results = [c for c in results if c.model.lower() == model.lower()]
    if year:
        results = [c for c in results if c.year == year]
    if price_min is not None:
        results = [c for c in results if c.price >= price_min]
    if price_max is not None:
        results = [c for c in results if c.price <= price_max]
    if mileage_max is not None:
        results = [c for c in results if c.mileage <= mileage_max]
    return results
