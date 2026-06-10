import os
import httpx
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from app.models.car import Car
from app.services.mock_data import MOCK_LISTINGS, filter_mock

router = APIRouter(prefix="/api/marketcheck", tags=["marketcheck"])

MARKETCHECK_BASE_URL = "https://mc-api.marketcheck.com/v2"


def _get_api_key() -> str:
    api_key = os.getenv("MARKETCHECK_API_KEY", "")
    if not api_key or api_key == "your_marketcheck_api_key_here":
        raise HTTPException(status_code=503, detail="Marketcheck API key not configured. Set MARKETCHECK_API_KEY in .env")
    return api_key


def _normalize_listing(listing: dict) -> Car:
    """Normalize a Marketcheck listing to the unified Car model"""
    build = listing.get("build") or {}
    dealer = listing.get("dealer") or {}
    media = listing.get("media") or {}
    photos = media.get("photo_links") or []

    city = dealer.get("city", "")
    state = dealer.get("state", "")
    location_parts = [p for p in [city, state] if p]
    location = ", ".join(location_parts) or "Unknown"

    trim = build.get("trim") or ""
    heading = listing.get("heading") or (
        f"{build.get('year', '')} {build.get('make', '')} {build.get('model', '')} {trim}".strip()
    )

    return Car(
        id=listing.get("id", ""),
        make=build.get("make") or "Unknown",
        model=build.get("model") or "Unknown",
        year=build.get("year") or 0,
        price=listing.get("price") or 0,
        mileage=listing.get("miles") or 0,
        location=location,
        description=heading,
        image_url=photos[0] if photos else None,
        source="marketcheck",
        listing_url=listing.get("vdp_url"),
        vin=listing.get("vin"),
        trim=trim or None,
    )


@router.get("/search")
async def search_active_inventory(
    make: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    mileage_max: Optional[int] = Query(None),
    zip_code: Optional[str] = Query(None, alias="zip"),
    radius: Optional[int] = Query(100),
    car_type: Optional[str] = Query("used"),
    start: int = Query(0),
    rows: int = Query(20),
):
    """
    Proxy for Marketcheck active inventory search.
    Maps to: GET /v2/search/car/active
    Falls back to mock data on any failure (missing key, timeout, 429, 5xx, etc.)
    """
    api_key = os.getenv("MARKETCHECK_API_KEY", "")
    use_mock = False

    # Try live API if key is configured
    if api_key and api_key != "your_marketcheck_api_key_here":
        try:
            params: dict = {"api_key": api_key, "start": start, "rows": min(rows, 50)}

            if make:
                params["make"] = make
            if model:
                params["model"] = model
            if year:
                params["year"] = year
            if price_min is not None or price_max is not None:
                low = int(price_min) if price_min is not None else 0
                high = int(price_max) if price_max is not None else 9999999
                params["price_range"] = f"{low}:{high}"
            if mileage_max is not None:
                params["miles_range"] = f"0:{mileage_max}"
            if zip_code:
                params["zip"] = zip_code
                params["radius"] = radius
            if car_type:
                params["car_type"] = car_type

            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(
                    f"{MARKETCHECK_BASE_URL}/search/car/active",
                    params=params,
                )
                resp.raise_for_status()

            data = resp.json()
            listings = data.get("listings") or []
            normalized = [_normalize_listing(listing) for listing in listings]

            return JSONResponse(
                {
                    "num_found": data.get("num_found", 0),
                    "listings": [car.model_dump() for car in normalized],
                },
                headers={"X-Data-Source": "marketcheck-live"}
            )
        except Exception:
            # Any error → fall back to mock (rate limit, timeout, network error, parse error, etc.)
            use_mock = True

    # Fallback to mock data
    if use_mock or not api_key or api_key == "your_marketcheck_api_key_here":
        filtered = filter_mock(
            MOCK_LISTINGS,
            make=make,
            model=model,
            year=year,
            price_min=price_min,
            price_max=price_max,
            mileage_max=mileage_max,
        )
        return JSONResponse(
            {
                "num_found": len(MOCK_LISTINGS),
                "listings": [car.model_dump() for car in filtered],
            },
            headers={"X-Data-Source": "mock"}
        )


@router.get("/listing/{listing_id}", response_model=Car)
async def get_listing_detail(listing_id: str):
    """
    Proxy for Marketcheck listing detail.
    Maps to: GET /v2/listing/car/{listing_id}
    """
    api_key = _get_api_key()

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(
                f"{MARKETCHECK_BASE_URL}/listing/car/{listing_id}",
                params={"api_key": api_key},
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Marketcheck error: {exc.response.text[:300]}",
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Could not reach Marketcheck API: {exc}")

    return _normalize_listing(resp.json())
