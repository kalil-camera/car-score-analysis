"""Vehicle domain - Value Objects"""
from app.shared.types import ValueObject
from app.shared.exceptions import InvalidValueObjectError
from enum import Enum


class FuelType(str, Enum):
    """Fuel type value object"""
    GASOLINA = "Gasolina"
    DIESEL = "Diesel"
    ETANOL = "Etanol"
    GNV = "GNV"
    HIBRIDO = "Híbrido"
    ELETRICO = "Elétrico"


class BodyType(str, Enum):
    """Body type value object"""
    SEDAN = "Sedan"
    HATCH = "Hatch"
    SUV = "SUV"
    PICKUP = "Pickup"
    MINIVAN = "Minivan"
    COUPE = "Coupe"


class Brand(ValueObject):
    """Brand value object"""
    
    def __init__(self, name: str):
        if not name or len(name.strip()) == 0:
            raise InvalidValueObjectError("Brand name cannot be empty")
        self.name = name.strip()
    
    def __str__(self):
        return self.name


class Model(ValueObject):
    """Model value object"""
    
    def __init__(self, name: str):
        if not name or len(name.strip()) == 0:
            raise InvalidValueObjectError("Model name cannot be empty")
        self.name = name.strip()
    
    def __str__(self):
        return self.name


class Year(ValueObject):
    """Year value object"""
    
    def __init__(self, value: int):
        if value < 1900 or value > 2100:
            raise InvalidValueObjectError(f"Year {value} is out of valid range")
        self.value = value
    
    def __int__(self):
        return self.value
    
    def __str__(self):
        return str(self.value)


class VehicleSpecification(ValueObject):
    """Vehicle specification value object (imutável)"""
    
    def __init__(self, brand: Brand, model: Model, year: Year, 
                 fuel_type: FuelType, body_type: BodyType):
        self.brand = brand
        self.model = model
        self.year = year
        self.fuel_type = fuel_type
        self.body_type = body_type
    
    def __str__(self):
        return f"{self.brand} {self.model} {self.year} ({self.fuel_type})"
