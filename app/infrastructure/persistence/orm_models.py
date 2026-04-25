"""Infrastructure layer - SQLAlchemy ORM Models"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.domain.vehicles import FuelType, BodyType


class VehicleORM(Base):
    """SQLAlchemy ORM model para Vehicle"""
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), index=True)
    model = Column(String(100), index=True)
    year = Column(Integer, index=True)
    fuel_type = Column(SQLEnum(FuelType))
    body_type = Column(SQLEnum(BodyType))
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prices = relationship("VehiclePriceORM", back_populates="vehicle", cascade="all, delete-orphan")
    safety_ratings = relationship("SafetyRatingORM", back_populates="vehicle", cascade="all, delete-orphan")
    reliability = relationship("ReliabilityORM", back_populates="vehicle", uselist=False, cascade="all, delete-orphan")


class VehiclePriceORM(Base):
    """SQLAlchemy ORM model para VehiclePrice"""
    __tablename__ = "vehicle_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), index=True)
    amount = Column(Float)
    currency = Column(String(3), default="BRL")
    source = Column(String(50))
    market_type = Column(String(20))
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    vehicle = relationship("VehicleORM", back_populates="prices")


class SafetyRatingORM(Base):
    """SQLAlchemy ORM model para SafetyRating"""
    __tablename__ = "safety_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), index=True)
    organization = Column(String(50))
    overall_score = Column(Float)
    frontal_crash = Column(Float)
    side_crash = Column(Float)
    rollover = Column(Float)
    child_protection = Column(Float)
    pedestrian_protection = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    vehicle = relationship("VehicleORM", back_populates="safety_ratings")


class ReliabilityORM(Base):
    """SQLAlchemy ORM model para Reliability"""
    __tablename__ = "reliability"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), unique=True, index=True)
    overall_score = Column(Float, default=50.0)
    breakdown_frequency = Column(Float, default=0.0)
    customer_satisfaction = Column(Float, default=0.0)
    warranty_claims_rate = Column(Float, default=0.0)
    warranty_avg_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    vehicle = relationship("VehicleORM", back_populates="reliability")


class DataCollectionLogORM(Base):
    """SQLAlchemy ORM model para DataCollectionLog"""
    __tablename__ = "data_collection_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    worker_name = Column(String(100), index=True)
    status = Column(String(50))
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    items_processed = Column(Integer, default=0)
    items_failed = Column(Integer, default=0)
    error_message = Column(String(1000), nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
