from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.utilities.config import settings
from app.api.endpoints import auth
import logging


router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/")
async def get_lab_data(
        *,
        db: Session = Depends(deps.get_db),
        aidoc_id: str = "",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get Lab Data.
    :param db: database session
    :param aidoc_id: document id
    :param _: To validate API token
    :returns: list of all section/headers
    """
    lab_data = crud.labdata_content.get_records(db, aidoc_id)
    return lab_data


@router.post('/lab_data_table_create')
def create_lab_data_table(
        *,
        db: Session = Depends(deps.get_db),
        data: schemas.LabDataTableCreate,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    create lab data table
    :param db: database session
    :param data: clinical terms
    :param _: To validate API token
    :returns: response with newly create record
    """
    lab_data = crud.labdata_content.create_lab_data_table(db, data.data)
    return lab_data


@router.post('/lab_data_operations')
def lab_data_operations(
        *,
        db: Session = Depends(deps.get_db),
        data: schemas.LabDataUpdate,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Method Used for the lab data operations
    :param db: database session
    :param data: array of lab data opations objects
    :param _: To validate API token
    :returns: response with newly create record
    """
    response = []

    operations = {"create": [], "update": [], "delete": []}
    for dt in data.data:
        if dt.request_type:
            operations[dt.request_type].append(dt)

    for k, v in operations.items():
        if k == "create":
            res = crud.labdata_content.save_data_to_db(db, v)
            response.append(res)
        if k == "update":
            res1 = crud.labdata_content.update_data_db(db, v)
            response.append(res1)
        if k == "delete":
            res2 = crud.labdata_content.delete_data_db(db, v)
            response.append(res2)

    if all(response):
        return {"message": "operation completed successfully"}
    else:
        return {"message": "operation not completed successfully"}
