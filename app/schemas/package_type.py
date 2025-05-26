from pydantic import BaseModel


class PackageTypeResponse(BaseModel):
    id: int
    name: str
