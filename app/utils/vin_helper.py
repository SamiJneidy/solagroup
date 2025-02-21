from vininfo import Vin, ValidationError
from fastapi import HTTPException, status
from .. import schemas


async def decode_vin(vin: str) -> schemas.CarInfo:
    try:
        car = Vin(vin)
        response = schemas.CarInfo(manufacturer=car.manufacturer, country=car.country, year=car.years[0])
        return response
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"An error has occurred while decoding VIN number. Details: {e}")