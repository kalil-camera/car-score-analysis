"""Application layer - Reliability Use Cases"""
import logging

from app.domain.reliability import (
    ReliabilityProfile, ReliabilityScore, WarrantyInfo,
    IReliabilityRepository
)
from app.domain.vehicles import IVehicleRepository
from app.shared.exceptions import EntityNotFoundError

logger = logging.getLogger(__name__)


class UpdateReliabilityUseCase:
    """Use case para atualizar reliability profile"""
    
    def __init__(self, reliability_repo: IReliabilityRepository, vehicle_repo: IVehicleRepository):
        self.reliability_repo = reliability_repo
        self.vehicle_repo = vehicle_repo
    
    async def execute(
        self,
        vehicle_id: int,
        overall_score: float,
        breakdown_frequency: float,
        customer_satisfaction: float,
        warranty_claims_rate: float,
        warranty_avg_cost: float
    ) -> ReliabilityProfile:
        """Executar use case"""
        # Validar vehicle
        vehicle = await self.vehicle_repo.find_by_id(vehicle_id)
        if not vehicle:
            raise EntityNotFoundError(f"Vehicle {vehicle_id} not found")
        
        # Buscar ou criar reliability profile
        reliability_profile = await self.reliability_repo.find_by_vehicle_id(vehicle_id)
        if not reliability_profile:
            reliability_profile = ReliabilityProfile(vehicle_id=vehicle_id)
        
        # Atualizar scores
        reliability_profile.update_score(
            overall_score=ReliabilityScore(overall_score),
            breakdown_frequency=breakdown_frequency,
            customer_satisfaction=customer_satisfaction,
            warranty_info=WarrantyInfo(warranty_claims_rate, warranty_avg_cost),
        )
        
        # Persistir
        saved_profile = await self.reliability_repo.save(reliability_profile)
        logger.info(f"Reliability profile updated for vehicle {vehicle_id}")
        return saved_profile


class GetReliabilityUseCase:
    """Use case para obter reliability profile"""
    
    def __init__(self, reliability_repo: IReliabilityRepository, vehicle_repo: IVehicleRepository):
        self.reliability_repo = reliability_repo
        self.vehicle_repo = vehicle_repo
    
    async def execute(self, vehicle_id: int) -> ReliabilityProfile:
        """Executar use case"""
        # Validar vehicle
        vehicle = await self.vehicle_repo.find_by_id(vehicle_id)
        if not vehicle:
            raise EntityNotFoundError(f"Vehicle {vehicle_id} not found")
        
        reliability_profile = await self.reliability_repo.find_by_vehicle_id(vehicle_id)
        if not reliability_profile:
            reliability_profile = ReliabilityProfile(vehicle_id=vehicle_id)
        
        logger.info(f"Retrieved reliability profile for vehicle {vehicle_id}")
        return reliability_profile
