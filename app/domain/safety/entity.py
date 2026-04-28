"""Safety domain - Aggregate Root Entity"""
from typing import List, Optional
from datetime import datetime
from app.shared.types import AggregateRoot
from .value_objects import SafetyRating


class SafetyProfile(AggregateRoot):
    """
    Safety Profile Aggregate Root
    
    Mantém ratings de segurança de um vehicle
    """
    
    def __init__(self, vehicle_id: int, id: int = None):
        super().__init__(id)
        self.vehicle_id = vehicle_id
        self.ratings: List[SafetyRating] = []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def add_rating(self, rating: SafetyRating):
        """Adicionar novo safety rating"""
        self.ratings.append(rating)
        self.updated_at = datetime.utcnow()
    
    def get_latest_rating(self) -> Optional[SafetyRating]:
        """Obter rating mais recente"""
        if not self.ratings:
            return None
        return self.ratings[-1]
    
    def get_average_score(self) -> float:
        """Calcular score médio"""
        if not self.ratings:
            return 0.0
        scores = [float(r.overall_score) for r in self.ratings]
        return sum(scores) / len(scores)
    
    def __str__(self):
        return f"SafetyProfile(vehicle_id={self.vehicle_id}, ratings={len(self.ratings)})"
