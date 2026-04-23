"""Vehicle domain - Repository Interface (Abstract)"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entity import Vehicle
from .value_objects import Brand


class IVehicleRepository(ABC):
    """Interface para persistência de vehicles"""
    
    @abstractmethod
    async def save(self, vehicle: Vehicle) -> Vehicle:
        """Salvar ou atualizar vehicle"""
        pass
    
    @abstractmethod
    async def find_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        """Buscar vehicle por ID"""
        pass
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 10) -> List[Vehicle]:
        """Buscar todos vehicles com paginação"""
        pass
    
    @abstractmethod
    async def search_by_brand(self, brand: Brand) -> List[Vehicle]:
        """Buscar vehicles por marca"""
        pass
    
    @abstractmethod
    async def delete(self, vehicle_id: int) -> bool:
        """Deletar vehicle"""
        pass
