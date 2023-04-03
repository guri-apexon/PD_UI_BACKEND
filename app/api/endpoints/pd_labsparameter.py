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


@router.post("/create_labsparameter")
def create_labsparameter_data(
        *,
        db: Session = Depends(deps.get_db),
        data: schemas.LabDataCreate,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Create new labs data records
    :param db: database session
    :param data: clinical terms
    :param _: To validate API token
    :returns: response with newly create record
    """
    lab_data = crud.labdata_content.save_data_to_db(db, data.data)
    return lab_data


@router.post('/update_labsparameter')
def update_labsparamater_data(
        *,
        db: Session = Depends(deps.get_db),
        data: schemas.LabDataUpdate,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    update new labs data records
    :param db: database session
    :param data: clinical terms
    :param _: To validate API token
    :returns: response with newly create record
    """
    lab_data = crud.labdata_content.update_data_db(data.data)
    return lab_data


@router.post('/delete_labsparameter')
def delete_labsparameter_data(
        *,
        db: Session = Depends(deps.get_db),
        data: schemas.LabData,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    delete new labs data records
    :param db: database session
    :param data: clinical terms
    :param _: To validate API token
    :returns: response with deleted record
    """
    lab_data = crud.labdata_content.delete_data_db(db, data.data)
    return lab_data
