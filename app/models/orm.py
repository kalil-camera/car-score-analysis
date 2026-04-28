"""
SQLAlchemy ORM models for database
"""
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Vehicle(Base):
    """Vehicle model"""

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False, index=True)
    model = Column(String(100), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    fuel_type = Column(String(50), nullable=False)  # Gasolina, Diesel, Etanol, etc
    body_type = Column(String(50), nullable=False)  # Sedan, SUV, Hatch, etc
    description = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    prices = relationship("VehiclePrice", back_populates="vehicle", cascade="all, delete-orphan")
    safety_ratings = relationship("SafetyRating", back_populates="vehicle", cascade="all, delete-orphan")
    reliability_index = relationship("ReliabilityIndex", back_populates="vehicle", uselist=False)

    __table_args__ = (
        Index("idx_vehicle_brand_model_year", "brand", "model", "year"),
    )


class VehiclePrice(Base):
    """Historical vehicle prices"""

    __tablename__ = "vehicle_prices"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="BRL")
    source = Column(String(50), nullable=False)  # FIPE, WebScrape, API, etc
    market_type = Column(String(50), nullable=False)  # Novo, Usado
    recorded_at = Column(DateTime, nullable=False, index=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="prices")

    __table_args__ = (
        Index("idx_price_vehicle_recorded", "vehicle_id", "recorded_at"),
    )


class SafetyRating(Base):
    """Vehicle safety ratings"""

    __tablename__ = "safety_ratings"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    organization = Column(String(100), nullable=False)  # NHTSA, Euro NCAP, INMETRO, etc
    overall_score = Column(Float, nullable=False)  # 0-5 stars or percentage
    frontal_crash = Column(Float, nullable=True)
    side_crash = Column(Float, nullable=True)
    rollover = Column(Float, nullable=True)
    child_protection = Column(Float, nullable=True)
    pedestrian_protection = Column(Float, nullable=True)
    url = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="safety_ratings")

    __table_args__ = (
        Index("idx_safety_rating_vehicle_org", "vehicle_id", "organization"),
    )


class ReliabilityIndex(Base):
    """Vehicle reliability index"""

    __tablename__ = "reliability_index"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, unique=True, index=True)
    score = Column(Float, nullable=False)  # 0-10 or 0-100
    breakdown_frequency = Column(Float, nullable=True)  # Average breakdowns per year
    customer_satisfaction = Column(Float, nullable=True)  # 0-10
    warranty_claims_rate = Column(Float, nullable=True)  # Percentage
    repair_cost_index = Column(Float, nullable=True)  # Relative to average
    data_source = Column(String(100), nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    vehicle = relationship("Vehicle", back_populates="reliability_index")


class DataCollectionLog(Base):
    """Log for data collection worker runs"""

    __tablename__ = "data_collection_logs"

    id = Column(Integer, primary_key=True, index=True)
    worker_name = Column(String(100), nullable=False, index=True)  # fipe_worker, scraper_worker
    status = Column(String(20), nullable=False)  # success, failed, partial
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    items_processed = Column(Integer, default=0)
    items_failed = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    metadata = Column(Text, nullable=True)  # JSON

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_collection_log_worker_created", "worker_name", "created_at"),
    )
