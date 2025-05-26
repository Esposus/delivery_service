from fastapi import HTTPException, status


class PackageNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")


class DeliveryCalculationError(Exception):
    pass
