"""Application layer - Safety Use Cases"""
from typing import Optional
import logging

from app.domain.safety import (
    SafetyProfile, SafetyRating, SafetyScore,
    SafetyOrganization, ISafetyRepository
)
from app.domain.vehicles import IVehicleRepository
from app.shared.exceptions import EntityNotFoundError

logger = logging.getLogger(__name__)


class AddSafetyRatingUseCase:
    """Use case para adicionar um safety rating"""
    
    def __init__(self, safety_repo: ISafetyRepository, vehicle_repo: IVehicleRepository):
        self.safety_repo = safety_repo
        self.vehicle_repo = vehicle_repo
    
    async def execute(
        self,
        vehicle_id: int,
        organization: str,
        overall_score: float,
        frontal_crash: float,
        side_crash: float,
        rollover: float,
        child_protection: float,
        pedestrian_protection: float
    ) -> SafetyProfile:
        """Executar use case"""
        # Validar vehicle
        vehicle = await self.vehicle_repo.find_by_id(vehicle_id)
        if not vehicle:
            raise EntityNotFoundError(f"Vehicle {vehicle_id} not found")
        
        # Buscar ou criar safety profile
        safety_profile = await self.safety_repo.find_by_vehicle_id(vehicle_id)
        if not safety_profile:
            safety_profile = SafetyProfile(vehicle_id=vehicle_id)
        
        # Criar rating
        rating = SafetyRating(
            organization=SafetyOrganization[organization.upper().replace(" ", "_")],
            overall_score=SafetyScore(overall_score),
            frontal_crash=SafetyScore(frontal_crash),
            side_crash=SafetyScore(side_crash),
            rollover=SafetyScore(rollover),
            child_protection=SafetyScore(child_protection),
            pedestrian_protection=SafetyScore(pedestrian_protection),
        )
        
        # Adicionar ao profile
        safety_profile.add_rating(rating)
        
        # Persistir
        saved_profile = await self.safety_repo.save(safety_profile)
        logger.info(f"Safety rating added for vehicle {vehicle_id}")
        return saved_profile


class GetSafetyProfileUseCase:
    """Use case para obter safety profile"""
    
    def __init__(self, safety_repo: ISafetyRepository, vehicle_repo: IVehicleRepository):
        self.safety_repo = safety_repo
        self.vehicle_repo = vehicle_repo
    
    async def execute(self, vehicle_id: int) -> SafetyProfile:
        """Executar use case"""
        # Validar vehicle
        vehicle = await self.vehicle_repo.find_by_id(vehicle_id)
        if not vehicle:
            raise EntityNotFoundError(f"Vehicle {vehicle_id} not found")
        
        safety_profile = await self.safety_repo.find_by_vehicle_id(vehicle_id)
        if not safety_profile:
            safety_profile = SafetyProfile(vehicle_id=vehicle_id)
        
        logger.info(f"Retrieved safety profile for vehicle {vehicle_id}")
        return safety_profile
