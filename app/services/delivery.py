import logging
from datetime import datetime, UTC

from tortoise.transactions import in_transaction
from asyncmy.errors import OperationalError

from app.models.package import Package
from app.services.currency import get_usd_rate
from app.services.delivery_log import DeliveryLogService
from app.utils.exceptions import DeliveryCalculationError

logger = logging.getLogger(__name__)


async def calculate_delivery_costs():
    """Расчет стоимости доставки"""
    try:
        rate = await get_usd_rate()
        if not rate:
            logger.error("Не удалось получить курс доллара")
            return False

        try:
            async with in_transaction():
                packages = await Package.filter(delivery_cost__isnull=True).select_for_update()

                if not packages:
                    logger.info("Нет посылок для расчета доставки")
                    return True

                updated = 0
                for package in packages:
                    try:
                        delivery_cost = (package.weight * 0.5 + package.content_cost * 0.01) * rate

                        logger.warning(package)
                        logger.warning(package.__dict__)
                        logger.warning(package.type_id)


                        # сохраняем лог в МонгоДБ
                        await DeliveryLogService.create_log(
                            package_id=package.id,
                            package_type=package.type_id,
                            delivery_cost=delivery_cost
                        )

                        package.delivery_cost = round(delivery_cost, 2)
                        package.calculated_at = datetime.now(UTC)
                        await package.save()
                        updated += 1
                    except Exception as e:
                        logger.error("Ошибка при расчете %s: %s", package.id, e)
                        continue

                logger.info(f"Обновлено {updated}/{len(packages)} посылок")
                return True

        except OperationalError as e:
            logger.error(f"Ошибка база данных при вычислении: {e}")
            return False

    except Exception as e:
        logger.critical("Ошибка при расчете доставки: %s", e)
        raise DeliveryCalculationError()
