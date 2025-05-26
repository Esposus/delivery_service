import asyncio
import logging

from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError, OperationalError

from app.config import settings
from app.models.package_type import PackageType, PackageTypeEnum

logger = logging.getLogger(__name__)


async def init_db():
    retries = 10
    delay = 5

    for attempt in range(retries):
        try:
            # Инициализация без автоматического создания БД
            await Tortoise.init(
                db_url=f"mysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}/{settings.MYSQL_DB}",
                modules={"models": ["app.models"]},
                _create_db=False,  # Важное изменение!
            )

            # Проверка соединения
            try:
                conn = Tortoise.get_connection("default")
                await conn.execute_query("SELECT 1")
            except Exception as e:
                logger.error(f"Сбой подключения к база данных: %s", e)
                raise DBConnectionError("Невозможно подключиться к базе данных")

            await init_schemas()
            await init_package_types()
            return
        except (DBConnectionError, OperationalError) as e:
            logger.warning("Попытка подключения к базе %s/%s не удалась: %s", attempt + 1, retries, e)
            if attempt == retries - 1:
                logger.error("Все попытки подключиться окончились неудачно")
                raise
            await asyncio.sleep(delay)


async def init_schemas():
    """Создание таблиц"""
    try:
        await Tortoise.generate_schemas(safe=True)
        logger.info("Созданы схемы базы данных")
    except Exception as e:
        logger.error(f"Генерация схем базы данных не удалась: %s", e)
        raise


async def init_package_types():
    """Инициализация типов посылок"""
    types = [
        (PackageTypeEnum.CLOTHES, 1),
        (PackageTypeEnum.ELECTRONICS, 2),
        (PackageTypeEnum.OTHER, 3),
    ]

    for name, tid in types:
        try:
            await PackageType.update_or_create(id=tid, defaults={"name": name})
        except Exception as e:
            logger.warning(f"Не удалось инициализировать типы посылок %s: %s", name, e)

    logger.info("Типы посылок инициализированы")
