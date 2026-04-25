"""Presentation layer - Controllers"""
from .vehicle_controller import router as vehicle_router
from .price_controller import router as price_router
from .safety_controller import router as safety_router
from .reliability_controller import router as reliability_router

__all__ = [
    "vehicle_router",
    "price_router",
    "safety_router",
    "reliability_router",
]
