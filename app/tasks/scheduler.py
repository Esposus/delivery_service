from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.delivery import calculate_delivery_costs

scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.add_job(calculate_delivery_costs, "interval", minutes=5)
    scheduler.start()
