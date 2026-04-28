"""Infrastructure layer - Mappers between ORM and Domain entities"""
from app.domain.vehicles import Vehicle, Brand, Model, Year, FuelType, BodyType
from app.domain.pricing import PriceHistory, PriceRecord, Price, Currency, PriceSource, MarketType
from app.domain.safety import SafetyProfile, SafetyRating, SafetyScore, SafetyOrganization
from app.domain.reliability import ReliabilityProfile, ReliabilityScore, WarrantyInfo

from .orm_models import (
    VehicleORM, VehiclePriceORM, SafetyRatingORM, ReliabilityORM
)


class VehicleMapper:
    """Mapper entre VehicleORM e Vehicle domain entity"""
    
    @staticmethod
    def to_domain(orm: VehicleORM) -> Vehicle:
        """Converter ORM model to domain entity"""
        if not orm:
            return None
        
        return Vehicle(
            id=orm.id,
            brand=Brand(orm.brand),
            model=Model(orm.model),
            year=Year(orm.year),
            fuel_type=orm.fuel_type,
            body_type=orm.body_type,
            description=orm.description,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
    
    @staticmethod
    def to_orm(vehicle: Vehicle) -> VehicleORM:
        """Converter domain entity to ORM model"""
        if not vehicle:
            return None
        
        return VehicleORM(
            id=vehicle.id,
            brand=str(vehicle.brand),
            model=str(vehicle.model),
            year=int(vehicle.year),
            fuel_type=vehicle.fuel_type,
            body_type=vehicle.body_type,
            description=vehicle.description,
            created_at=vehicle.created_at,
            updated_at=vehicle.updated_at,
        )


class PriceHistoryMapper:
    """Mapper entre VehiclePriceORM e PriceHistory domain entity"""
    
    @staticmethod
    def to_domain(vehicle_id: int, price_orms: list) -> PriceHistory:
        """Converter ORM models to domain entity"""
        price_history = PriceHistory(vehicle_id=vehicle_id)
        
        for price_orm in price_orms:
            record = PriceRecord(
                price=Price(price_orm.amount, Currency[price_orm.currency]),
                source=PriceSource[price_orm.source],
                market_type=MarketType[price_orm.market_type],
                recorded_at=price_orm.recorded_at,
            )
            price_history.records.append(record)
        
        return price_history
    
    @staticmethod
    def to_orm(price_history: PriceHistory) -> list:
        """Converter domain entity to ORM models"""
        orm_records = []
        
        for record in price_history.records:
            orm_record = VehiclePriceORM(
                vehicle_id=price_history.vehicle_id,
                amount=float(record.price),
                currency=record.price.currency.value,
                source=record.source.value,
                market_type=record.market_type.value,
                recorded_at=record.recorded_at,
            )
            orm_records.append(orm_record)
        
        return orm_records


class SafetyProfileMapper:
    """Mapper entre SafetyRatingORM e SafetyProfile domain entity"""
    
    @staticmethod
    def to_domain(vehicle_id: int, rating_orms: list) -> SafetyProfile:
        """Converter ORM models to domain entity"""
        safety_profile = SafetyProfile(vehicle_id=vehicle_id)
        
        for rating_orm in rating_orms:
            rating = SafetyRating(
                organization=SafetyOrganization[rating_orm.organization.replace(" ", "_").upper()],
                overall_score=SafetyScore(rating_orm.overall_score),
                frontal_crash=SafetyScore(rating_orm.frontal_crash),
                side_crash=SafetyScore(rating_orm.side_crash),
                rollover=SafetyScore(rating_orm.rollover),
                child_protection=SafetyScore(rating_orm.child_protection),
                pedestrian_protection=SafetyScore(rating_orm.pedestrian_protection),
            )
            safety_profile.ratings.append(rating)
        
        return safety_profile
    
    @staticmethod
    def to_orm(safety_profile: SafetyProfile) -> list:
        """Converter domain entity to ORM models"""
        orm_records = []
        
        for rating in safety_profile.ratings:
            orm_rating = SafetyRatingORM(
                vehicle_id=safety_profile.vehicle_id,
                organization=rating.organization.value,
                overall_score=float(rating.overall_score),
                frontal_crash=float(rating.frontal_crash),
                side_crash=float(rating.side_crash),
                rollover=float(rating.rollover),
                child_protection=float(rating.child_protection),
                pedestrian_protection=float(rating.pedestrian_protection),
            )
            orm_records.append(orm_rating)
        
        return orm_records


class ReliabilityProfileMapper:
    """Mapper entre ReliabilityORM e ReliabilityProfile domain entity"""
    
    @staticmethod
    def to_domain(orm: ReliabilityORM) -> ReliabilityProfile:
        """Converter ORM model to domain entity"""
        if not orm:
            return None
        
        return ReliabilityProfile(
            id=orm.id,
            vehicle_id=orm.vehicle_id,
            overall_score=ReliabilityScore(orm.overall_score),
            breakdown_frequency=orm.breakdown_frequency,
            customer_satisfaction=orm.customer_satisfaction,
            warranty_info=WarrantyInfo(orm.warranty_claims_rate, orm.warranty_avg_cost),
        )
    
    @staticmethod
    def to_orm(reliability_profile: ReliabilityProfile) -> ReliabilityORM:
        """Converter domain entity to ORM model"""
        if not reliability_profile:
            return None
        
        orm = ReliabilityORM(
            id=reliability_profile.id,
            vehicle_id=reliability_profile.vehicle_id,
            overall_score=float(reliability_profile.overall_score),
            breakdown_frequency=reliability_profile.breakdown_frequency,
            customer_satisfaction=reliability_profile.customer_satisfaction,
            warranty_claims_rate=reliability_profile.warranty_info.claims_rate,
            warranty_avg_cost=reliability_profile.warranty_info.avg_cost,
            created_at=reliability_profile.created_at,
            updated_at=reliability_profile.updated_at,
        )
        return orm
