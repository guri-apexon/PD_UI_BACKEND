import logging
from typing import List

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus

from app import crud, schemas
from app.api import deps
from app.utilities.config import settings
from app.utilities.elastic_utilities import update_bulk_elastic
router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)

@router.post("/")
def search_elastic(search_json_in: schemas.SearchJson, db: Session = Depends(deps.get_db)):
    try:
        logger.info("Received request in ES keyword_search.search_elastic: {}".format(search_json_in))
        res = crud.query_elastic(search_json_in, db)
    except Exception as ex:
        logger.exception("Exception Inside keyword_search.search_elastic: {}".format(ex))
        res = dict()
        res['ResponseCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
        res['Message'] = str(ex)

    return (res)

@router.put("/sync_qcStatus_db_es", response_model = tuple)
async def sync_qcStatus_db_es(*,
        db: Session = Depends(deps.get_db),
        docIdArray: List[str] = Query(None, description = 'Internal document id'),
        syncAllProtocols: bool = Query(False, description = 'Update all protocol qcStatus'),
        userId: str = Query(..., description = 'UserId associated with the document(s)', min_length=6, max_length=12)
) -> tuple:
    """
    Syncronizes qcStatus of the requested protocol(s) from SQLserver database to elastic search
    > Note: If both syncAllProtocols and docIdArray are provided, only docIdArray is considered
    """
    logger.info(f'sync_qcStatus_db_es: Triggerd by {userId}; Getting Metadata for the docIdArray:{docIdArray} or all:{syncAllProtocols}')

    all_qc_status = []

    if docIdArray is None and syncAllProtocols is False:
        logger.exception(f'sync_qcStatus_db_es: No Valid input Provided')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Valid input Provided")

    if docIdArray:
        for doc_id in docIdArray:
            protocol_metadata = await crud.pd_protocol_metadata.get_qc_status(db, doc_id = doc_id)
            if protocol_metadata:
                all_qc_status.append(protocol_metadata[0])
    else:
        protocol_metadata = await crud.pd_protocol_metadata.get_qc_status(db)
        all_qc_status = protocol_metadata

    es_update_dict = {exist_doc.pop('id'): exist_doc for exist_doc in all_qc_status}

    es_response, success_num, failures = update_bulk_elastic(es_update_dict)

    if es_response:
        es_message_str = f"ES update completed. success docs: {success_num}; Failure docs: {len(failures)}"
    else:
        es_message_str = f"ES update (partially) failed. success docs: {success_num}; Failure docs: {len(failures)}"
        
    return es_response, es_message_str