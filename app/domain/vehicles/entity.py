"""Vehicle domain - Aggregate Root Entity"""
from datetime import datetime
from typing import Optional
from app.shared.types import AggregateRoot
from app.shared.exceptions import BusinessRuleViolationError
from .value_objects import Brand, Model, Year, VehicleSpecification, FuelType, BodyType


class Vehicle(AggregateRoot):
    """
    Vehicle Aggregate Root
    
    Invariants:
    - Uma vehicle deve ter brand, model, year obrigatoriamente
    - Specification é imutável após criação
    """
    
    def __init__(
        self,
        id: int = None,
        brand: Brand = None,
        model: Model = None,
        year: Year = None,
        fuel_type: FuelType = None,
        body_type: BodyType = None,
        description: Optional[str] = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        super().__init__(id)
        
        # Validar invariantes
        if not all([brand, model, year, fuel_type, body_type]):
            raise BusinessRuleViolationError(
                "Vehicle must have brand, model, year, fuel_type and body_type"
            )
        
        self.specification = VehicleSpecification(brand, model, year, fuel_type, body_type)
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @property
    def brand(self) -> Brand:
        return self.specification.brand
    
    @property
    def model(self) -> Model:
        return self.specification.model
    
    @property
    def year(self) -> Year:
        return self.specification.year
    
    @property
    def fuel_type(self) -> FuelType:
        return self.specification.fuel_type
    
    @property
    def body_type(self) -> BodyType:
        return self.specification.body_type
    
    def update_description(self, description: str):
        """Update vehicle description"""
        self.description = description
        self.updated_at = datetime.utcnow()
    
    def __str__(self):
        return f"Vehicle(id={self.id}, spec={self.specification})"
