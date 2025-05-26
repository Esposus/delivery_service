# 2. Сервис для работы с логами (services/delivery_log.py)
from datetime import datetime
from uuid import UUID

from app.models import PackageType
from app.models.log_models import DeliveryLog


class DeliveryLogService:
    @staticmethod
    async def create_log(package_id: UUID, package_type: int, delivery_cost: float):
        await DeliveryLog(
            package_id=package_id,
            package_type=package_type,
            delivery_cost=delivery_cost
        ).save()

    @staticmethod
    async def get_daily_summary(date: datetime):
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        pipeline = [
            {
                "$match": {
                    "calculated_at": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": "$package_type",
                    "total_cost": {"$sum": "$delivery_cost"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "type": "$_id",
                    "total_cost": 1,
                    "count": 1,
                    "_id": 0
                }
            }
        ]

        return await DeliveryLog.aggregate(pipeline).to_list()