"""Application layer - DTOs"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ==== Vehicle DTOs ====
class CreateVehicleRequest(BaseModel):
    """Request DTO para criar vehicle"""
    brand: str
    model: str
    year: int
    fuel_type: str
    body_type: str
    description: Optional[str] = None


class UpdateVehicleRequest(BaseModel):
    """Request DTO para atualizar vehicle"""
    description: Optional[str] = None


class VehicleResponse(BaseModel):
    """Response DTO para vehicle"""
    id: int
    brand: str
    model: str
    year: int
    fuel_type: str
    body_type: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class VehicleDetailResponse(BaseModel):
    """Response DTO com detalhes completos"""
    vehicle: VehicleResponse
    prices: Optional[List['PriceRecordResponse']] = None
    safety_ratings: Optional[List['SafetyRatingResponse']] = None
    reliability: Optional['ReliabilityResponse'] = None


class SearchVehicleQuery(BaseModel):
    """Query DTO para busca avançada"""
    brand: Optional[str] = None
    model: Optional[str] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    fuel_type: Optional[str] = None
    body_type: Optional[str] = None
    skip: int = 0
    limit: int = 10


# ==== Price DTOs ====
class AddPriceRequest(BaseModel):
    """Request DTO para adicionar preço"""
    price: float = Field(gt=0)
    source: str
    market_type: str
    currency: Optional[str] = "BRL"


class PriceRecordResponse(BaseModel):
    """Response DTO para preço record"""
    amount: float
    currency: str
    source: str
    market_type: str
    recorded_at: datetime


class PriceStatisticsResponse(BaseModel):
    """Response DTO para estatísticas de preço"""
    count: int
    average: float
    min: float
    max: float


class PriceHistoryResponse(BaseModel):
    """Response DTO para histórico de preços"""
    vehicle_id: int
    records: List[PriceRecordResponse]
    statistics: PriceStatisticsResponse


class SearchByPriceQuery(BaseModel):
    """Query DTO para busca por preço"""
    min_price: float = Field(ge=0)
    max_price: float = Field(gt=0)
    currency: Optional[str] = "BRL"
    skip: int = 0
    limit: int = 10


# ==== Safety DTOs ====
class AddSafetyRatingRequest(BaseModel):
    """Request DTO para adicionar safety rating"""
    organization: str
    overall_score: float = Field(ge=0, le=5)
    frontal_crash: float = Field(ge=0, le=5)
    side_crash: float = Field(ge=0, le=5)
    rollover: float = Field(ge=0, le=5)
    child_protection: float = Field(ge=0, le=5)
    pedestrian_protection: float = Field(ge=0, le=5)


class SafetyRatingResponse(BaseModel):
    """Response DTO para safety rating"""
    organization: str
    overall_score: float
    frontal_crash: float
    side_crash: float
    rollover: float
    child_protection: float
    pedestrian_protection: float
    created_at: datetime


class SafetyProfileResponse(BaseModel):
    """Response DTO para safety profile"""
    vehicle_id: int
    ratings: List[SafetyRatingResponse]
    average_score: float


# ==== Reliability DTOs ====
class UpdateReliabilityRequest(BaseModel):
    """Request DTO para atualizar reliability"""
    overall_score: float = Field(ge=0, le=100)
    breakdown_frequency: float = Field(ge=0)
    customer_satisfaction: float = Field(ge=0, le=100)
    warranty_claims_rate: float = Field(ge=0, le=100)
    warranty_avg_cost: float = Field(ge=0)


class WarrantyInfoResponse(BaseModel):
    """Response DTO para warranty info"""
    claims_rate: float
    avg_cost: float


class ReliabilityResponse(BaseModel):
    """Response DTO para reliability"""
    vehicle_id: int
    overall_score: float
    breakdown_frequency: float
    customer_satisfaction: float
    warranty_info: WarrantyInfoResponse
    created_at: datetime
    updated_at: datetime


# ==== Health DTOs ====
class HealthResponse(BaseModel):
    """Response DTO para health check"""
    status: str
    version: str
    timestamp: datetime
    database: str
    workers: dict
