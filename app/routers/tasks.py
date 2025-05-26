from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse

from app.services.delivery import calculate_delivery_costs

router = APIRouter(tags=["Tasks"])


@router.post("/calculate-delivery-costs", summary="Trigger delivery cost calculation")
async def trigger_cost_calculation(background_tasks: BackgroundTasks):
    """
    Запуск расчета стоимости доставки вручную для всех необработанных посылок
    """
    background_tasks.add_task(calculate_delivery_costs)
    return JSONResponse(status_code=202, content={"message": "Calculation started in background"})
