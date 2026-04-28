"""Reliability domain - Value Objects"""
from app.shared.types import ValueObject
from app.shared.exceptions import InvalidValueObjectError


class ReliabilityScore(ValueObject):
    """Reliability score value object (0-100)"""
    
    def __init__(self, score: float):
        if not 0 <= score <= 100:
            raise InvalidValueObjectError(f"Reliability score must be 0-100, got {score}")
        self.score = float(score)
    
    def __float__(self):
        return self.score
    
    def __str__(self):
        return f"{self.score}%"


class WarrantyInfo(ValueObject):
    """Warranty information value object"""
    
    def __init__(self, claims_rate: float, avg_cost: float):
        if not 0 <= claims_rate <= 100:
            raise InvalidValueObjectError(f"Claims rate must be 0-100, got {claims_rate}")
        if avg_cost < 0:
            raise InvalidValueObjectError(f"Average cost cannot be negative: {avg_cost}")
        
        self.claims_rate = float(claims_rate)
        self.avg_cost = float(avg_cost)
    
    def __str__(self):
        return f"Warranty(claims={self.claims_rate}%, avg_cost=${self.avg_cost})"
