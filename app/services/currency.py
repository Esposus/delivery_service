# services/currency.py
import httpx
from app.config import settings
from redis import asyncio as aioredis


async def get_usd_rate() -> float:
    async with aioredis.from_url(settings.REDIS_URL) as redis:
        cached_rate = await redis.get("usd_rate")
        if cached_rate:
            return float(cached_rate)

        async with httpx.AsyncClient() as client:
            response = await client.get(settings.CBR_API_URL)
            rate = response.json()["Valute"]["USD"]["Value"]
            await redis.set("usd_rate", rate, ex=300)
            return rate
