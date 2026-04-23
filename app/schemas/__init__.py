"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Vehicle Schemas
class VehicleBase(BaseModel):
    """Base vehicle schema"""

    brand: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1900, le=2100)
    fuel_type: str = Field(..., max_length=50)
    body_type: str = Field(..., max_length=50)
    description: Optional[str] = None


class VehicleCreate(VehicleBase):
    """Schema for creating vehicle"""

    pass


class VehicleUpdate(BaseModel):
    """Schema for updating vehicle"""

    description: Optional[str] = None


class VehicleResponse(VehicleBase):
    """Schema for vehicle response"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Price Schemas
class VehiclePriceBase(BaseModel):
    """Base price schema"""

    price: float = Field(..., gt=0)
    currency: str = "BRL"
    source: str = Field(..., max_length=50)
    market_type: str = Field(..., max_length=50)
    recorded_at: datetime


class VehiclePriceCreate(VehiclePriceBase):
    """Schema for creating vehicle price"""

    vehicle_id: int


class VehiclePriceResponse(VehiclePriceBase):
    """Schema for price response"""

    id: int
    vehicle_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PriceHistoryResponse(BaseModel):
    """Price history with statistics"""

    vehicle_id: int
    latest_price: float
    avg_price: float
    min_price: float
    max_price: float
    total_records: int
    date_range: dict  # {start, end}
    prices: List[VehiclePriceResponse]

    class Config:
        from_attributes = True


# Safety Rating Schemas
class SafetyRatingBase(BaseModel):
    """Base safety rating schema"""

    organization: str = Field(..., max_length=100)
    overall_score: float = Field(..., ge=0, le=5)
    frontal_crash: Optional[float] = None
    side_crash: Optional[float] = None
    rollover: Optional[float] = None
    child_protection: Optional[float] = None
    pedestrian_protection: Optional[float] = None
    url: Optional[str] = None


class SafetyRatingCreate(SafetyRatingBase):
    """Schema for creating safety rating"""

    vehicle_id: int


class SafetyRatingResponse(SafetyRatingBase):
    """Schema for safety rating response"""

    id: int
    vehicle_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Reliability Index Schemas
class ReliabilityIndexBase(BaseModel):
    """Base reliability index schema"""

    score: float = Field(..., ge=0, le=10)
    breakdown_frequency: Optional[float] = None
    customer_satisfaction: Optional[float] = None
    warranty_claims_rate: Optional[float] = None
    repair_cost_index: Optional[float] = None
    data_source: str = Field(..., max_length=100)


class ReliabilityIndexCreate(ReliabilityIndexBase):
    """Schema for creating reliability index"""

    vehicle_id: int


class ReliabilityIndexResponse(ReliabilityIndexBase):
    """Schema for reliability index response"""

    id: int
    vehicle_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Composite Schemas
class VehicleDetailResponse(VehicleResponse):
    """Vehicle with all related data"""

    prices: Optional[List[VehiclePriceResponse]] = None
    safety_ratings: Optional[List[SafetyRatingResponse]] = None
    reliability_index: Optional[ReliabilityIndexResponse] = None


class VehicleAnalyticsResponse(BaseModel):
    """Vehicle analytics summary"""

    vehicle: VehicleResponse
    price_summary: dict
    safety_summary: dict
    reliability_summary: dict
    last_updated: datetime


# Worker Schemas
class DataCollectionLogResponse(BaseModel):
    """Schema for data collection log"""

    id: int
    worker_name: str
    status: str
    start_time: datetime
    end_time: datetime
    items_processed: int
    items_failed: int
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Search/Filter Schemas
class VehicleSearchParams(BaseModel):
    """Parameters for vehicle search"""

    brand: Optional[str] = None
    model: Optional[str] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    fuel_type: Optional[str] = None
    body_type: Optional[str] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=1000)


class PriceRangeFilter(BaseModel):
    """Filter for price ranges"""

    min_price: Optional[float] = None
    max_price: Optional[float] = None
    currency: str = "BRL"
    market_type: Optional[str] = None
    source: Optional[str] = None


# Health Check
class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    version: str
    timestamp: datetime
    database: str
    workers: dict
