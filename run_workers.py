#!/usr/bin/env python
"""
Worker runner script for collecting vehicle data

Usage:
    python run_workers.py          # Run workers once
    python run_workers.py --daemon # Run workers in daemon mode
"""
import asyncio
import argparse
import logging
import time
from datetime import datetime

from app.config import settings
from app.workers import run_all_workers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def run_workers_once():
    """Run workers a single time"""
    logger.info("Starting workers...")
    start_time = datetime.utcnow()

    try:
        await run_all_workers()
        logger.info(f"Workers completed successfully in {datetime.utcnow() - start_time}")
    except Exception as e:
        logger.error(f"Error running workers: {e}", exc_info=True)


async def run_workers_daemon():
    """Run workers in daemon mode with interval"""
    logger.info(f"Starting worker daemon (interval: {settings.worker_interval}s)")

    while True:
        try:
            start_time = datetime.utcnow()
            await run_all_workers()
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Worker cycle completed in {elapsed:.2f}s")

            # Sleep until next interval
            sleep_time = max(0, settings.worker_interval - elapsed)
            logger.info(f"Sleeping for {sleep_time:.2f}s until next cycle")
            await asyncio.sleep(sleep_time)

        except Exception as e:
            logger.error(f"Error in worker daemon: {e}", exc_info=True)
            # Sleep before retrying on error
            await asyncio.sleep(60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Vehicle data worker")
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run workers in daemon mode (continuous)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=None,
        help="Override worker interval (seconds)",
    )

    args = parser.parse_args()

    if args.interval:
        settings.worker_interval = args.interval

    if args.daemon:
        logger.info("Running workers in daemon mode")
        asyncio.run(run_workers_daemon())
    else:
        logger.info("Running workers once")
        asyncio.run(run_workers_once())


if __name__ == "__main__":
    main()
