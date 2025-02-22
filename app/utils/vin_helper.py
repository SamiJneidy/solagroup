from vininfo import Vin, ValidationError
from fastapi import HTTPException, status
from .. import schemas


async def decode_vin(vin: str) -> schemas.CarInfo:
    try:
        car = Vin(vin)
        response = schemas.CarInfo(manufacturer=car.manufacturer, country=car.country, year=car.years[0])
        return response
    except ValidationError as e:
        return schemas.CarInfo()