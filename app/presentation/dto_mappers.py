"""Presentation layer - DTO Mappers"""
from app.domain.vehicles import Vehicle
from app.domain.pricing import PriceHistory
from app.domain.safety import SafetyProfile
from app.domain.reliability import ReliabilityProfile

from app.application.dtos import (
    VehicleResponse, PriceRecordResponse, PriceHistoryResponse,
    PriceStatisticsResponse, SafetyRatingResponse, SafetyProfileResponse,
    ReliabilityResponse, WarrantyInfoResponse, VehicleDetailResponse,
)


class VehicleDTOMapper:
    """Mapper between Vehicle domain entity and DTOs"""
    
    @staticmethod
    def to_response(vehicle: Vehicle) -> VehicleResponse:
        """Convert domain entity to response DTO"""
        return VehicleResponse(
            id=vehicle.id,
            brand=str(vehicle.brand),
            model=str(vehicle.model),
            year=int(vehicle.year),
            fuel_type=vehicle.fuel_type.value,
            body_type=vehicle.body_type.value,
            description=vehicle.description,
            created_at=vehicle.created_at,
            updated_at=vehicle.updated_at,
        )


class PriceHistoryDTOMapper:
    """Mapper between PriceHistory domain entity and DTOs"""
    
    @staticmethod
    def to_response(price_history: PriceHistory) -> PriceHistoryResponse:
        """Convert domain entity to response DTO"""
        records = [
            PriceRecordResponse(
                amount=float(record.price),
                currency=record.price.currency.value,
                source=record.source.value,
                market_type=record.market_type.value,
                recorded_at=record.recorded_at,
            )
            for record in price_history.records
        ]
        
        stats = price_history.get_price_statistics()
        statistics = PriceStatisticsResponse(
            count=stats["count"],
            average=stats["average"],
            min=stats["min"],
            max=stats["max"],
        )
        
        return PriceHistoryResponse(
            vehicle_id=price_history.vehicle_id,
            records=records,
            statistics=statistics,
        )


class SafetyProfileDTOMapper:
    """Mapper between SafetyProfile domain entity and DTOs"""
    
    @staticmethod
    def to_response(safety_profile: SafetyProfile) -> SafetyProfileResponse:
        """Convert domain entity to response DTO"""
        ratings = [
            SafetyRatingResponse(
                organization=rating.organization.value,
                overall_score=float(rating.overall_score),
                frontal_crash=float(rating.frontal_crash),
                side_crash=float(rating.side_crash),
                rollover=float(rating.rollover),
                child_protection=float(rating.child_protection),
                pedestrian_protection=float(rating.pedestrian_protection),
                created_at=rating.frontal_crash.__dict__.get("created_at", None),  # Workaround
            )
            for rating in safety_profile.ratings
        ]
        
        return SafetyProfileResponse(
            vehicle_id=safety_profile.vehicle_id,
            ratings=ratings,
            average_score=safety_profile.get_average_score(),
        )


class ReliabilityProfileDTOMapper:
    """Mapper between ReliabilityProfile domain entity and DTOs"""
    
    @staticmethod
    def to_response(reliability_profile: ReliabilityProfile) -> ReliabilityResponse:
        """Convert domain entity to response DTO"""
        warranty_info = WarrantyInfoResponse(
            claims_rate=reliability_profile.warranty_info.claims_rate,
            avg_cost=reliability_profile.warranty_info.avg_cost,
        )
        
        return ReliabilityResponse(
            vehicle_id=reliability_profile.vehicle_id,
            overall_score=float(reliability_profile.overall_score),
            breakdown_frequency=reliability_profile.breakdown_frequency,
            customer_satisfaction=reliability_profile.customer_satisfaction,
            warranty_info=warranty_info,
            created_at=reliability_profile.created_at,
            updated_at=reliability_profile.updated_at,
        )
