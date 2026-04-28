"""Pricing domain - Aggregate Root Entity"""
from typing import List
from datetime import datetime
from app.shared.types import AggregateRoot
from .value_objects import PriceRecord


class PriceHistory(AggregateRoot):
    """
    Price History Aggregate Root
    
    Mantém histórico de preços de um vehicle
    """
    
    def __init__(self, vehicle_id: int, id: int = None):
        super().__init__(id)
        self.vehicle_id = vehicle_id
        self.records: List[PriceRecord] = []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def add_price_record(self, record: PriceRecord):
        """Adicionar novo price record"""
        self.records.append(record)
        self.updated_at = datetime.utcnow()
    
    def get_latest_price(self) -> PriceRecord:
        """Obter preço mais recente"""
        if not self.records:
            return None
        return sorted(self.records, key=lambda r: r.recorded_at)[-1]
    
    def get_price_statistics(self) -> dict:
        """Calcular estatísticas de preço"""
        if not self.records:
            return {
                "count": 0,
                "average": 0,
                "min": 0,
                "max": 0
            }
        
        prices = [float(r.price) for r in self.records]
        return {
            "count": len(prices),
            "average": sum(prices) / len(prices),
            "min": min(prices),
            "max": max(prices)
        }
    
    def __str__(self):
        return f"PriceHistory(vehicle_id={self.vehicle_id}, records={len(self.records)})"
