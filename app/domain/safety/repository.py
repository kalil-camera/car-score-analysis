"""Safety domain - Repository Interface"""
from abc import ABC, abstractmethod
from typing import Optional
from .entity import SafetyProfile


class ISafetyRepository(ABC):
    """Interface para persistência de safety profiles"""
    
    @abstractmethod
    async def save(self, safety_profile: SafetyProfile) -> SafetyProfile:
        """Salvar ou atualizar safety profile"""
        pass
    
    @abstractmethod
    async def find_by_vehicle_id(self, vehicle_id: int) -> Optional[SafetyProfile]:
        """Buscar safety profile de um vehicle"""
        pass
    
    @abstractmethod
    async def delete(self, vehicle_id: int) -> bool:
        """Deletar safety profile"""
        pass
