"""
Configuration settings for the application
"""
import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # App
    app_name: str = "Vehicle Analytics Backend"
    app_version: str = "0.1.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = environment == "development"

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://admin:ChangeMe123!@localhost:5432/pythonapp"
    )
    sqlalchemy_echo: bool = debug

    # AWS
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    aws_s3_bucket: str = os.getenv("AWS_S3_BUCKET", "vehicle-data")

    # SQS
    sqs_queue_url: Optional[str] = os.getenv("SQS_QUEUE_URL")
    sqs_dlq_url: Optional[str] = os.getenv("SQS_DLQ_URL")

    # API
    api_title: str = "Vehicle Analytics API"
    api_description: str = "Distributed system for vehicle data collection, processing and analytics"
    api_version: str = "0.1.0"

    # Workers
    worker_interval: int = int(os.getenv("WORKER_INTERVAL", "3600"))  # 1 hour
    worker_batch_size: int = int(os.getenv("WORKER_BATCH_SIZE", "100"))

    # FIPE API simulation
    fipe_api_enabled: bool = os.getenv("FIPE_API_ENABLED", "true").lower() == "true"
    fipe_api_base_url: str = os.getenv("FIPE_API_BASE_URL", "https://parallelum.com.br/fipe/api/v1")

    # Web Scraping
    web_scraping_enabled: bool = os.getenv("WEB_SCRAPING_ENABLED", "true").lower() == "true"
    web_scraping_user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
