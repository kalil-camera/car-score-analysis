"""
API routes for vehicles and related data
"""
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Vehicle
from app.schemas import (
    VehicleCreate,
    VehicleResponse,
    VehicleUpdate,
    VehicleDetailResponse,
    VehicleSearchParams,
    VehiclePriceResponse,
    PriceHistoryResponse,
    SafetyRatingResponse,
    ReliabilityIndexResponse,
    PriceRangeFilter,
)
from app.services import VehicleService, PriceService, SafetyService, ReliabilityService

router = APIRouter(prefix="/api/v1/vehicles", tags=["vehicles"])


# Vehicle endpoints
@router.post("/", response_model=VehicleResponse, status_code=201)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
):
    """Create a new vehicle"""
    return VehicleService.create_vehicle(db, vehicle)


@router.get("/", response_model=List[VehicleResponse])
async def list_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List all vehicles with pagination"""
    return VehicleService.get_vehicles(db, skip=skip, limit=limit)


@router.get("/search", response_model=List[VehicleResponse])
async def search_vehicles(
    brand: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    year_from: Optional[int] = Query(None),
    year_to: Optional[int] = Query(None),
    fuel_type: Optional[str] = Query(None),
    body_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Search vehicles with filters"""
    params = VehicleSearchParams(
        brand=brand,
        model=model,
        year_from=year_from,
        year_to=year_to,
        fuel_type=fuel_type,
        body_type=body_type,
        skip=skip,
        limit=limit,
    )
    return VehicleService.search_vehicles(db, params)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
):
    """Get vehicle by ID"""
    vehicle = VehicleService.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.get("/{vehicle_id}/detail", response_model=VehicleDetailResponse)
async def get_vehicle_detail(
    vehicle_id: int,
    db: Session = Depends(get_db),
):
    """Get complete vehicle details with prices, safety, and reliability data"""
    vehicle = VehicleService.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.patch("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_update: VehicleUpdate,
    db: Session = Depends(get_db),
):
    """Update vehicle"""
    vehicle = VehicleService.update_vehicle(db, vehicle_id, vehicle_update)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.delete("/{vehicle_id}", status_code=204)
async def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
):
    """Delete vehicle"""
    deleted = VehicleService.delete_vehicle(db, vehicle_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vehicle not found")


# Price endpoints
@router.get("/{vehicle_id}/prices", response_model=PriceHistoryResponse)
async def get_price_history(
    vehicle_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    """Get price history for vehicle"""
    vehicle = VehicleService.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    prices = PriceService.get_price_history(db, vehicle_id, days=days)
    stats = PriceService.get_price_statistics(db, vehicle_id, days=days)

    return PriceHistoryResponse(
        vehicle_id=vehicle_id,
        prices=prices,
        date_range={
            "start": (datetime.utcnow() - timedelta(days=days)).isoformat(),
            "end": datetime.utcnow().isoformat(),
        },
        **stats,
    )


@router.post("/{vehicle_id}/prices", response_model=VehiclePriceResponse, status_code=201)
async def add_price(
    vehicle_id: int,
    price: float = Query(..., gt=0),
    currency: str = Query("BRL"),
    source: str = Query(...),
    market_type: str = Query(...),
    db: Session = Depends(get_db),
):
    """Add price record for vehicle"""
    vehicle = VehicleService.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return PriceService.add_price(
        db,
        vehicle_id=vehicle_id,
        price=price,
        currency=currency,
        source=source,
        market_type=market_type,
        recorded_at=datetime.utcnow(),
    )


@router.post("/search-by-price", response_model=List[dict])
async def search_by_price(
    filter_params: PriceRangeFilter,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Find vehicles within price range"""
    results = PriceService.filter_by_price_range(db, filter_params, limit=limit)
    return [
        {
            "vehicle": {
                "id": vehicle.id,
                "brand": vehicle.brand,
                "model": vehicle.model,
                "year": vehicle.year,
            },
            "price": price.price,
            "source": price.source,
            "market_type": price.market_type,
        }
        for vehicle, price in results
    ]


# Safety endpoints
@router.get("/{vehicle_id}/safety", response_model=List[SafetyRatingResponse])
async def get_safety_ratings(
    vehicle_id: int,
    db: Session = Depends(get_db),
):
    """Get all safety ratings for vehicle"""
    vehicle = VehicleService.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return SafetyService.get_ratings(db, vehicle_id)


@router.post("/{vehicle_id}/safety", response_model=SafetyRatingResponse, status_code=201)
async def add_safety_rating(
    vehicle_id: int,
    organization: str = Query(...),
    overall_score: float = Query(..., ge=0, le=5),
    frontal_crash: Optional[float] = Query(None),
    side_crash: Optional[float] = Query(None),
    rollover: Optional[float] = Query(None),
    child_protection: Optional[float] = Query(None),
    pedestrian_protection: Optional[float] = Query(None),
    url: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Add safety rating for vehicle"""
    vehicle = VehicleService.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return SafetyService.add_rating(
        db,
        vehicle_id=vehicle_id,
        organization=organization,
        overall_score=overall_score,
        frontal_crash=frontal_crash,
        side_crash=side_crash,
        rollover=rollover,
        child_protection=child_protection,
        pedestrian_protection=pedestrian_protection,
        url=url,
    )


# Reliability endpoints
@router.get("/{vehicle_id}/reliability", response_model=ReliabilityIndexResponse)
async def get_reliability_index(
    vehicle_id: int,
    db: Session = Depends(get_db),
):
    """Get reliability index for vehicle"""
    vehicle = VehicleService.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    reliability = ReliabilityService.get_reliability_index(db, vehicle_id)
    if not reliability:
        raise HTTPException(status_code=404, detail="Reliability index not found")

    return reliability


@router.post("/{vehicle_id}/reliability", response_model=ReliabilityIndexResponse, status_code=201)
async def set_reliability_index(
    vehicle_id: int,
    score: float = Query(..., ge=0, le=10),
    breakdown_frequency: Optional[float] = Query(None),
    customer_satisfaction: Optional[float] = Query(None),
    warranty_claims_rate: Optional[float] = Query(None),
    repair_cost_index: Optional[float] = Query(None),
    data_source: str = Query(...),
    db: Session = Depends(get_db),
):
    """Set or update reliability index"""
    vehicle = VehicleService.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return ReliabilityService.set_reliability_index(
        db,
        vehicle_id=vehicle_id,
        score=score,
        data_source=data_source,
        breakdown_frequency=breakdown_frequency,
        customer_satisfaction=customer_satisfaction,
        warranty_claims_rate=warranty_claims_rate,
        repair_cost_index=repair_cost_index,
    )
