"""Dependency Injection Container"""
from typing import Callable
from sqlalchemy.orm import Session

from app.infrastructure import (
    SQLAlchemyVehicleRepository,
    SQLAlchemyPriceRepository,
    SQLAlchemySafetyRepository,
    SQLAlchemyReliabilityRepository,
)
from app.application.use_cases import (
    CreateVehicleUseCase,
    ListVehiclesUseCase,
    GetVehicleUseCase,
    UpdateVehicleUseCase,
    DeleteVehicleUseCase,
    SearchVehiclesByBrandUseCase,
    AddPriceUseCase,
    GetPriceHistoryUseCase,
    GetPriceStatisticsUseCase,
    AddSafetyRatingUseCase,
    GetSafetyProfileUseCase,
    UpdateReliabilityUseCase,
    GetReliabilityUseCase,
)


class DIContainer:
    """Dependency Injection Container"""
    
    def __init__(self, get_db: Callable[[], Session]):
        self.get_db = get_db
    
    # ===== Repositories =====
    def get_vehicle_repository(self):
        db = next(self.get_db())
        return SQLAlchemyVehicleRepository(db)
    
    def get_price_repository(self):
        db = next(self.get_db())
        return SQLAlchemyPriceRepository(db)
    
    def get_safety_repository(self):
        db = next(self.get_db())
        return SQLAlchemySafetyRepository(db)
    
    def get_reliability_repository(self):
        db = next(self.get_db())
        return SQLAlchemyReliabilityRepository(db)
    
    # ===== Vehicle Use Cases =====
    def get_create_vehicle_use_case(self) -> CreateVehicleUseCase:
        return CreateVehicleUseCase(self.get_vehicle_repository())
    
    def get_list_vehicles_use_case(self) -> ListVehiclesUseCase:
        return ListVehiclesUseCase(self.get_vehicle_repository())
    
    def get_get_vehicle_use_case(self) -> GetVehicleUseCase:
        return GetVehicleUseCase(self.get_vehicle_repository())
    
    def get_update_vehicle_use_case(self) -> UpdateVehicleUseCase:
        return UpdateVehicleUseCase(self.get_vehicle_repository())
    
    def get_delete_vehicle_use_case(self) -> DeleteVehicleUseCase:
        return DeleteVehicleUseCase(self.get_vehicle_repository())
    
    def get_search_vehicles_by_brand_use_case(self) -> SearchVehiclesByBrandUseCase:
        return SearchVehiclesByBrandUseCase(self.get_vehicle_repository())
    
    # ===== Price Use Cases =====
    def get_add_price_use_case(self) -> AddPriceUseCase:
        return AddPriceUseCase(self.get_price_repository(), self.get_vehicle_repository())
    
    def get_get_price_history_use_case(self) -> GetPriceHistoryUseCase:
        return GetPriceHistoryUseCase(self.get_price_repository(), self.get_vehicle_repository())
    
    def get_get_price_statistics_use_case(self) -> GetPriceStatisticsUseCase:
        return GetPriceStatisticsUseCase(self.get_price_repository(), self.get_vehicle_repository())
    
    # ===== Safety Use Cases =====
    def get_add_safety_rating_use_case(self) -> AddSafetyRatingUseCase:
        return AddSafetyRatingUseCase(self.get_safety_repository(), self.get_vehicle_repository())
    
    def get_get_safety_profile_use_case(self) -> GetSafetyProfileUseCase:
        return GetSafetyProfileUseCase(self.get_safety_repository(), self.get_vehicle_repository())
    
    # ===== Reliability Use Cases =====
    def get_update_reliability_use_case(self) -> UpdateReliabilityUseCase:
        return UpdateReliabilityUseCase(self.get_reliability_repository(), self.get_vehicle_repository())
    
    def get_get_reliability_use_case(self) -> GetReliabilityUseCase:
        return GetReliabilityUseCase(self.get_reliability_repository(), self.get_vehicle_repository())


# Global container instance
_container: DIContainer = None


def initialize_container(get_db: Callable[[], Session]):
    """Inicializar o container global"""
    global _container
    _container = DIContainer(get_db)


def get_container() -> DIContainer:
    """Obter o container global"""
    if _container is None:
        raise RuntimeError("DI Container not initialized")
    return _container
