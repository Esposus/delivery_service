from fastapi import APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist

from app.models.package_type import PackageType
from app.schemas.package_type import PackageTypeResponse

router = APIRouter(tags=["Package Types"])


@router.get("/", response_model=list[PackageTypeResponse], summary="List package types")
async def get_package_types():
    """
    Все возможные типы посылок
    """
    types = await PackageType.all()
    return [PackageTypeResponse(id=t.id, name=t.name) for t in types]
