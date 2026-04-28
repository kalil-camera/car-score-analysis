"""Pricing domain - Repository Interface"""
from abc import ABC, abstractmethod
from typing import Optional
from .entity import PriceHistory


class IPriceRepository(ABC):
    """Interface para persistência de preços"""
    
    @abstractmethod
    async def save(self, price_history: PriceHistory) -> PriceHistory:
        """Salvar ou atualizar price history"""
        pass
    
    @abstractmethod
    async def find_by_vehicle_id(self, vehicle_id: int) -> Optional[PriceHistory]:
        """Buscar price history de um vehicle"""
        pass
    
    @abstractmethod
    async def delete(self, vehicle_id: int) -> bool:
        """Deletar price history"""
        pass
