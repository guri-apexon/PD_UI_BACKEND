from typing import Any, List

from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.MetadataSoftdelete])
def get_metadata_on_delete_condition(
        db: Session = Depends(deps.get_db),
        id: str = None,
        userId: str = None,
        protocol: str = None,
        projectId: str = None,
        #Opportunity no: str = None,
        sponsor: str = None,
        indication: str = None,
        moleculeDevice: str = None,
        amendment: str = None,
        versionNumber: str = None,
        documentStatus: str = None,
        isActive: bool=None
) -> Any:
    """
    Get protocol data.
    """
    #records = crud.pd_protocol_metadata.get_records_by_filter_condition(db, protocol,projectId,sponsor,indication,moleculeDevice,amendment,versionNumber,documentStatus)
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

    records=crud.pd_protocol_metadata.get_metadata_by_deleteCondition_old(db,filter)

    if len(records) > 0:
        deleted_data = crud.pd_protocol_metadata.get_metadata_by_deleteCondition(db, records,isActive)
    else:
        raise HTTPException(status_code=404, detail="Item not found for Condition {}".format(filter))

    return deleted_data
#
# @router.post("/", response_model=schemas.MetadataSoftdelete)
# def create_soft_delete(
#         *,
#         db: Session = Depends(deps.get_db),
#         protocol_metadata_soft_delete_in: schemas.ProtocolMetadataSoftDeleteCreate,
# ) -> Any:
#     """
#     Create a post status.
#     """
#     protocol_metadata = crud.pd_protocol_metadata.create_soft_delete(db, obj_in=protocol_metadata_soft_delete_in)
#     return protocol_metadata
