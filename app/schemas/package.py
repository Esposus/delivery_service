# schemas/package.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PackageCreate(BaseModel):
    name: str
    weight: float = Field(..., gt=0)
    type_id: int
    content_cost: float = Field(..., gt=0)


class PackageResponse(BaseModel):
    id: UUID
    name: str
    weight: float
    type: str
    content_cost: float
    delivery_cost: float | str = Field(default="Не рассчитано")
    created_at: datetime
