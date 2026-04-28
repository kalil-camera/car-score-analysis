"""Application layer - Vehicle Use Cases"""
from typing import List, Optional
import logging

from app.domain.vehicles import (
    Vehicle, Brand, Model, Year, FuelType, BodyType,
    IVehicleRepository
)
from app.shared.exceptions import EntityNotFoundError, InvalidValueObjectError

logger = logging.getLogger(__name__)


class CreateVehicleUseCase:
    """Use case para criar um novo vehicle"""
    
    def __init__(self, vehicle_repo: IVehicleRepository):
        self.vehicle_repo = vehicle_repo
    
    async def execute(self, brand: str, model: str, year: int, 
                     fuel_type: str, body_type: str, 
                     description: Optional[str] = None) -> Vehicle:
        """Executar use case"""
        try:
            # Criar value objects
            brand_vo = Brand(brand)
            model_vo = Model(model)
            year_vo = Year(year)
            fuel_type_enum = FuelType(fuel_type)
            body_type_enum = BodyType(body_type)
            
            # Criar entity
            vehicle = Vehicle(
                brand=brand_vo,
                model=model_vo,
                year=year_vo,
                fuel_type=fuel_type_enum,
                body_type=body_type_enum,
                description=description
            )
            
            # Persistir
            saved_vehicle = await self.vehicle_repo.save(vehicle)
            logger.info(f"Vehicle created: {saved_vehicle}")
            return saved_vehicle
            
        except InvalidValueObjectError as e:
            logger.error(f"Validation error: {e}")
            raise


class ListVehiclesUseCase:
    """Use case para listar vehicles"""
    
    def __init__(self, vehicle_repo: IVehicleRepository):
        self.vehicle_repo = vehicle_repo
    
    async def execute(self, skip: int = 0, limit: int = 10) -> List[Vehicle]:
        """Executar use case"""
        vehicles = await self.vehicle_repo.find_all(skip, limit)
        logger.info(f"Listed {len(vehicles)} vehicles")
        return vehicles


class GetVehicleUseCase:
    """Use case para obter um vehicle"""
    
    def __init__(self, vehicle_repo: IVehicleRepository):
        self.vehicle_repo = vehicle_repo
    
    async def execute(self, vehicle_id: int) -> Vehicle:
        """Executar use case"""
        vehicle = await self.vehicle_repo.find_by_id(vehicle_id)
        
        if not vehicle:
            logger.error(f"Vehicle {vehicle_id} not found")
            raise EntityNotFoundError(f"Vehicle {vehicle_id} not found")
        
        return vehicle


class UpdateVehicleUseCase:
    """Use case para atualizar vehicle"""
    
    def __init__(self, vehicle_repo: IVehicleRepository):
        self.vehicle_repo = vehicle_repo
    
    async def execute(self, vehicle_id: int, description: Optional[str] = None) -> Vehicle:
        """Executar use case"""
        vehicle = await self.vehicle_repo.find_by_id(vehicle_id)
        
        if not vehicle:
            raise EntityNotFoundError(f"Vehicle {vehicle_id} not found")
        
        if description:
            vehicle.update_description(description)
        
        updated_vehicle = await self.vehicle_repo.save(vehicle)
        logger.info(f"Vehicle {vehicle_id} updated")
        return updated_vehicle


class DeleteVehicleUseCase:
    """Use case para deletar vehicle"""
    
    def __init__(self, vehicle_repo: IVehicleRepository):
        self.vehicle_repo = vehicle_repo
    
    async def execute(self, vehicle_id: int) -> bool:
        """Executar use case"""
        vehicle = await self.vehicle_repo.find_by_id(vehicle_id)
        
        if not vehicle:
            raise EntityNotFoundError(f"Vehicle {vehicle_id} not found")
        
        result = await self.vehicle_repo.delete(vehicle_id)
        logger.info(f"Vehicle {vehicle_id} deleted")
        return result


class SearchVehiclesByBrandUseCase:
    """Use case para buscar vehicles por brand"""
    
    def __init__(self, vehicle_repo: IVehicleRepository):
        self.vehicle_repo = vehicle_repo
    
    async def execute(self, brand: str) -> List[Vehicle]:
        """Executar use case"""
        brand_vo = Brand(brand)
        vehicles = await self.vehicle_repo.search_by_brand(brand_vo)
        logger.info(f"Found {len(vehicles)} vehicles for brand {brand}")
        return vehicles
