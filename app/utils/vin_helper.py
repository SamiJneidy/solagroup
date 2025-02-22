from vininfo import Vin, ValidationError
from fastapi import HTTPException, status
from typing import Optional
from .. import schemas


async def decode_vin(vin: Optional[str] = None) -> schemas.CarInfo:
    try:
        if vin is None:
            raise ValidationError()
        car = Vin(vin)
        response = schemas.CarInfo(manufacturer=car.manufacturer, country=car.country, year=car.years[0])
        return response
    except ValidationError as e:
        return schemas.CarInfo()