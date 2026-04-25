"""Application layer - Pricing Use Cases"""
from typing import Optional, List
import logging

from app.domain.pricing import (
    PriceHistory, PriceRecord, Price, Currency,
    PriceSource, MarketType, IPriceRepository
)
from app.domain.vehicles import IVehicleRepository
from app.shared.exceptions import EntityNotFoundError

logger = logging.getLogger(__name__)


class AddPriceUseCase:
    """Use case para adicionar um preço"""
    
    def __init__(self, price_repo: IPriceRepository, vehicle_repo: IVehicleRepository):
        self.price_repo = price_repo
        self.vehicle_repo = vehicle_repo
    
    async def execute(
        self,
        vehicle_id: int,
        price_amount: float,
        source: str,
        market_type: str,
        currency: str = "BRL"
    ) -> PriceHistory:
        """Executar use case"""
        # Validar que vehicle existe
        vehicle = await self.vehicle_repo.find_by_id(vehicle_id)
        if not vehicle:
            raise EntityNotFoundError(f"Vehicle {vehicle_id} not found")
        
        # Buscar ou criar price history
        price_history = await self.price_repo.find_by_vehicle_id(vehicle_id)
        if not price_history:
            price_history = PriceHistory(vehicle_id=vehicle_id)
        
        # Criar novo price record
        price = Price(price_amount, Currency[currency])
        record = PriceRecord(
            price=price,
            source=PriceSource[source.upper()],
            market_type=MarketType[market_type.upper()],
        )
        
        # Adicionar ao histórico
        price_history.add_price_record(record)
        
        # Persistir
        saved_history = await self.price_repo.save(price_history)
        logger.info(f"Price added for vehicle {vehicle_id}: {record}")
        return saved_history


class GetPriceHistoryUseCase:
    """Use case para obter histórico de preços"""
    
    def __init__(self, price_repo: IPriceRepository, vehicle_repo: IVehicleRepository):
        self.price_repo = price_repo
        self.vehicle_repo = vehicle_repo
    
    async def execute(self, vehicle_id: int) -> PriceHistory:
        """Executar use case"""
        # Validar que vehicle existe
        vehicle = await self.vehicle_repo.find_by_id(vehicle_id)
        if not vehicle:
            raise EntityNotFoundError(f"Vehicle {vehicle_id} not found")
        
        price_history = await self.price_repo.find_by_vehicle_id(vehicle_id)
        if not price_history:
            price_history = PriceHistory(vehicle_id=vehicle_id)
        
        logger.info(f"Retrieved price history for vehicle {vehicle_id}")
        return price_history


class GetPriceStatisticsUseCase:
    """Use case para obter estatísticas de preço"""
    
    def __init__(self, price_repo: IPriceRepository, vehicle_repo: IVehicleRepository):
        self.price_repo = price_repo
        self.vehicle_repo = vehicle_repo
    
    async def execute(self, vehicle_id: int) -> dict:
        """Executar use case"""
        # Validar que vehicle existe
        vehicle = await self.vehicle_repo.find_by_id(vehicle_id)
        if not vehicle:
            raise EntityNotFoundError(f"Vehicle {vehicle_id} not found")
        
        price_history = await self.price_repo.find_by_vehicle_id(vehicle_id)
        if not price_history or not price_history.records:
            return {
                "count": 0,
                "average": 0.0,
                "min": 0.0,
                "max": 0.0
            }
        
        stats = price_history.get_price_statistics()
        logger.info(f"Retrieved price statistics for vehicle {vehicle_id}")
        return stats
