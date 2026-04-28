"""Reliability domain - Repository Interface"""
from abc import ABC, abstractmethod
from typing import Optional
from .entity import ReliabilityProfile


class IReliabilityRepository(ABC):
    """Interface para persistência de reliability profiles"""
    
    @abstractmethod
    async def save(self, reliability_profile: ReliabilityProfile) -> ReliabilityProfile:
        """Salvar ou atualizar reliability profile"""
        pass
    
    @abstractmethod
    async def find_by_vehicle_id(self, vehicle_id: int) -> Optional[ReliabilityProfile]:
        """Buscar reliability profile de um vehicle"""
        pass
    
    @abstractmethod
    async def delete(self, vehicle_id: int) -> bool:
        """Deletar reliability profile"""
        pass
