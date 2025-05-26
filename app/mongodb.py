import logging

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models.log_models import DeliveryLog

logger = logging.getLogger(__name__)


async def init_mongodb():
    # Подключение с аутентификацией
    client = AsyncIOMotorClient(
        f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:27017/{settings.MONGO_DB}",
        authSource="admin"  # Аутентификация через admin базу
    )

    try:
        await init_beanie(
            database=client[settings.MONGO_DB],
            document_models=[DeliveryLog]
        )
        logger.info("MongoDB успешно подключен")
    except Exception as e:
        logger.error(f"Ошибка подключения к MongoDB: %s", e)
        raise