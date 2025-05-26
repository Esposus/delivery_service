# 1. Модель данных для лога расчета стоимости (log_models.py)
from datetime import datetime
from typing import Any

from beanie import Document
from cryptography.utils import Enum
from pydantic import Field
from uuid import UUID


# class PackageType(str, Enum):
#     CLOTHES = "clothes"
#     ELECTRONICS = "electronics"
#     OTHER = "other"

class DeliveryLog(Document):
    package_id: UUID
    package_type: int
    delivery_cost: float
    calculated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "delivery_logs"
        indexes = [
            [("package_type", 1), ("calculated_at", 1)],  # Составной индекс для быстрых запросов
        ]