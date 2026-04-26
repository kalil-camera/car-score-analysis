"""Background workers for data collection"""
import asyncio

from .workers import BaseWorker, FIPEWorker, WebScrapingWorker, ReliabilityIndexWorker


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


__all__ = [
    "BaseWorker",
    "FIPEWorker",
    "WebScrapingWorker",
    "ReliabilityIndexWorker",
    "run_all_workers",
    "run_workers_sync",
]
