# models/package.py
from tortoise.models import Model
from tortoise import fields
from uuid import uuid4

class Package(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    name = fields.CharField(max_length=255)
    weight = fields.FloatField()
    type = fields.ForeignKeyField("models.PackageType")
    content_cost = fields.FloatField()
    delivery_cost = fields.FloatField(null=True)
    session_id = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)


if __name__ == "__main__":
    print(Package.all())