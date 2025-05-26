# 4. Эндпоинт для получения статистики (routers/statistics.py)
from datetime import datetime
from fastapi import APIRouter, Query

from app.services.delivery_log import DeliveryLogService

router = APIRouter(tags=["Statistics"])

@router.get("/daily-summary")
async def get_daily_summary(
    date: datetime = Query(..., description="Дата в формате YYYY-MM-DD")
):
    """
    Получить суммарную стоимость доставок по типам за указанный день
    """
    return await DeliveryLogService.get_daily_summary(date)