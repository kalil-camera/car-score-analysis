"""Infrastructure layer - SQLAlchemy Repositories"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.domain.vehicles import Vehicle, IVehicleRepository, Brand
from app.domain.pricing import PriceHistory, IPriceRepository, PriceSource, MarketType
from app.domain.safety import SafetyProfile, ISafetyRepository
from app.domain.reliability import ReliabilityProfile, IReliabilityRepository

from .orm_models import VehicleORM, VehiclePriceORM, SafetyRatingORM, ReliabilityORM
from .mappers import VehicleMapper, PriceHistoryMapper, SafetyProfileMapper, ReliabilityProfileMapper


class SQLAlchemyVehicleRepository(IVehicleRepository):
    """SQLAlchemy implementation de IVehicleRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def save(self, vehicle: Vehicle) -> Vehicle:
        """Salvar ou atualizar vehicle"""
        orm = VehicleMapper.to_orm(vehicle)
        
        if orm.id:
            # Update
            existing = self.db.query(VehicleORM).filter(VehicleORM.id == orm.id).first()
            for key, value in vars(orm).items():
                if not key.startswith('_'):
                    setattr(existing, key, value)
            self.db.add(existing)
        else:
            # Create
            self.db.add(orm)
        
        self.db.commit()
        self.db.refresh(orm)
        return VehicleMapper.to_domain(orm)
    
    async def find_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        """Buscar vehicle por ID"""
        orm = self.db.query(VehicleORM).filter(VehicleORM.id == vehicle_id).first()
        return VehicleMapper.to_domain(orm)
    
    async def find_all(self, skip: int = 0, limit: int = 10) -> List[Vehicle]:
        """Buscar todos vehicles com paginação"""
        orms = self.db.query(VehicleORM).offset(skip).limit(limit).all()
        return [VehicleMapper.to_domain(orm) for orm in orms]
    
    async def search_by_brand(self, brand: Brand) -> List[Vehicle]:
        """Buscar vehicles por brand"""
        orms = self.db.query(VehicleORM).filter(VehicleORM.brand == str(brand)).all()
        return [VehicleMapper.to_domain(orm) for orm in orms]
    
    async def delete(self, vehicle_id: int) -> bool:
        """Deletar vehicle"""
        result = self.db.query(VehicleORM).filter(VehicleORM.id == vehicle_id).delete()
        self.db.commit()
        return result > 0


class SQLAlchemyPriceRepository(IPriceRepository):
    """SQLAlchemy implementation de IPriceRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def save(self, price_history: PriceHistory) -> PriceHistory:
        """Salvar price records"""
        for record in price_history.records:
            orm_records = PriceHistoryMapper.to_orm(price_history)
            for orm_record in orm_records:
                self.db.add(orm_record)
        
        self.db.commit()
        return price_history
    
    async def find_by_vehicle_id(self, vehicle_id: int) -> Optional[PriceHistory]:
        """Buscar price history de um vehicle"""
        orms = self.db.query(VehiclePriceORM).filter(
            VehiclePriceORM.vehicle_id == vehicle_id
        ).order_by(VehiclePriceORM.recorded_at).all()
        
        if not orms:
            return None
        
        return PriceHistoryMapper.to_domain(vehicle_id, orms)
    
    async def delete(self, vehicle_id: int) -> bool:
        """Deletar price history"""
        result = self.db.query(VehiclePriceORM).filter(
            VehiclePriceORM.vehicle_id == vehicle_id
        ).delete()
        self.db.commit()
        return result > 0


class SQLAlchemySafetyRepository(ISafetyRepository):
    """SQLAlchemy implementation de ISafetyRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def save(self, safety_profile: SafetyProfile) -> SafetyProfile:
        """Salvar safety ratings"""
        orm_records = SafetyProfileMapper.to_orm(safety_profile)
        for orm_record in orm_records:
            self.db.add(orm_record)
        
        self.db.commit()
        return safety_profile
    
    async def find_by_vehicle_id(self, vehicle_id: int) -> Optional[SafetyProfile]:
        """Buscar safety profile de um vehicle"""
        orms = self.db.query(SafetyRatingORM).filter(
            SafetyRatingORM.vehicle_id == vehicle_id
        ).all()
        
        if not orms:
            return None
        
        return SafetyProfileMapper.to_domain(vehicle_id, orms)
    
    async def delete(self, vehicle_id: int) -> bool:
        """Deletar safety profile"""
        result = self.db.query(SafetyRatingORM).filter(
            SafetyRatingORM.vehicle_id == vehicle_id
        ).delete()
        self.db.commit()
        return result > 0


class SQLAlchemyReliabilityRepository(IReliabilityRepository):
    """SQLAlchemy implementation de IReliabilityRepository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def save(self, reliability_profile: ReliabilityProfile) -> ReliabilityProfile:
        """Salvar reliability profile"""
        orm = ReliabilityProfileMapper.to_orm(reliability_profile)
        
        if orm.id:
            existing = self.db.query(ReliabilityORM).filter(ReliabilityORM.id == orm.id).first()
            if existing:
                for key, value in vars(orm).items():
                    if not key.startswith('_'):
                        setattr(existing, key, value)
                self.db.add(existing)
            else:
                self.db.add(orm)
        else:
            self.db.add(orm)
        
        self.db.commit()
        self.db.refresh(orm)
        return ReliabilityProfileMapper.to_domain(orm)
    
    async def find_by_vehicle_id(self, vehicle_id: int) -> Optional[ReliabilityProfile]:
        """Buscar reliability profile de um vehicle"""
        orm = self.db.query(ReliabilityORM).filter(
            ReliabilityORM.vehicle_id == vehicle_id
        ).first()
        
        if not orm:
            return None
        
        return ReliabilityProfileMapper.to_domain(orm)
    
    async def delete(self, vehicle_id: int) -> bool:
        """Deletar reliability profile"""
        result = self.db.query(ReliabilityORM).filter(
            ReliabilityORM.vehicle_id == vehicle_id
        ).delete()
        self.db.commit()
        return result > 0
