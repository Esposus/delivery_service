from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import Pagination, get_session_id
from app.models.package import Package
from app.models.package_type import PackageType
from app.schemas.package import PackageCreate, PackageResponse

router = APIRouter(tags=["Packages"])


@router.post("/packages", response_model=dict, summary="Create new package")
async def create_package(data: PackageCreate, session_id: str = Depends(get_session_id)):
    """
    Создать новую посылку
    """
    if not await PackageType.exists(id=data.type_id):
        raise HTTPException(status_code=400, detail="Invalid package type")
    try:
        package = await Package.create(
            name=data.name,
            weight=data.weight,
            type_id=data.type_id,
            content_cost=data.content_cost,
            session_id=session_id,
        )
        return {"id": str(package.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/packages", response_model=List[PackageResponse], summary="List packages")
async def get_packages(
    session_id: str = Depends(get_session_id),
    pagination: Pagination = Depends(),
    type_id: int | None = Query(None, description="Фильтр по типу посылки"),
    has_delivery_cost: bool | None = Query(None, description="Фильтр по стоимости доставки"),
):
    """
    Список посылок
    """
    query = Package.filter(session_id=session_id).select_related("type")

    if type_id:
        query = query.filter(type_id=type_id)

    if has_delivery_cost is not None:
        if has_delivery_cost:
            query = query.filter(delivery_cost__not_isnull=True)
        else:
            query = query.filter(delivery_cost__isnull=True)

    packages = await query.offset((pagination.page - 1) * pagination.limit).limit(pagination.limit).all()

    return [
        PackageResponse(
            id=str(pkg.id),
            name=pkg.name,
            weight=pkg.weight,
            type=pkg.type.name,
            content_cost=pkg.content_cost,
            delivery_cost=pkg.delivery_cost or "Не рассчитано",
            created_at=pkg.created_at,
        )
        for pkg in packages
    ]


@router.get("/packages/{package_id}", response_model=PackageResponse, summary="Детали посылки")
async def get_package(package_id: str, session_id: str = Depends(get_session_id)):
    """
    Получить информацию о посылке по ID
    """
    package = await Package.get_or_none(id=package_id).select_related("type")

    if not package or package.session_id != session_id:
        raise HTTPException(status_code=404, detail="Посылка не найдена")

    return PackageResponse(
        id=str(package.id),
        name=package.name,
        weight=package.weight,
        type=package.type.name,
        content_cost=package.content_cost,
        delivery_cost=package.delivery_cost or "Не рассчитано",
        created_at=package.created_at,
    )
