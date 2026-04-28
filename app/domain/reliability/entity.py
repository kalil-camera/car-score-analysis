"""Reliability domain - Aggregate Root Entity"""
from datetime import datetime
from app.shared.types import AggregateRoot
from .value_objects import ReliabilityScore, WarrantyInfo


class ReliabilityProfile(AggregateRoot):
    """
    Reliability Profile Aggregate Root
    
    Mantém informações de confiabilidade de um vehicle
    """
    
    def __init__(
        self,
        vehicle_id: int,
        overall_score: ReliabilityScore = None,
        breakdown_frequency: float = 0.0,
        customer_satisfaction: float = 0.0,
        warranty_info: WarrantyInfo = None,
        id: int = None
    ):
        super().__init__(id)
        self.vehicle_id = vehicle_id
        self.overall_score = overall_score or ReliabilityScore(50.0)
        self.breakdown_frequency = breakdown_frequency
        self.customer_satisfaction = customer_satisfaction
        self.warranty_info = warranty_info or WarrantyInfo(0.0, 0.0)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def update_score(
        self,
        overall_score: ReliabilityScore,
        breakdown_frequency: float,
        customer_satisfaction: float,
        warranty_info: WarrantyInfo
    ):
        """Atualizar score de confiabilidade"""
        self.overall_score = overall_score
        self.breakdown_frequency = breakdown_frequency
        self.customer_satisfaction = customer_satisfaction
        self.warranty_info = warranty_info
        self.updated_at = datetime.utcnow()
    
    def __str__(self):
        return f"ReliabilityProfile(vehicle_id={self.vehicle_id}, score={self.overall_score})"
