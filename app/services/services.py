"""Vehicle service layer"""
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models import Vehicle, VehiclePrice, SafetyRating, ReliabilityIndex
from app.schemas import (
    VehicleCreate,
    VehicleUpdate,
    PriceRangeFilter,
    VehicleSearchParams,
)


class VehicleService:
    """Service for vehicle operations"""

    @staticmethod
    def create_vehicle(db: Session, vehicle: VehicleCreate) -> Vehicle:
        """Create a new vehicle"""
        db_vehicle = Vehicle(**vehicle.model_dump())
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle

    @staticmethod
    def get_vehicle(db: Session, vehicle_id: int) -> Optional[Vehicle]:
        """Get vehicle by ID"""
        return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    @staticmethod
    def get_vehicles(db: Session, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Get all vehicles with pagination"""
        return db.query(Vehicle).offset(skip).limit(limit).all()

    @staticmethod
    def search_vehicles(db: Session, params: VehicleSearchParams) -> List[Vehicle]:
        """Search vehicles with filters"""
        query = db.query(Vehicle)

        if params.brand:
            query = query.filter(Vehicle.brand.ilike(f"%{params.brand}%"))
        if params.model:
            query = query.filter(Vehicle.model.ilike(f"%{params.model}%"))
        if params.year_from:
            query = query.filter(Vehicle.year >= params.year_from)
        if params.year_to:
            query = query.filter(Vehicle.year <= params.year_to)
        if params.fuel_type:
            query = query.filter(Vehicle.fuel_type.ilike(f"%{params.fuel_type}%"))
        if params.body_type:
            query = query.filter(Vehicle.body_type.ilike(f"%{params.body_type}%"))

        return query.offset(params.skip).limit(params.limit).all()

    @staticmethod
    def update_vehicle(db: Session, vehicle_id: int, vehicle_update: VehicleUpdate) -> Optional[Vehicle]:
        """Update vehicle"""
        db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not db_vehicle:
            return None

        update_data = vehicle_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vehicle, field, value)

        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle

    @staticmethod
    def delete_vehicle(db: Session, vehicle_id: int) -> bool:
        """Delete vehicle"""
        db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not db_vehicle:
            return False

        db.delete(db_vehicle)
        db.commit()
        return True

    @staticmethod
    def get_or_create_vehicle(db: Session, brand: str, model: str, year: int,
                             fuel_type: str, body_type: str) -> Vehicle:
        """Get existing vehicle or create new one"""
        db_vehicle = db.query(Vehicle).filter(
            and_(
                Vehicle.brand == brand,
                Vehicle.model == model,
                Vehicle.year == year,
                Vehicle.fuel_type == fuel_type,
                Vehicle.body_type == body_type,
            )
        ).first()

        if not db_vehicle:
            db_vehicle = Vehicle(
                brand=brand,
                model=model,
                year=year,
                fuel_type=fuel_type,
                body_type=body_type,
            )
            db.add(db_vehicle)
            db.commit()
            db.refresh(db_vehicle)

        return db_vehicle


class PriceService:
    """Service for vehicle price operations"""

    @staticmethod
    def add_price(db: Session, vehicle_id: int, price: float, currency: str,
                  source: str, market_type: str, recorded_at: datetime = None) -> VehiclePrice:
        """Add price record for vehicle"""
        if recorded_at is None:
            recorded_at = datetime.utcnow()

        db_price = VehiclePrice(
            vehicle_id=vehicle_id,
            price=price,
            currency=currency,
            source=source,
            market_type=market_type,
            recorded_at=recorded_at,
        )
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price

    @staticmethod
    def get_price_history(db: Session, vehicle_id: int, days: int = 30,
                          limit: int = 1000) -> List[VehiclePrice]:
        """Get price history for vehicle"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return db.query(VehiclePrice).filter(
            and_(
                VehiclePrice.vehicle_id == vehicle_id,
                VehiclePrice.recorded_at >= cutoff_date,
            )
        ).order_by(VehiclePrice.recorded_at.desc()).limit(limit).all()

    @staticmethod
    def get_price_statistics(db: Session, vehicle_id: int, days: int = 30) -> dict:
        """Get price statistics for vehicle"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = db.query(VehiclePrice).filter(
            and_(
                VehiclePrice.vehicle_id == vehicle_id,
                VehiclePrice.recorded_at >= cutoff_date,
            )
        )

        stats = db.query(
            func.avg(VehiclePrice.price).label("avg_price"),
            func.min(VehiclePrice.price).label("min_price"),
            func.max(VehiclePrice.price).label("max_price"),
            func.count(VehiclePrice.id).label("total_records"),
        ).filter(
            and_(
                VehiclePrice.vehicle_id == vehicle_id,
                VehiclePrice.recorded_at >= cutoff_date,
            )
        ).first()

        latest = query.order_by(VehiclePrice.recorded_at.desc()).first()

        return {
            "latest_price": latest.price if latest else None,
            "avg_price": float(stats.avg_price) if stats.avg_price else None,
            "min_price": float(stats.min_price) if stats.min_price else None,
            "max_price": float(stats.max_price) if stats.max_price else None,
            "total_records": stats.total_records if stats.total_records else 0,
            "period_days": days,
        }

    @staticmethod
    def filter_by_price_range(db: Session, filter_params: PriceRangeFilter,
                             limit: int = 100) -> List[dict]:
        """Find vehicles within price range"""
        query = db.query(
            Vehicle,
            VehiclePrice,
        ).join(VehiclePrice).filter(VehiclePrice.currency == filter_params.currency)

        if filter_params.min_price:
            query = query.filter(VehiclePrice.price >= filter_params.min_price)
        if filter_params.max_price:
            query = query.filter(VehiclePrice.price <= filter_params.max_price)
        if filter_params.market_type:
            query = query.filter(VehiclePrice.market_type == filter_params.market_type)
        if filter_params.source:
            query = query.filter(VehiclePrice.source == filter_params.source)

        return query.limit(limit).all()


class SafetyService:
    """Service for safety rating operations"""

    @staticmethod
    def add_rating(db: Session, vehicle_id: int, organization: str,
                   overall_score: float, **kwargs) -> SafetyRating:
        """Add safety rating for vehicle"""
        db_rating = SafetyRating(
            vehicle_id=vehicle_id,
            organization=organization,
            overall_score=overall_score,
            **kwargs,
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating

    @staticmethod
    def get_ratings(db: Session, vehicle_id: int) -> List[SafetyRating]:
        """Get all safety ratings for vehicle"""
        return db.query(SafetyRating).filter(
            SafetyRating.vehicle_id == vehicle_id
        ).all()

    @staticmethod
    def get_rating_by_organization(db: Session, vehicle_id: int,
                                   organization: str) -> Optional[SafetyRating]:
        """Get safety rating by organization"""
        return db.query(SafetyRating).filter(
            and_(
                SafetyRating.vehicle_id == vehicle_id,
                SafetyRating.organization == organization,
            )
        ).first()


class ReliabilityService:
    """Service for reliability index operations"""

    @staticmethod
    def set_reliability_index(db: Session, vehicle_id: int, score: float,
                             data_source: str, **kwargs) -> ReliabilityIndex:
        """Set or update reliability index"""
        db_index = db.query(ReliabilityIndex).filter(
            ReliabilityIndex.vehicle_id == vehicle_id
        ).first()

        if db_index:
            db_index.score = score
            db_index.data_source = data_source
            for key, value in kwargs.items():
                if hasattr(db_index, key):
                    setattr(db_index, key, value)
        else:
            db_index = ReliabilityIndex(
                vehicle_id=vehicle_id,
                score=score,
                data_source=data_source,
                **kwargs,
            )
            db.add(db_index)

        db.commit()
        db.refresh(db_index)
        return db_index

    @staticmethod
    def get_reliability_index(db: Session, vehicle_id: int) -> Optional[ReliabilityIndex]:
        """Get reliability index"""
        return db.query(ReliabilityIndex).filter(
            ReliabilityIndex.vehicle_id == vehicle_id
        ).first()
