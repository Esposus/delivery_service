from enum import StrEnum
from uuid import UUID

from tortoise import fields
from tortoise.models import Model


class PackageTypeEnum(StrEnum):
    # одежда, электроника, разное
    CLOTHES = "clothes"
    ELECTRONICS = "electronics"
    OTHER = "other"


class PackageType(Model):
    id = fields.IntField(pk=True, default=3)
    name = fields.CharEnumField(PackageTypeEnum, max_length=255)


if __name__ == "__main__":
    p = PackageType(name=PackageTypeEnum.CLOTHES)
    print(p.name)
    print(list(PackageTypeEnum))
