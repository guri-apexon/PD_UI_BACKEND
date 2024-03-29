from typing import Any, List

from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from enum import Enum
from app.api.endpoints import auth

router = APIRouter()


class documentStatus(str, Enum):
    final = "final"
    draft = "draft"

@router.get("/", response_model=List[schemas.MetadataSoftdelete])
def get_metadata_on_delete_condition(
        sponsor: str ,
        indication: str ,
        moleculeDevice: str ,
        amendment: str ,
        documentStatus: documentStatus,
        isActive: bool,
        versionNumber: str = None,
        id: str = None,
        userId: str = None,
        protocol: str = None,
        projectId: str = None,
        #Opportunity no: str = None,
        db: Session = Depends(deps.get_db),
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get protocol data.
    """
    filter = {'id': id,
    'userId': userId,
    'protocol': protocol,
    'projectId': projectId,
    'sponsor': sponsor,
    'indication': indication,
    'moleculeDevice': moleculeDevice,
    'amendment': amendment,
    'versionNumber': versionNumber,
    'documentStatus':documentStatus}

    records=crud.pd_protocol_metadata.get_metadata_by_filter(db,filter)

    if len(records) > 0:
        deleted_data = crud.pd_protocol_metadata.execute_metadata_by_deleteCondition(db,records,isActive)
    else:
        raise HTTPException(status_code=404, detail="Item not found for Condition {}".format(filter))

    return deleted_data

