from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..core.database import get_db
from ..crud.authentication import get_current_user

router = APIRouter(prefix="/inland-transport")

@router.get(path="/get/id/{id}", response_model=schemas.InlandTransport, status_code=status.HTTP_200_OK, tags=["Inland Transport"])
async def get_inland_transport_by_id(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.inland_transport.get_inland_transport_by_id(id, db)

@router.get(path="/get", response_model=schemas.Pagination[schemas.InlandTransport], status_code=status.HTTP_200_OK, tags=["Inland Transport"])
async def get_inland_transports(page: int = 1, limit: int = 10, source_id: int = None, warehouse_id: int = None, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.inland_transport.get_inland_transports(db, page, limit, source_id, warehouse_id)

@router.post(path="/create", response_model=schemas.InlandTransport, status_code=status.HTTP_200_OK, tags=["Inland Transport"])
async def create_inland_transport(data: schemas.InlandTransportCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.inland_transport.create_inland_transport(data, db)

@router.put(path="/update/{id}", response_model=schemas.InlandTransport, status_code=status.HTTP_200_OK, tags=["Inland Transport"])
async def update_inland_transport(id: int, data: schemas.InlandTransportUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.inland_transport.update_inland_transport(id, data, db)

@router.delete(path="/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Inland Transport"])
async def delete_inland_transport(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return await crud.inland_transport.delete_inland_transport(id, db)

@router.get(path="/add-from-xlsx", status_code=status.HTTP_200_OK, tags=["Inland Transport"])
async def add_costs_from_xlsx(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    import pandas as pd
    file_path = "sola.xlsx"
    sheets = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")  
    df = pd.concat(sheets.values(), ignore_index=True)
    for index, row in df.iterrows():
        if index == 0 or index > 398:
            continue
        try:
            source = schemas.SourceCreate(state=row.iloc[3], city=row.iloc[9], address=row.iloc[10], zipcode=str(row.iloc[4]))
            created_source = await crud.source.create_source(source, db)
            
            try:
                c = float(row.iloc[5])
            except:
                c = 0
            inland_transport = schemas.InlandTransportCreate(source_id=created_source.id, warehouse_id=13, cost=c)
            ga = await crud.inland_transport.create_inland_transport(inland_transport, db)
            
            try:
                c = float(row.iloc[6])
            except:
                c = 0
            inland_transport = schemas.InlandTransportCreate(source_id=created_source.id, warehouse_id=12, cost=c)
            ny = await crud.inland_transport.create_inland_transport(inland_transport, db)
            
            try:
                c = float(row.iloc[7])
            except:
                c = 0
            inland_transport = schemas.InlandTransportCreate(source_id=created_source.id, warehouse_id=11, cost=c)
            ca = await crud.inland_transport.create_inland_transport(inland_transport, db)
            
            try:
                c = float(row.iloc[8])
            except:
                c = 0
            inland_transport = schemas.InlandTransportCreate(source_id=created_source.id, warehouse_id=9, cost=c)
            tx = await crud.inland_transport.create_inland_transport(inland_transport, db)
        except Exception as e:
            db.rollback()
            print(f"Failed at index {index}, details: {e}")

# Failed at index 25, details: 409: Zipcode already in use
# Failed at index 64, details: 2 validation errors for SourceCreate
# city
#   Input should be a valid string [type=string_type, input_value=nan, input_type=float]
#     For further information visit https://errors.pydantic.dev/2.10/v/string_type
# address
#   Input should be a valid string [type=string_type, input_value=nan, input_type=float]
#     For further information visit https://errors.pydantic.dev/2.10/v/string_type
# Failed at index 220, details: 1 validation error for SourceCreate
# city
#   Input should be a valid string [type=string_type, input_value=nan, input_type=float]
#     For further information visit https://errors.pydantic.dev/2.10/v/string_type
