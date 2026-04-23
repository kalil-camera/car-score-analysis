"""
Background workers for data collection
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import random

import httpx

from app.config import settings
from app.database import SessionLocal
from app.models import DataCollectionLog
from app.services import VehicleService, PriceService, SafetyService, ReliabilityService

logger = logging.getLogger(__name__)


class BaseWorker:
    """Base class for workers"""

    def __init__(self, name: str):
        self.name = name
        self.db = SessionLocal()

    def __del__(self):
        """Cleanup database session"""
        if hasattr(self, 'db'):
            self.db.close()

    def log_execution(self, status: str, items_processed: int, items_failed: int,
                      start_time: datetime, end_time: datetime,
                      error_message: str = None, metadata: dict = None):
        """Log worker execution"""
        log_entry = DataCollectionLog(
            worker_name=self.name,
            status=status,
            start_time=start_time,
            end_time=end_time,
            items_processed=items_processed,
            items_failed=items_failed,
            error_message=error_message,
            metadata=json.dumps(metadata) if metadata else None,
        )
        self.db.add(log_entry)
        self.db.commit()

        logger.info(
            f"Worker {self.name}: {status} - "
            f"Processed: {items_processed}, Failed: {items_failed}"
        )


class FIPEWorker(BaseWorker):
    """Worker for FIPE API data collection"""

    def __init__(self):
        super().__init__("fipe_worker")
        self.base_url = settings.fipe_api_base_url

    async def fetch_data(self) -> List[Dict[str, Any]]:
        """Simulate FIPE API data fetch"""
        # Simulating FIPE API response
        mock_data = [
            {
                "brand": "Fiat",
                "model": "Uno",
                "year": 2023,
                "fipe_code": "001001-5",
                "fuel_type": "Gasolina",
                "price": 55000,
            },
            {
                "brand": "Volkswagen",
                "model": "Gol",
                "year": 2023,
                "fipe_code": "029002-0",
                "fuel_type": "Gasolina",
                "price": 62000,
            },
            {
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2023,
                "fipe_code": "020006-3",
                "fuel_type": "Gasolina",
                "price": 115000,
            },
            {
                "brand": "Honda",
                "model": "Civic",
                "year": 2023,
                "fipe_code": "017002-8",
                "fuel_type": "Gasolina",
                "price": 125000,
            },
        ]

        logger.info(f"FIPE Worker: Simulating fetch of {len(mock_data)} vehicles")
        return mock_data

    async def process_data(self, data: List[Dict[str, Any]]) -> tuple:
        """Process FIPE data and store in database"""
        processed = 0
        failed = 0

        for item in data:
            try:
                # Get or create vehicle
                vehicle = VehicleService.get_or_create_vehicle(
                    self.db,
                    brand=item["brand"],
                    model=item["model"],
                    year=item["year"],
                    fuel_type=item["fuel_type"],
                    body_type="Sedan",  # Default
                )

                # Add price record
                PriceService.add_price(
                    self.db,
                    vehicle_id=vehicle.id,
                    price=item["price"],
                    currency="BRL",
                    source="FIPE",
                    market_type="Novo",
                    recorded_at=datetime.utcnow(),
                )

                processed += 1
                logger.debug(f"Processed vehicle: {item['brand']} {item['model']}")

            except Exception as e:
                failed += 1
                logger.error(f"Error processing FIPE data for {item}: {str(e)}")

        return processed, failed

    async def run(self):
        """Execute worker"""
        start_time = datetime.utcnow()
        status = "success"
        items_processed = 0
        items_failed = 0
        error_message = None

        try:
            if not settings.fipe_api_enabled:
                logger.info("FIPE worker is disabled")
                return

            # Fetch and process data
            data = await self.fetch_data()
            items_processed, items_failed = await self.process_data(data)

            if items_failed > 0:
                status = "partial"

        except Exception as e:
            status = "failed"
            error_message = str(e)
            logger.error(f"FIPE Worker failed: {error_message}")

        finally:
            end_time = datetime.utcnow()
            self.log_execution(
                status=status,
                items_processed=items_processed,
                items_failed=items_failed,
                start_time=start_time,
                end_time=end_time,
                error_message=error_message,
            )


class WebScrapingWorker(BaseWorker):
    """Worker for web scraping vehicle data"""

    def __init__(self):
        super().__init__("web_scraper_worker")
        self.headers = {
            "User-Agent": settings.web_scraping_user_agent,
        }

    async def fetch_data(self) -> List[Dict[str, Any]]:
        """Simulate web scraping vehicle data"""
        # Simulating scraped data
        mock_data = [
            {
                "brand": "Toyota",
                "model": "Hilux",
                "year": 2023,
                "fuel_type": "Diesel",
                "body_type": "Pickup",
                "price": 185000,
                "source_url": "https://example.com/toyota-hilux",
            },
            {
                "brand": "Chevrolet",
                "model": "S10",
                "year": 2023,
                "fuel_type": "Diesel",
                "body_type": "Pickup",
                "price": 165000,
                "source_url": "https://example.com/chevy-s10",
            },
            {
                "brand": "Hyundai",
                "model": "HB20",
                "year": 2023,
                "fuel_type": "Gasolina",
                "body_type": "Hatch",
                "price": 48000,
                "source_url": "https://example.com/hyundai-hb20",
            },
        ]

        logger.info(f"Web Scraper Worker: Simulating scrape of {len(mock_data)} vehicles")
        return mock_data

    async def process_data(self, data: List[Dict[str, Any]]) -> tuple:
        """Process scraped data and store in database"""
        processed = 0
        failed = 0

        for item in data:
            try:
                # Get or create vehicle
                vehicle = VehicleService.get_or_create_vehicle(
                    self.db,
                    brand=item["brand"],
                    model=item["model"],
                    year=item["year"],
                    fuel_type=item["fuel_type"],
                    body_type=item["body_type"],
                )

                # Add price record
                PriceService.add_price(
                    self.db,
                    vehicle_id=vehicle.id,
                    price=item["price"],
                    currency="BRL",
                    source="WebScrape",
                    market_type="Novo",
                    recorded_at=datetime.utcnow(),
                )

                processed += 1
                logger.debug(f"Processed scraped vehicle: {item['brand']} {item['model']}")

            except Exception as e:
                failed += 1
                logger.error(f"Error processing scraped data for {item}: {str(e)}")

        return processed, failed

    async def run(self):
        """Execute worker"""
        start_time = datetime.utcnow()
        status = "success"
        items_processed = 0
        items_failed = 0
        error_message = None

        try:
            if not settings.web_scraping_enabled:
                logger.info("Web scraping worker is disabled")
                return

            # Fetch and process data
            data = await self.fetch_data()
            items_processed, items_failed = await self.process_data(data)

            if items_failed > 0:
                status = "partial"

        except Exception as e:
            status = "failed"
            error_message = str(e)
            logger.error(f"Web Scraper Worker failed: {error_message}")

        finally:
            end_time = datetime.utcnow()
            self.log_execution(
                status=status,
                items_processed=items_processed,
                items_failed=items_failed,
                start_time=start_time,
                end_time=end_time,
                error_message=error_message,
            )


class ReliabilityIndexWorker(BaseWorker):
    """Worker for collecting reliability index data"""

    def __init__(self):
        super().__init__("reliability_worker")

    async def fetch_reliability_data(self) -> dict:
        """Simulate reliability data from various sources"""
        return {
            "Fiat Uno 2023": {
                "score": 7.2,
                "breakdown_frequency": 0.15,
                "customer_satisfaction": 7.5,
                "warranty_claims_rate": 8.5,
                "repair_cost_index": 0.85,
            },
            "Volkswagen Gol 2023": {
                "score": 7.8,
                "breakdown_frequency": 0.12,
                "customer_satisfaction": 8.0,
                "warranty_claims_rate": 7.2,
                "repair_cost_index": 0.90,
            },
            "Toyota Corolla 2023": {
                "score": 9.0,
                "breakdown_frequency": 0.05,
                "customer_satisfaction": 9.2,
                "warranty_claims_rate": 4.1,
                "repair_cost_index": 1.05,
            },
        }

    async def process_data(self, data: dict) -> tuple:
        """Process reliability data"""
        processed = 0
        failed = 0

        for vehicle_key, reliability_data in data.items():
            try:
                # Parse vehicle key
                parts = vehicle_key.split()
                brand = parts[0]
                model = parts[1]
                year = int(parts[2]) if len(parts) > 2 else 2023

                # Get vehicle (should already exist from price workers)
                vehicle = self.db.query(Vehicle).filter(
                    lambda v: v.brand == brand and v.model == model and v.year == year
                ).first()

                if vehicle:
                    from app.models import Vehicle
                    vehicle = self.db.query(Vehicle).filter(
                        Vehicle.brand == brand,
                        Vehicle.model == model,
                        Vehicle.year == year
                    ).first()

                    if vehicle:
                        ReliabilityService.set_reliability_index(
                            self.db,
                            vehicle_id=vehicle.id,
                            score=reliability_data["score"],
                            data_source="Reliability DB",
                            **{k: v for k, v in reliability_data.items() if k != "score"}
                        )
                        processed += 1
                        logger.debug(f"Updated reliability for {vehicle_key}")

            except Exception as e:
                failed += 1
                logger.error(f"Error processing reliability data for {vehicle_key}: {str(e)}")

        return processed, failed

    async def run(self):
        """Execute worker"""
        start_time = datetime.utcnow()
        status = "success"
        items_processed = 0
        items_failed = 0
        error_message = None

        try:
            data = await self.fetch_reliability_data()
            items_processed, items_failed = await self.process_data(data)

            if items_failed > 0:
                status = "partial"

        except Exception as e:
            status = "failed"
            error_message = str(e)
            logger.error(f"Reliability Worker failed: {error_message}")

        finally:
            end_time = datetime.utcnow()
            self.log_execution(
                status=status,
                items_processed=items_processed,
                items_failed=items_failed,
                start_time=start_time,
                end_time=end_time,
                error_message=error_message,
            )


async def run_all_workers():
    """Run all workers concurrently"""
    workers = [
        FIPEWorker(),
        WebScrapingWorker(),
        ReliabilityIndexWorker(),
    ]

    await asyncio.gather(*[worker.run() for worker in workers])


def run_workers_sync():
    """Run all workers (synchronous wrapper)"""
    asyncio.run(run_all_workers())
