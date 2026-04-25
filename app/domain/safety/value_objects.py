"""Safety domain - Value Objects"""
from enum import Enum
from app.shared.types import ValueObject
from app.shared.exceptions import InvalidValueObjectError


class SafetyOrganization(str, Enum):
    """Safety rating organization"""
    NHTSA = "NHTSA"
    EURO_NCAP = "Euro NCAP"
    JC_08 = "JC-08"


class SafetyScore(ValueObject):
    """Safety score value object (0-5)"""
    
    def __init__(self, score: float):
        if not 0 <= score <= 5:
            raise InvalidValueObjectError(f"Safety score must be 0-5, got {score}")
        self.score = float(score)
    
    def __float__(self):
        return self.score
    
    def __str__(self):
        return f"{self.score}/5.0"


class SafetyRating(ValueObject):
    """Individual safety rating"""
    
    def __init__(
        self,
        organization: SafetyOrganization,
        overall_score: SafetyScore,
        frontal_crash: SafetyScore,
        side_crash: SafetyScore,
        rollover: SafetyScore,
        child_protection: SafetyScore,
        pedestrian_protection: SafetyScore
    ):
        self.organization = organization
        self.overall_score = overall_score
        self.frontal_crash = frontal_crash
        self.side_crash = side_crash
        self.rollover = rollover
        self.child_protection = child_protection
        self.pedestrian_protection = pedestrian_protection
    
    def __str__(self):
        return f"{self.organization.value}: {self.overall_score}"
